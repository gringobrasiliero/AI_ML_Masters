import json
import pandas as pd
from cleaners import *
import re
import os
import csv
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, BartTokenizer, BartConfig, TFBartForConditionalGeneration, BartTokenizerFast
import tensorflow as tf
from tensorflow import keras
from keras.optimizers import Adam
from tensorflow.keras.optimizers.schedules import PolynomialDecay
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.python.keras.losses import SparseCategoricalCrossentropy
#####UNCOMMENT IN COLAB##################

#from google.colab import drive
#drive.mount('/content/drive/')
#########################################

# Callback to calculate perplexity
class PerplexityCallback(tf.keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        valid_loss = logs['loss']
        perplexity = tf.exp(valid_loss)
        returned_perplexity = perplexity
        print(f" Epoch {epoch + 1} - Perplexity: {perplexity:.2f}")

def perplexity(y_true, y_pred):
    cross_entropy = tf.reduce_mean(
        SparseCategoricalCrossentropy()(y_true, y_pred))
    return tf.exp(cross_entropy)

class Chatbot_Trainer():
    def __init__(self):
        self.trained_model_path = 'BartModel/'
        self.pretrained_model = "facebook/bart-base"

        #Training HyperParameters
        self.learning_rate = 1e-5
        self.epochs = 3
        self.batch_size = 40
        
        #Tokenizer HyperParameters
        self.max_length = 100

        #Generate Parameters
        self.repetition_penalty = 1.2 
        self.temperature = 0.8  

        #Data
        self.x_train = None
        self.y_train = None
        self.x_test = None
        self.y_test = None
        
        #Tokenizer
        self.tokenizer = BartTokenizerFast.from_pretrained(self.pretrained_model)
        special_tokens = {"additional_special_tokens": ["<user>", "<system>"]}
        num_added_toks = self.tokenizer.add_special_tokens(special_tokens)
        print('We have added', num_added_toks, 'tokens')

        #Load Model
        
        self.model = TFBartForConditionalGeneration.from_pretrained(self.trained_model_path)
        self.model.resize_token_embeddings(len(self.tokenizer))
        pass

    def extract_data(self, file_path):
        df = pd.read_csv(file_path, sep=',')
        # Shuffle the rows
        df = df.sample(frac=1, random_state=42)
        #Dropping rows with null values
        df = df.dropna()
        # Split the DataFrame using .iloc
        x = df.iloc[:, [0]]
        y = df.iloc[:, [1]]

        # Get the shape of the DataFrame
        num_rows, num_columns = x.shape

        print("Number of rows:", num_rows)
        print("Number of columns:", num_columns)
        #Split Data
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.1, random_state=42)
        self.x_train.columns = ["Text"]
        self.y_train.columns = ["Text"]
        self.x_test.columns = ["Text"]
        self.y_test.columns = ["Text"]
     
        self.clean_data()
        return self.x_train, self.x_test, self.y_train, self.y_test

    # Converts all text to lower-cased, removes contractions, removes double white-spaces, trims
    def clean_data(self):
        self.x_train["Text"] = self.x_train["Text"].apply(lambda z: clean_data(z))
        self.x_test["Text"] = self.x_test["Text"].apply(lambda z: clean_data(z))
        self.y_train["Text"] = self.y_train["Text"].apply(lambda z: clean_data(z))
        self.y_test["Text"] = self.y_test["Text"].apply(lambda z: clean_data(z))
        return
        

    def tokenize_data(self, df):
        # Tokenize the text in the DataFrame and get attention masks
        encoded_data = df["Text"].apply(
        lambda x: self.tokenizer.encode_plus(x, add_special_tokens=False, padding='max_length', max_length=self.max_length, truncation=True)
        )   
        #Convert the tokenized data and attention masks to TensorFlow tensors
        inputIDs = [tf.constant(encoded['input_ids'], dtype=tf.int32) for encoded in encoded_data]
        attention = [tf.constant(encoded['attention_mask'], dtype=tf.int32) for encoded in encoded_data]
        return inputIDs, attention

    def train(self, x_inputIDs, x_attention, y_inputIDs):
        #Batching data into slices
        dataset = tf.data.Dataset.from_tensor_slices((
          {
              'input_ids': x_inputIDs,
              'attention_mask': x_attention,
          },
          {
              'labels': y_inputIDs,
          }
          )).batch(self.batch_size).shuffle(True)

        #Setup of Learn Rate Scheduler. 
        train_steps_per_epoch = len(x_inputIDs)//self.batch_size
        num_train_steps = train_steps_per_epoch * self.epochs
        lr_scheduler = PolynomialDecay(
            initial_learning_rate=5e-5, end_learning_rate=0.0, decay_steps=num_train_steps
        )
        #Create Optimizer
        opt = Adam(learning_rate=lr_scheduler)        
        
        #Setup Early Stopping
        early_stopping = EarlyStopping(monitor='perplexity', patience=3, mode='min', verbose=1)
        #Compile Model
        self.model.compile(optimizer=opt,loss='sparse_categorical_crossentropy',
                      metrics=[perplexity])
        
        #Training Model
        with tf.device("/GPU:0"):  # Use GPU if available
            self.model.fit(dataset, epochs=self.epochs, batch_size=self.batch_size,callbacks=[early_stopping,PerplexityCallback()])
        self.model.save_pretrained(self.trained_model_path)

    def validate_data(self):
        x_testinputIDs, x_testattention = self.tokenize_data(self.x_test)
        y_testinputIDs, y_testattention = self.tokenize_data(self.y_test)

        dataset = tf.data.Dataset.from_tensor_slices((
                {
                'input_ids': x_testinputIDs,
                'attention_mask': x_testattention
                },
                {
                'labels': y_testinputIDs,
                }
            ))

        for i, data in enumerate(dataset):
            input_ids = data[0]['input_ids']
            attention_mask = data[0]['attention_mask']
            target_ids = data[1]['labels']
            gt = self.tokenizer.decode(input_ids, skip_special_tokens=False)
            inputs = self.tokenizer(gt, add_special_tokens=True, padding='max_length', max_length=self.max_length, truncation=True,return_tensors="tf")

            print()
            print("Input: " + gt)
            generated_ids = self.model.generate([input_ids], attention_mask=[attention_mask], max_length=self.max_length, repetition_penalty=self.repetition_penalty, do_sample=True, temperature=self.temperature)
            generated_text = self.tokenizer.decode(generated_ids[0], skip_special_tokens=True)
            target_text = self.tokenizer.decode(target_ids, skip_special_tokens=True)

            print("Generated Text:", generated_text)
            print("Target Text:", target_text)

            #Breaking after 100 responses, as it would take a while to process all.
            if i == 100:
              break
        return

    def execute_training(self):
        x_inputIDs, x_attention = self.tokenize_data(self.x_train)
        y_inputIDs, y_attention = self.tokenize_data(self.y_train)
        self.train(x_inputIDs, x_attention, y_inputIDs)


def main():
    data_file_path = 'test_data/training_data.csv' #"/content/drive/MyDrive/NLP/BartModel"

    c = Chatbot_Trainer()
    #If on Google Colab, using the following for c.trained_model_path - "/content/drive/MyDrive/NLP/BartModel"
    c.pretrained_model = "facebook/bart-base"
    c.trained_model_path = 'BartModel2/'
    c.learning_rate = 1e-5
    c.epochs = 20
    c.batch_size = 40
    #Extracting Data from data set.
    c.extract_data(data_file_path)
    #Execute the Training Process from the Pretrained Model
    c.execute_training()
    #Validate the results by printing out data from the test set, bots responses, and the target response.  
    c.validate_data()
    pass

if __name__ == "__main__":
    main()