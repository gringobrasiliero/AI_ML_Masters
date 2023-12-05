import pandas as pd  
from keras.models import Sequential  
from keras.layers import *
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os

# Set the logging verbosity level to suppress INFO messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # '0' (default) shows all messages, '2' shows only ERROR messages


class VGame_Sales_Predictor():
    def __init__(self):
        #Data Sets
        self.x_train = None
        self.y_train= None
        self.x_test = None
        self.y_test = None
        #DATA FILE PATHS
        self.training_data = 'sales_data_training.csv'
        self.testing_data = 'sales_data_test.csv'
        self.scaled_training_data = 'sales_data_training_scaled.csv'
        self.scaled_testing_data = 'sales_data_test_scaled.csv'

        #Scaling
        # Data needs to be scaled to a small range like 0 to 1 for the neural# network to work well.
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.scale_multiplier = 0
        self.scale_adder = 0

        #MODEL
        self.model = None
        self.model_name = "trained_model.keras"
        #HYPERPARAMETERS
        self.epochs=50
        self.batch_size = 20
        self.learning_rate = 0.001
        pass

    def data_scaler(self):
        training_data_df = pd.read_csv(self.training_data)
        # Load testing data set from CSV file
        test_data_df = pd.read_csv(self.testing_data)
        # Scale both the training inputs and outputs
        scaled_training = self.scaler.fit_transform(training_data_df)
        scaled_testing = self.scaler.transform(test_data_df)
        # Print out the adjustment that the scaler applied to the total_earnings column of data
        self.scale_multiplier = self.scaler.scale_[8]
        self.scale_adder = self.scaler.min_[8]
        print("Note: total_earnings values were scaled by multiplying by {:.10f} and adding {:.6f}".format(self.scale_multiplier, self.scale_adder))
        print("\n\n")
        # Create new pandas DataFrame objects from the scaled data
        scaled_training_df = pd.DataFrame(scaled_training, columns=training_data_df.columns.values)
        scaled_testing_df = pd.DataFrame(scaled_testing, columns=test_data_df.columns.values)
        # Save scaled data dataframes to new CSV files
        if not os.path.exists(self.scaled_training_data):
            scaled_training_df.to_csv(self.scaled_training_data, index=False)
        if not os.path.exists(self.scaled_testing_data):
            scaled_testing_df.to_csv(self.scaled_testing_data, index=False)
        pass

    def data_descaler(self, data):
        print(data)
        newdata = self.scaler.inverse_transform(data)
        return data

    def load_data(self):
        # Load the training data
        train_data_df = pd.read_csv("sales_data_training_scaled.csv")
        self.y_train = train_data_df[['total_earnings']].values
        self.x_train = train_data_df.drop('total_earnings', axis=1).values
        # Load the separate test data set
        test_data_df = pd.read_csv("sales_data_testing_scaled.csv")
        self.y_test = test_data_df[['total_earnings']].values
        self.x_test = test_data_df.drop('total_earnings', axis=1).values
        return

    def define_model(self):
        #use a sequential model
        self.model = keras.Sequential()
        #use nine inputs and one output
        self.model.add(keras.layers.Input(shape=(9,)))
        #make the model dense + use the ReLU activation function for the hidden layers
        self.model.add(keras.layers.Dense(64, activation='relu'))
        #use the linear activation function for the output layer.
        self.model.add(keras.layers.Dense(1, activation='linear'))
        opt = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        # Compile the model
        #self.model.compile(optimizer='adam', loss='mean_squared_error',metrics=['mean_squared_error'])
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        pass

    def evaluate_test_data(self):
        if self.model == None:
            self.model = keras.models.load_model(self.model_name)
        test_error_rate = self.model.evaluate(self.x_test, self.y_test)
        print("The mean squared error (MSE) for the test data set is: {}\n\n".format(test_error_rate))
        d = test_error_rate / self.scale_multiplier + (-1*self.scale_adder)
        print(d)
        pass

    def predict(self):
        if self.model == None:
            self.model = keras.models.load_model(self.model_name)
        x = pd.read_csv("proposed_new_product.csv").values
        prediction = self.model.predict(x)
        
         # Grab just the first element of the first prediction (since we only have one)  
        prediction = prediction[0][0]
         # Re-scale the data from the 0-to-1 range back to dollars
         # These constants are from when the data was originally scaled down to the 0-to-1 range  
        #descaled_prediction = prediction * self.scale_multiplier + self.scale_adder
        column_names = ['critic_rating', 'is_action', 'is_exclusive', 'is_portable', 'is_role_playing', 'is_sequel', 'is_sports', 'suitable_for_kids', 'total_earnings', 'unit_price']
        #Dividing by the multiplier, then adding the inverse of the scale adder.
        descaled_prediction = prediction / self.scale_multiplier + (-1*self.scale_adder)
     
        print("Earnings Prediction for Proposed Product - ${}\n".format(descaled_prediction))
        pass

    def train(self):
        #Training Model
        with tf.device("/GPU:0"):  # Use GPU if available
            self.model.fit(self.x_train, self.y_train, epochs=self.epochs, shuffle=True,verbose=2)
        # Save the model to disk  
        self.model.save(self.model_name)
        print("Model saved to disk.\n") 
        pass

def main():
    video_game_sales_predictor = VGame_Sales_Predictor()
    video_game_sales_predictor.data_scaler()
    video_game_sales_predictor.load_data()
    video_game_sales_predictor.define_model()
    video_game_sales_predictor.train()
    video_game_sales_predictor. evaluate_test_data()
    video_game_sales_predictor.predict()
    pass

if __name__ == "__main__":
    main()
    


