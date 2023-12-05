
import os
import multiprocessing
import numpy as np
np.random.seed(456)
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
tf.set_random_seed(456)
import matplotlib.pyplot as plt
import deepchem as dc
from sklearn.metrics import accuracy_score
from tensorflow.keras.callbacks import TensorBoard
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import time
import shutil
#Uncomment in Google Colab
#from google.colab import drive
#drive.mount('/content/drive/')


def random_forest_classifier(train_X=[], train_y=[], train_w=[], valid_X=[], valid_y=[], valid_w=[], test_X=[], test_y=[], test_w=[]):
    sklearn_model = RandomForestClassifier(class_weight="balanced", n_estimators=50)
    print("")
    print("About to fit Random Forest Classifier model on train set.")
    sklearn_model.fit(train_X, train_y)
    print("")
    train_y_pred = sklearn_model.predict(train_X)
    valid_y_pred = sklearn_model.predict(valid_X)
    test_y_pred = sklearn_model.predict(test_X)

    weighted_score = accuracy_score(train_y, train_y_pred, sample_weight=train_w)
    print("Weighted train Classification Accuracy: %f" % weighted_score)
    weighted_score = accuracy_score(valid_y, valid_y_pred, sample_weight=valid_w)
    print("Weighted valid Classification Accuracy: %f" % weighted_score)
    weighted_score = accuracy_score(test_y, test_y_pred, sample_weight=test_w)
    print("Weighted test Classification Accuracy: %f" % weighted_score)


log_dir = "/content/drive/MyDrive/AI ML/Tox21/logs/fit/"  # Specify the directory for TensorBoard logs
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

def eval_tox21_hyperparams(n_hidden=50, n_layers=1, learning_rate=.001,dropout_prob=0.5, n_epochs=45, batch_size=100,weight_positives=True,train_X=[], train_y=[], train_w=[], valid_X=[], valid_y=[], valid_w=[], test_X=[], test_y=[], test_w=[]):
    d = 1024
    graph = tf.Graph()
    with graph.as_default():
        # Generate tensorflow graph
        with tf.name_scope("placeholders"):
            x = tf.placeholder(tf.float32, (None, d))
            y = tf.placeholder(tf.float32, (None,))
            w = tf.placeholder(tf.float32, (None,))
            keep_prob = tf.placeholder(tf.float32)
        for layer in range(n_layers):
            with tf.name_scope("layer-%d" % layer):
                W = tf.Variable(tf.random_normal((d, n_hidden)))
                b = tf.Variable(tf.random_normal((n_hidden,)))
                x_hidden = tf.nn.relu(tf.matmul(x, W) + b)
                # Apply dropout
                x_hidden = tf.nn.dropout(x_hidden, keep_prob)

        with tf.name_scope("output"):
            W = tf.Variable(tf.random_normal((n_hidden, 1)))
            b = tf.Variable(tf.random_normal((1,)))
            y_logit = tf.matmul(x_hidden, W) + b
            # the sigmoid gives the class probability of 1
            y_one_prob = tf.sigmoid(y_logit)
            # Rounding P(y=1) will give the correct prediction.
            y_pred = tf.round(y_one_prob)
        with tf.name_scope("loss"):
            # Compute the cross-entropy term for each datapoint
            y_expand = tf.expand_dims(y, 1)
            entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=y_logit, labels=y_expand)
        # Multiply by weights
            if weight_positives:
                w_expand = tf.expand_dims(w, 1)
                entropy = w_expand * entropy
        # Sum all contributions
            l = tf.reduce_sum(entropy)

        with tf.name_scope("optim"):
            train_op = tf.train.AdamOptimizer(learning_rate).minimize(l)

        with tf.name_scope("summaries"):
            tf.summary.scalar("loss", l)
            merged = tf.summary.merge_all()

        hyperparam_str = "d-%d-hidden-%d-lr-%f-n_epochs-%d-batch_size-%d-weight_pos-%s" % (d, n_hidden, learning_rate, n_epochs, batch_size, str(weight_positives))
        hyperparam_str += "-dropout-" + str(dropout_prob)
        hyperparam_str += "-layers-" + str(n_layers)

        train_writer = tf.summary.FileWriter('/content/drive/MyDrive/AI ML/Tox21/tmp/' + hyperparam_str, tf.get_default_graph())
        N = train_X.shape[0]
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            step = 0
            for epoch in range(n_epochs):
                pos = 0
                while pos < N:
                    batch_X = train_X[pos:pos+batch_size]
                    batch_y = train_y[pos:pos+batch_size]
                    batch_w = train_w[pos:pos+batch_size]
                    feed_dict = {x: batch_X, y: batch_y, w: batch_w, keep_prob: dropout_prob}
                    _, summary, loss = sess.run([train_op, merged, l], feed_dict=feed_dict)
                    train_writer.add_summary(summary, step)
                    step += 1
                    pos += batch_size
            #Closing Train Writer.
            train_writer.close()
            # Make Predictions (set keep_prob to 1.0 for predictions)
            valid_y_pred = sess.run(y_pred, feed_dict={x: valid_X, keep_prob: 1.0})
    weighted_score = accuracy_score(valid_y, valid_y_pred, sample_weight=valid_w)
    return weighted_score

