# -*- coding: utf-8 -*-
"""
Created on Tue May 30 03:14:15 2023

@author: nolan
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
import matplotlib.pyplot as plt
import os
from random import randint

#Dictionary that defines the Labels of the fashion_mnist dataset.
label_dict = {0:"T-Shirt", 1:"Trouser",2:"Pullover",3:"Dress",4:"Coat",5:"Sandal",6:"Shirt",7:"Sneaker",8:"Bag",9:"Ankle Boot"}    

#Trains or retrieves the Trained Model.
def train_model(x_train,y_train):
    exists = os.path.isdir('fashion_model')
    if exists:
        print("Model Exists. Loading Model.")
        model = tf.keras.models.load_model('fashion_model')
        pass
    else:
        loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False)
        
        model = tf.keras.models.Sequential([
          tf.keras.layers.Flatten(input_shape=(28, 28)), #28x28 Pixels in images
          tf.keras.layers.Dense(784, activation='relu'), #784 Pixels (28x28)
          tf.keras.layers.Dropout(0.2),
          tf.keras.layers.Dense(10, activation=tf.nn.softmax) #10 Different Categories
        ])
    
        model.compile(optimizer='adam',
                      loss=loss_fn,
                      metrics=['accuracy'])
    
        model.fit(x_train, y_train, epochs=5)    
        model.save('fashion_model')
    return model

#Evaluates performance of Trained Model to the Test Data. Prints out the accuracy and resulting Loss function Value.
def evaluate_results(model, x_test,y_test):
    eval_results = model.evaluate(x_test,  y_test, verbose=2)
    
    loss = eval_results[0]
    test_accuracy = eval_results[1]
    print("\n\n")
    print("The Model predicted " + str(round(test_accuracy*100,2)) + "% of Test cases correctly")
    print("Resulting Loss Function: " + str(loss))
    print("\n\n")
    return

#Plots the results of the test data, displays the image, and provides the predicted category, actual category, and confidence score of each
#Number of results returned depends on value of input param 'num_tests'
def display_sample_results(num_tests,x_test, y_test,model):
    predictions = model.predict(x_test)
    for i in range(num_tests):
        r_test_index = randint(0,len(x_test)-1) #Assigns Random index
        
        image = x_test[r_test_index]
        prediction = predictions[r_test_index]
        predicted_category_key = prediction.argmax()
        confidence_score = prediction.max()
        
        title = "Predicted: " + label_dict[predicted_category_key] + "\n Actual: " + label_dict[y_test[r_test_index]] + "\n Confidence: " + str(confidence_score)
        print("Test Case: " + str(r_test_index))
        print(title)
        print()
        plt.title(title)
        plt.imshow(image, cmap='gray')
        
        plt.show()
    return
 
def main():
    # The Fashion dataset includes images of different articles of clothing. 
    # See https://www.tensorflow.org/api_docs/python/tf/keras/datasets/fashion_mnist/load_data for more info on this dataset.
    fashion = tf.keras.datasets.fashion_mnist
    
    #x_train, x_test represents the images
    #y_train, y_test represents the respective classifications
    (x_train, y_train), (x_test, y_test) = fashion.load_data()    
    x_train, x_test = x_train / 255.0, x_test / 255.0
    
    model = train_model(x_train,y_train)
    
    evaluate_results(model, x_test,y_test)
    
    num_display_tests = 5
    
    display_sample_results(num_display_tests,x_test, y_test,model)
    
if __name__ == "__main__":
    main()
    


