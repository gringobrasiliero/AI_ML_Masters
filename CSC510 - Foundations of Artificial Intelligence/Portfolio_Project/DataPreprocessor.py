# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 03:16:00 2023

@author: nolan
"""
import os
import csv
import numpy as np
import cv2
from Helpers import Helpers 


class DataPreprocessor:
    def __init__(self):
        self.test_chars_from_file = 5
        self.helpers = Helpers()
        self.minimum_unicode_char = 65
        self.maximum_unicode_char = 122

        pass
    
    def get_dataset(self, folder):
        subfolders = [ f.name for f in os.scandir(folder) if f.is_dir() ]
    
        print(subfolders)
    
        pass

    def extract_data_from_csv(self, directory):
        data = []
        x_train = []
        x_test = []
        y_train = []
        y_test = []
        i=0
        # Iterate over all files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory, filename)
            
                # Load the CSV file using NumPy
                file_data = np.genfromtxt(file_path, delimiter=',')
                #Removing Header Row
                file_data = np.delete(file_data, 0, 0)

                #Removes all rows EXCEPT for chr codes 65 - 122 (Capital and lowercase letters)
                #Column Index 2 has the Chr codes. 
                file_data = file_data[file_data[:,2] >= self.minimum_unicode_char]
                file_data = file_data[file_data[:,2] <= self.maximum_unicode_char]

                #Seperate Column 2 for Y-test
                y = file_data[:, [2]]
                #Subtracts 65 to from each, so it can be used with the classification model. (Expects categories starting from 0) 
                #When model gives predictions, it will add 65 to the result to give the proper ASCII code for the Character
                
                y = np.subtract(y,self.minimum_unicode_char)
                
                #Remove Column 0, 1, 2, 3, 4, 5, 6, 7, 10, 11
                #Removes additional columns not needed for training.
                remove_cols = [0, 1, 2, 3, 4, 5, 6, 7, 10, 11]
                file_data = np.delete(file_data, remove_cols, axis = 1)

                #Splits data so that a consistent # of characters from each font is used in Test Data Set        
                train = file_data[self.test_chars_from_file:]
                test = file_data[:self.test_chars_from_file]

                test_y = y[:self.test_chars_from_file]
                train_y = y[self.test_chars_from_file:]

                #First iteration of loop assigns the x and y test and train variables.
                if len(x_train) == 0:
                    x_train = train
                    y_train = train_y
                    x_test = test
                    y_test = test_y
                else:
                    #adds the extracted data for the font to the overall data sets containing all of the fonts
                    x_train = np.concatenate((x_train, train), axis=0)
                    y_train = np.concatenate((y_train, train_y), axis=0)
                    x_test = np.concatenate((x_test, test), axis=0)
                    y_test = np.concatenate((y_test, test_y), axis=0)

        # Concatenate all data arrays into a single array
        x_train = np.asarray(x_train, dtype=np.float32)
        x_train[:,2:] = self.helpers.convert_binary(x_train[:,2:],127 )
        x_train[:,2:] = x_train[:,2:]/255
        y_train = np.asarray(y_train, dtype=np.uint8)
        
        x_test = np.asarray(x_test, dtype=np.float32)
        x_test[:,2:] = self.helpers.convert_binary(x_test[:,2:],127)
        x_test[:,2:] = x_test[:,2:]/255
        y_test = np.asarray(y_test, dtype=np.uint8)
        
        return x_train, y_train, x_test, y_test

def main():
    pass

if __name__ == "__main__":
    main()
    
