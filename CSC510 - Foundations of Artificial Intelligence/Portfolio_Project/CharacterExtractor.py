# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 04:40:35 2023

@author: nolan
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import cv2
import numpy as np
from Helpers import Helpers 
import os
import imutils

class CharacterExtractor():
    
    def __init__(self):
        self.helpers = Helpers()
        pass

    #FINDING LINES OF TEXT
    def get_line_ys(self, img):
        lines = np.mean(img, axis=1)
        i=0
        start_found = False
        line_ys = []
        y_size = lines.shape[0]
        while i < y_size:
            if lines[i][0] != 0 and not start_found:
                y_start = i
                start_found = True
                zzz = lines[i][0]
            elif lines[i][0] == 0 and start_found:
                y_end = i
                start_found = False
                line_ys.append([y_start, y_end])
            i+=1
        return line_ys        

    def get_chars(self, img):
        line_height, line_width, line_dims = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = img.copy()

        cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = imutils.grab_contours(cnts)
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        #Sorts the characters from Left to Right
        boundingBoxes = sorted(boundingBoxes, key=lambda b:b[0]+b[1], reverse=False)
    
        i=1
        characters = []
        character_data = []
        original_size = []          
        flattened_chars = []
        prev_x = 0
        prev_x_end = 0
        prev_y = 0
        prev_w = 0
        prev_h = 0
        extra_width = 0

        prev_x_end = boundingBoxes[0][0] + boundingBoxes[0][2]
        widths=0
        distances=0


        #GETTING AVERAGE DISTANCE BETWEEN CHARACTERS
        i=1
        while i < len(boundingBoxes):
            x,y,w,h = boundingBoxes[i]
            prev_x, prev_y, prev_w, prev_h = boundingBoxes[i-1]
            prev_x_end = prev_x+prev_w
            x_start = x
            percent_of_line_height = h/line_height
            if percent_of_line_height < 0.5:
                boundingBoxes.pop(i)
                continue
            distance = x_start - prev_x_end
            distances+= distance
            i+=1        
        avg_distance = distances/(len(boundingBoxes)-1)
        prev_x_end = boundingBoxes[0][0] + boundingBoxes[0][2]

        #EXTRACTING WORDS OUT OF THE LINE
        words=[]
        for box in boundingBoxes:
            x,y,w,h = box
            ratio = float(w)/h
            percent_of_line_height = h/line_height
           
            if percent_of_line_height < 0.5:
                continue

            roi = img2[y:y+h, x:x+w]
            original_size = []
            original_size.append(h)
            original_size.append(w)

            #RESIZING
            dim = (20, 20)
            
            # resize image
            resized_roi = cv2.resize(roi, dim, interpolation = cv2.INTER_AREA)
            #Convert to 2D Image
            resized_roi = resized_roi[:,:,0]
            
            #Flatten img
            char_data = np.ndarray.flatten(resized_roi)
            char_data = self.helpers.convert_binary(char_data,127)
            char_data = char_data / 255.0

            #Add Original Height and Width
            char_data = np.concatenate((original_size, char_data))
            
            space_between_chars = x - prev_x_end 
            if space_between_chars > avg_distance*1.5:
                words.append(characters)
                characters = []

            #Add to list of Chars
            characters.append(char_data)
            
            character_data.append(char_data)
            #END OF LOOP ACTIONS
            prev_x = x
            prev_x_end = x+w
            prev_y = y
            prev_w = w
            prev_h = h
            i+=1
        #Appends last word after exiting loop
        words.append(characters)
        return characters, words

    def read_image(self, file_path):
        img = cv2.imread(file_path)
        img2 = img.copy()
        #Gets Binary pixels
        thresh, img2 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)
        #Inverts the Pixels
        img2 = cv2.bitwise_not(img2)

        #GET Y STARTING AND STOPPING POINTS OF LINES
        line_ys = self.get_line_ys(img2)

        ii=0
        dir_path = "tmp/"
        character_data = []
        lines=[]
        for line_y in line_ys:
            y_start = line_y[0]
            y_end = line_y[1]
            #Gets the ROI of the Line
            line_roi = img2[y_start:y_end, :]
   
            #Identifies each character in the line.
            characters, words = self.get_chars(line_roi)
            
            #Appends the words identified to the lines
            lines.append(words)
            
            ii+=1    


        cv2.imshow('img',img)
 
        # waitKey() waits for a key press to close the window and 0 specifies indefinite loop
        cv2.waitKey(0)
 
        # cv2.destroyAllWindows() simply destroys all the windows we created.
        cv2.destroyAllWindows()
        return lines




def main():
    pass

if __name__ == "__main__":
    main()