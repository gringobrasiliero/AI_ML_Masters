# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 03:39:15 2023

@author: nolan
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
#import keras
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from random import randint
import cv2
from DataPreprocessor import DataPreprocessor 
from sklearn.utils import shuffle
import keras


class Classifier:
    def __init__(self):
        self.training_model = True
        self.model = self.load_model()
        self.char_limit = 5
        self.minimum_unicode_char = 65
        self.maximum_unicode_char = 122
        pass

    def load_model(self):
        exists = os.path.isdir('text_classifier')
        model = None
        if exists:
            model = tf.keras.models.load_model('text_classifier')
        return model

    #Trains or retrieves the Trained Model.
    def train_model(self, x_train, y_train):
        exists = os.path.isdir('text_classifier')
        if self.training_model == False:
            print("Model Exists. Loading Model.")
            model = tf.keras.models.load_model('text_classifier')
            pass
        else:
            loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
            x_train = np.squeeze(x_train)
            y_train = np.squeeze(y_train)
  
            # Randomize the training data and labels
            x_train, y_train = shuffle(x_train, y_train)
            #Stops training early if Accuracy is decreasing
            es_callback = keras.callbacks.EarlyStopping(monitor='accuracy', patience=3)

            #Calculates the total number of categories by subtracting the min unicode char from the max unicode char
            num_categories = self.maximum_unicode_char - self.minimum_unicode_char +1

            model = tf.keras.models.Sequential([
              tf.keras.layers.Dense(402, activation='relu'), #Original Height, Original Width, and 400 Pixels
              tf.keras.layers.Dropout(0.2), #20% dropout rate
              tf.keras.layers.Dense(num_categories, activation=tf.nn.softmax) #57 Different Categories = 58
            ])
        
            model.compile(optimizer='adam',
                          loss=loss_fn,
                          metrics=['accuracy'])
        
            model.fit(x_train, y_train, epochs=9001, batch_size=64, callbacks=[es_callback])    
            model.save('text_classifier')
        return model

    #Evaluates performance of the Trained Model to the Test Data. Prints out the accuracy and resulting Loss function Value.
    def evaluate_results(self, model, x_test, y_test):
        eval_results = model.evaluate(x_test,  y_test, verbose=2)
    
        loss = eval_results[0]
        test_accuracy = eval_results[1]
        print("\n\n")
        print("The Model predicted " + str(round(test_accuracy*100,2)) + "% of Test cases correctly")
        print("Resulting Loss Function: " + str(loss))
        print("\n\n")
        return

    def predict(self, imgs, model):
        if len(imgs)>1:
            imgs = np.squeeze(imgs)
        else:
            imgs = np.array(imgs)
 
        predicted_string = ""

        predictions = model.predict(imgs)
        for i in range(len(imgs)):
            r_test_index = i
        
            image = imgs[r_test_index][2:]
            image = image.reshape((20, 20))
            prediction = predictions[r_test_index]

            #Adds the minimum unicode character to adjust for correct Unicode Char
            predicted_category_key = prediction.argmax() + self.minimum_unicode_char
            confidence_score = prediction.max()

            pred = chr(predicted_category_key)

            predicted_string += pred
            title = "Predicted: " + pred + "\n Confidence: " + str(confidence_score)


        return predicted_string


def main():
    directory = "character+font+images/"

    #Loads the data
    print("Loading Dataset. Please be patient.")
    data_preprocessor = DataPreprocessor()
    x_train, y_train, x_test, y_test = data_preprocessor.extract_data_from_csv(directory)
    classifier = Classifier()

    #Trains the Model with Training Dataset
    model = classifier.train_model(x_train,y_train)
    #Tests Created Model with Test Data Set
    classifier.evaluate_results(model, x_test,y_test)

if __name__ == "__main__":
    main()
    

