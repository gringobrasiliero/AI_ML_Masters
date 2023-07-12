
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow as tf
import numpy as np
import os
from random import randint
import cv2
from DataPreprocessor import DataPreprocessor 
from sklearn.utils import shuffle
import keras
from Classifier import Classifier
from CharacterExtractor import CharacterExtractor


class TextDigitizer():

    def __init__(self):
        self.input_folder = "inputs/"
        pass

    def get_input_files(self):
        dir_list = os.listdir(self.input_folder)
        i=0
        len_dir_list = len(dir_list)
        if len_dir_list > 0:
            while i < len_dir_list:
                dir_list[i] = self.input_folder + dir_list[i]
                i+=1
        else:
            print("Please insert your images which contain the text you want extracted into the " + self.input_folder + " directory before running.")
        return dir_list

def main():
    print("Hello, I will digitize the text that is within the images that you have placed in the Inputs Folder.")

    # Get the list of all files and directories
    t = TextDigitizer()
    input_files = t.get_input_files()
    directory = "character+font+images/"
    char_extractor = CharacterExtractor()

    
    classifier = Classifier()
    model_exists = os.path.isdir('text_classifier')
    if model_exists:
        model = classifier.load_model()
        print("Trained Model Exists.\nIf you would like me to retrain, Run the Classifier.py file, or remove the 'text_classifier' directory and rerun the program.\n\nProceeding to digitize Images located in the Inputs folder.")
    else:
        print("\nI need to train the model real quick. Please be patient.\n\nLoading Dataset...")
        data_preprocessor = DataPreprocessor()

        x_train, y_train, x_test, y_test = data_preprocessor.extract_data_from_csv(directory)
        print("Training the model\n\n")
        model = classifier.train_model(x_train, y_train)
        
        print("\n\nTraining Complete. Evaluating the trained model with the test data set.\n\n")
        classifier.evaluate_results(model, x_test, y_test)

        print("\n\nProceeding to digitize your images of text...\n")

    #Loop to Predict all words on each line
    for file in input_files:
        char_extractor.character_data = []
        lines = char_extractor.read_image(file)
        text = ""
        for line in lines:
            for word in line:
                word_len = str(len(word))
                
                predicted_string = classifier.predict(word, model)
                text += predicted_string + " "
            text += "\n"

        print("File Name: " + file)
        print("Identified Text: \n\n" + text)
        print("______________________")

if __name__ == "__main__":
    main()
    
