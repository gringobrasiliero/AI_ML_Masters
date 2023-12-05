
from __future__ import absolute_import, division, print_function, unicode_literals    
import pathlib    
import matplotlib.pyplot as plt  
import numpy as np  
import pandas as pd
import seaborn as sns
import tensorflow as tf    
from tensorflow import keras  
from tensorflow.keras import layers    
import tensorflow_docs as tfdocs  
import tensorflow_docs.plots  
import tensorflow_docs.modeling

class Fuel_efficiency_predictor():
    def __init__(self):
        self.train_dataset = None
        self.test_dataset = None
        self.train_labels = None
        self.test_labels = None
        self.train_stats = None
        self.normed_train_data = None
        self.normed_test_data = None
        self.EPOCHS = 1000  
        self.model = None
        self.MPG_train_stats = None
        pass

    def get_dataset(self):
        #Step 1: Download the dataset using keras get_file method.
        dataset_path = keras.utils.get_file("auto-mpg.data", "http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data")

        #Step 2: Import database using Pandas.
        column_names = ['MPG','Cylinders', 'Displacement', 'Horsepower', 'Weight', 'Acceleration', 'Model Year', 'Origin']
        raw_dataset = pd.read_csv(dataset_path, names=column_names, na_values = "?", comment='\t', sep=" ", skipinitialspace=True)
        dataset = raw_dataset.copy()
        dataset.dropna(axis=0, how='any', inplace=True)
        #Step 3: Take a screenshot of the tail of the dataset.


        print(dataset.tail())
        print("\n\n")
        #Step 4: Split the data into train and test.
        self.train_dataset = dataset.sample(frac=0.8,random_state=0)
        self.test_dataset = dataset.drop(self.train_dataset.index)

        #Step 5: Inspect the data.
        sns.pairplot(self.train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")

        #Step 6: Take a screenshot of the tail of the plots.
        plt.waitforbuttonpress()
        plt.close()

        #Step 7: Review the statistics.
        self.train_stats = self.train_dataset.describe()  
        self.MPG_train_stats = self.train_stats.pop("MPG")
        self.MPG_train_stats = self.MPG_train_stats.transpose()
        self.train_stats = self.train_stats.transpose()  
        print(self.train_stats)
        
        #Step 8: Take a screenshot of the tail of the statistics.
        print("__SCREENSHOT 3 - TAIL OF STATISTICS__\n")
        print(self.train_stats.tail())
 
        #Step 9: Split features from labels.
        #Step 10: Separate the target value, or "label," from the features. This label is the value that you will train the model to predict.
        self.train_labels = self.train_dataset.pop('MPG')  
        self.test_labels = self.test_dataset.pop('MPG')  

    def normalize_data(self, x):
        return (x - self.train_stats['mean']) / self.train_stats['std']  

    def denormalize_data(self,x):
        return (x * self.MPG_train_stats['std']) + self.MPG_train_stats['mean']
        
    def build_model(self):    
        self.model = keras.Sequential([
            layers.Dense(64, activation='relu',
            input_shape=[len(self.train_dataset.keys())]),
            layers.Dense(64, activation='relu'),
            layers.Dense(1)])      
    
        optimizer = tf.keras.optimizers.RMSprop(0.001)
        self.model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
        return self.model    

    def train(self):
        #Step 18: Train the model for 1000 epochs, and record the training and validation accuracy in the  history  object.
        
        callbacks = [tfdocs.modeling.EpochDots()]
        train_dataset = self.normed_train_data
        train_labels = self.train_labels

        history = self.model.fit(train_dataset, train_labels, epochs=1000, validation_split = 0.2, verbose=0, callbacks=callbacks)
        
        #Step 19: Visualize the model's training progress using the stats stored in the  history  object.
        hist = pd.DataFrame(history.history)
        hist['epoch'] = history.epoch
        
        #Step 20: Provide a screenshot of the tail of the history.
        print(hist.tail()) 
        #Step 21: Provide a screenshot of the history plot.
        plotter = tfdocs.plots.HistoryPlotter(smoothing_std=2)    
        plotter.plot({'Basic': history}, metric = "mae")  
        plt.ylim([0, 10])  
        plt.ylabel('MAE [MPG]')  
        plt.waitforbuttonpress()
        plt.close()
        
        plotter.plot({'Basic': history}, metric = "mse")  
        plt.ylim([0, 20])  
        plt.ylabel('MSE [MPG^2]')
        plt.waitforbuttonpress()
        plt.close()
      
        pass 

def main():
    f = Fuel_efficiency_predictor()
    f.get_dataset()
    
    
    #Step 11: Normalize the data. It is good practice to normalize features that use different scales and ranges. 
    #Although the model might converge without feature normalization, it makes training more difficult, 
    #and it makes the resulting model dependent on the choice of units used in the input.
    
    f.normed_train_data = f.normalize_data(f.train_dataset)
    f.normed_test_data = f.normalize_data(f.test_dataset)
    
    #Step 12: Build the model.
    model = f.build_model()

    #Step 13: Inspect the model
    #Step 14: Take a screenshot of the model summary.
    print(model.summary())

    #Step 15: Now, try out the model. Take a batch of  10  examples from the training data and call  model.predict   on it.
    batch_size = 10
    sampled_batch = f.normed_train_data.sample(n=batch_size)

    predictions = model.predict(sampled_batch)

    print("__Predictions__\n\n")
    print(predictions)
    print("\nUnstandardized Predictions\n")
    print(f.denormalize_data(predictions))

    #Step 16: Provide a screenshot of the model summary.
    print("MODEL SUMMARY")
    print(model.summary())

    #Step 17: Train the model.
    f.train()

    pass

if __name__ == "__main__":
    main()
    


   