#To Open TensorBoard, run the following:
#    tensorboard --logdir tmp/fcnet-tox21
# http://localhost:6006/
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

log_dir = "logs/fit/"  # Specify the directory for TensorBoard logs
tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
 
#Step 1: Load the Tox21 Dataset
_, (train, valid, test), _ = dc.molnet.load_tox21()
train_X, train_y, train_w = train.X, train.y, train.w
valid_X, valid_y, valid_w = valid.X, valid.y, valid.w
test_X, test_y, test_w = test.X, test.y, test.w

#Step 2: Remove extra datasets.
# Remove extra tasks
train_y = train_y[:, 0]
valid_y = valid_y[:, 0]
test_y = test_y[:, 0]
train_w = train_w[:, 0]
valid_w = valid_w[:, 0]
test_w = test_w[:, 0]


num_toxic_in_train_set = np.sum(train_y == 1)
num_non_toxic_in_train_set = np.sum(train_y == 0)
len_train_data = len(train_y)
percent_toxic = round(num_toxic_in_train_set / len_train_data * 100, 2)
percent_non_toxic = round(num_non_toxic_in_train_set / len_train_data * 100, 2)
print("\n\n")
print("Training Data Toxic Percentage: " + str(percent_toxic) + "%")
print("Training Data Non-toxic Percentage: " + str(percent_non_toxic) + "%")
print("\n\n")


#Step 3: Define placeholders that accept minibatches of different sizes.
# Generate tensorflow graph
d = 1024 #Dimensionality of the feature vectors
n_hidden = 50
learning_rate = .001
n_epochs = 10
batch_size = 100
keep_probability = 0.9


with tf.name_scope("Inputs"):
    x = tf.placeholder(tf.float32, (None, d))
    y = tf.placeholder(tf.float32, (None,))
    keep_probability = tf.placeholder(tf.float32)

#Step 4: Implement a hidden layer.
with tf.name_scope("hidden-layer"):
    W = tf.Variable(tf.random.normal((d, n_hidden)))
    b = tf.Variable(tf.random.normal((n_hidden,)))
    #Step 6: Add dropout to a hidden layer.
    x_hidden = tf.nn.relu(tf.matmul(x, W) + b)
    x_hidden = tf.nn.dropout(x_hidden, keep_probability)

# Define the second hidden layer
with tf.name_scope("hidden-layer2"):
    W2 = tf.Variable(tf.random.normal((n_hidden, n_hidden)))  # Adjusted the input dimension
    b2 = tf.Variable(tf.random.normal((n_hidden,)))
    # Step 6: Add dropout to the second hidden layer.
    x_hidden2 = tf.nn.relu(tf.matmul(x_hidden, W2) + b2)
    x_hidden2 = tf.nn.dropout(x_hidden2, keep_probability)

#Step 5: Complete the fully connected architecture.
with tf.name_scope("output"):
    W = tf.Variable(tf.random.normal((n_hidden, 1)))
    b = tf.Variable(tf.random.normal((1,)))
    y_logit = tf.matmul(x_hidden2, W) + b
    # the sigmoid gives the class probability of 1
    y_one_prob = tf.sigmoid(y_logit)
    # Rounding P(y=1) will give the correct prediction.
    y_pred = tf.round(y_one_prob)

with tf.name_scope("loss"):
    # Compute the cross-entropy term for each datapoint
    y_expand = tf.expand_dims(y, 1)
    entropy = tf.nn.sigmoid_cross_entropy_with_logits(logits=y_logit, labels=y_expand)
    # Sum all contributions
    l = tf.reduce_sum(entropy)

with tf.name_scope("optim"):
    train_op = tf.train.AdamOptimizer(learning_rate).minimize(l)

with tf.name_scope("summaries"):
    tf.summary.scalar("loss", l)
    merged = tf.summary.merge_all()

#Step 8: Implement mini-batching training.
train_writer = tf.summary.FileWriter('tmp/fcnet-tox21', tf.get_default_graph())
N = train_X.shape[0]
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    step = 0
    for epoch in range(n_epochs):
        pos = 0
        while pos < N:
            batch_X = train_X[pos:pos+batch_size]
            batch_y = train_y[pos:pos+batch_size]
            feed_dict = {x: batch_X, y: batch_y, keep_probability: keep_probability }
            _, summary, loss = sess.run([train_op, merged, l], feed_dict=feed_dict)
            print("epoch %d, step %d, loss: %f" % (epoch, step, loss))
            train_writer.add_summary(summary, step)
            step += 1
            pos += batch_size
    #Closing Train Writer.
    train_writer.close()

  # Make Predictions (set keep_probability to 1.0 for predictions)
    train_y_pred = sess.run(y_pred, feed_dict={x: train_X, keep_probability: 1.0})
    valid_y_pred = sess.run(y_pred, feed_dict={x: valid_X, keep_probability: 1.0})
    test_y_pred = sess.run(y_pred, feed_dict={x: test_X, keep_probability: 1.0})


print("\n\nCLASSIFICATION ACCURACY:\n")
train_weighted_score = accuracy_score(train_y, train_y_pred, sample_weight=train_w)
print("Train Weighted Classification Accuracy: %f" % train_weighted_score)
valid_weighted_score = accuracy_score(valid_y, valid_y_pred, sample_weight=valid_w)
print("Valid Weighted Classification Accuracy: %f" % valid_weighted_score)
test_weighted_score = accuracy_score(test_y, test_y_pred, sample_weight=test_w)
print("Test Weighted Classification Accuracy: %f" % test_weighted_score)