def generate_queue():
    #Hyperparameter Lists
    n_hidden_list = [10,25, 50] #Number of Hidden Layers
    n_layers_list = [1,2,3] #Number of Layers
    learning_rate_list = [0.001, 0.0001, 0.00001] #Learning Rates
    keep_prob_list = [0.5, 0.75, 0.9] #Probability of keeping nodes. 1-keep_prob gives us the Dropout Rate
    n_epochs_list = [25, 45, 65] #Number of epochs
    batch_size_list = [100, 50, 25] #Size of Batches
    num_trials = 3
    scores = []
    # Create an empty DataFrame with column names
    columns = ['Hidden', 'Layers', 'Learning Rate', 'Dropout Probability', 'Epochs', 'Batch Size', 'Average Score']
    df = pd.DataFrame(columns=columns)
    file_name = 'results.csv'
    i=0
    for n_hidden in n_hidden_list:
        for n_layers in n_layers_list:
            for learning_rate in learning_rate_list:
                for dropout_prob in dropout_prob_list:
                    for n_epochs in n_epochs_list:
                        for batch_size in batch_size_list:
                            i+=1
                            param_dict = {'n_hidden':n_hidden, 'n_layers':n_layers, 'learning_rate':learning_rate, 'dropout_prob':dropout_prob, 'n_epochs':n_epochs, 'batch_size':batch_size, 'weight_positives':True}
                            while True:
                                if not data_queue.full():
                                    data_queue.put(param_dict)
                                    break

    #Creating Final Queue Items to signal the Consumers to quit. Indicates that there is nothing left to process.
    param_dict = {'n_hidden':0, 'n_layers':0, 'learning_rate':0, 'dropout_prob':0, 'n_epochs':0, 'batch_size':0, 'weight_positives':True}
    consumer_count = 12
    for i in range(consumer_count):
        data_queue.put(param_dict)
    return

def consumer(train_X, train_y, train_w, valid_X, valid_y, valid_w, test_X, test_y, test_w):
    file_name = 'content/drive/MyDrive/AI ML/Tox21/results.csv'
    num_trials = 3
    scores = []
    i=0
    df = pd.DataFrame()

    while True:
        if not data_queue.empty():
            i+=1
            data_dict = data_queue.get()
            if data_dict['n_epochs']==0:
                #Writing any final data to queue and quitting.
                df.to_csv(file_name, encoding='utf-8', header=False, index=False, mode='a')
                break
            for i in range(num_trials):
                score = eval_tox21_hyperparams(n_hidden=data_dict['n_hidden'], n_layers=data_dict['n_layers'], learning_rate=data_dict['learning_rate'], dropout_prob=data_dict['dropout_prob'], n_epochs=data_dict['n_epochs'], batch_size=data_dict['batch_size'],weight_positives=data_dict['weight_positives'],train_X=train_X, train_y=train_y, train_w=train_w, valid_X=valid_X, valid_y=valid_y, valid_w=valid_w, test_X=test_X, test_y=test_y, test_w=test_w)
                scores.append(score)
            average_score = sum(scores)/num_trials
            print("Average Accuracy: %f" % average_score)
            new_data = {
                'Hidden': data_dict['n_hidden'],
                'Layers':data_dict['n_layers'],
                'Learning Rate':data_dict['learning_rate'],
                'Dropout Probability':data_dict['dropout_prob'],
                'Epochs': data_dict['n_epochs'],
                'Batch Size':data_dict['batch_size'],
                'Average Score':average_score
                }
            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)
            #Inserting data into .csv after every 2 rows.
            if i%2==0:
                df.to_csv(file_name, encoding='utf-8', header=False, index=False, mode='a')
                df = pd.DataFrame()
            #Resetting Scores
            scores = []
        else:
            #Queue is Empty. Quitting.
            return

#Data Queue is global
data_queue = multiprocessing.Queue()

def main():
    columns = ['Hidden', 'Layers', 'Learning Rate', 'Dropout Probability', 'Epochs', 'Batch Size', 'Average Score']
    df = pd.DataFrame(columns=columns)
    file_name = 'content/drive/MyDrive/AI ML/Tox21/results.csv'

    log_dir = 'content/drive/MyDrive/AI ML/Tox21/tmp/'
    #Removing all logs if exists to restart.
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    
    #Writing headers to CSV File
    df.to_csv(file_name, encoding='utf-8', header=True, index=False, mode='w')
    #Loading Data
    _, (train, valid, test), _ = dc.molnet.load_tox21()
    train_X, train_y, train_w = train.X, train.y, train.w
    valid_X, valid_y, valid_w = valid.X, valid.y, valid.w
    test_X, test_y, test_w = test.X, test.y, test.w

    # Remove extra tasks
    train_y = train_y[:, 0]
    valid_y = valid_y[:, 0]
    test_y = test_y[:, 0]
    train_w = train_w[:, 0]
    valid_w = valid_w[:, 0]
    test_w = test_w[:, 0]

    #Trying Random Forest Classifier
    random_forest_classifier(train_X=train_X, train_y=train_y, train_w=train_w, valid_X=valid_X, valid_y=valid_y, valid_w=valid_w, test_X=test_X, test_y=test_y, test_w=test_w)


    #Populating Queue
    generate_queue()

    # Create and start multiple processes to write data to the CSV file
    processes = []
    
    consumer_count = 12
    for i in range(consumer_count):
        process = multiprocessing.Process(target=consumer, args=(train_X, train_y, train_w, valid_X, valid_y, valid_w, test_X, test_y, test_w,))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

if __name__ == '__main__':
    main()