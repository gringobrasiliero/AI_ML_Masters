import os
import csv
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
from collections import Counter

class k_nearest_neighbors_classifier():
    def __init__(self, k):
        self.k = k
        pass

    def train(self, file_path):
        #Get data from CSV file
        col_names = ['age', 'height', 'weight', 'gender', 'genre']
        df=pd.read_csv(file_path)
        df.columns = col_names
        #Assign Genres
        y = df.loc[:,'genre']
       
        #Remove Genre column from x
        x = df.drop(columns=['genre'])
        self.x_train = x
        self.y_train = y
        pass

    #Returns the distance between two points.
    def euclidean_distance(self, point1, point2):
        return np.sqrt(np.sum((point1-point2) ** 2))

    def predict(self, point, x_train, y_train):
        #Calculate the distance between test data and each row of training data;
        distances = [self.euclidean_distance(point,train_point) for train_point in x_train.iloc]    

        # Sort the calculated distances in ascending order based on distance values;
        #Get top k rows from the sorted array;
        k_indices = np.argsort(distances)[:self.k]
   
        # Get the labels of the k-nearest neighbors
        k_nearest_labels = [y_train[index] for index in k_indices]

        # Perform majority vote to get the most frequent class
        most_common = Counter(k_nearest_labels).most_common(1)
        #Return Predicted Class
        predicted_category = most_common[0][0]
        return predicted_category

    #This function prevents errors from occurring in case end user types in a string where a Float is required.
    def ask_for_float(self, text):
        while True:
            res = input(text)
            if res.isdigit():
                return float(res)
            else:
                print("Please Provide a Number\n\n")

    def run(self):
        print("Welcome to the K-Nearest_Neighbors Classifier. I can predict your Video Game Preferences based on your Age, Height, Weight, and Gender.\n\n")
        while True:
            age = self.ask_for_float("What is your Age?\n")
            height = self.ask_for_float("What is your Height (In Inches)?\n")
            weight = self.ask_for_float("What is your Weight?\n")
            gender = self.ask_for_float("What is your Gender? (Submit 0 for Female, and 1 for Male)\n")

            person_data = np.array([age, height, weight, gender])

            predicted_category = self.predict(person_data, self.x_train, self.y_train)
            print("I predict that your favorite genre of video game is '" + predicted_category + "'.")


            quit_program = input("Would you like to try again? (Press Y to try again. Press N to quit\n")

            if quit_program.upper() == "N":
                print("Have a nice day! Goodbye.")
                break
        pass

def main():
    #Load the data
    file_path = "VideoGamePreferencesData.csv"

    #Initialise the value of k
    k = 3
    
    classifier = k_nearest_neighbors_classifier(k)
    classifier.train(file_path)
    classifier.run()
    pass

if __name__ == "__main__":
    main()
    

