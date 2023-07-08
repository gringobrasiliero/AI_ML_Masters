#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import listdir
import cv2
import numpy as np

def get_local_img_filepath():
    for x in listdir():
        if x.endswith(".jpg"):
            return x

def main():
    #Gets the full file path of a .jpg image in the local directory
    #This is so you do not have to rename your file to a hard coded value when testing.
    file = get_local_img_filepath()

    #Loading the image
    img = cv2.imread(file, 1)

    #Splitting the Image    
    B = img[:,:,0]
    G = img[:,:,1]
    R = img[:,:,2]

    #Getting shape of image so we know how much to move the windows.
    height, width, channels = img.shape
    
    #Showing the Blue, Green, Red Channels
    cv2.imshow("Blue Channel",B)
    cv2.moveWindow('Blue Channel',width,0)
    cv2.imshow("Green Channel",G)
    cv2.moveWindow('Green Channel',width*2,0)
    cv2.imshow("Red Channel",R)
    cv2.moveWindow('Red Channel',width*3,0)
    cv2.waitKey(0)

    
    rgb = np.dstack((B,G,R)) #Stacks the Arrays back to 3D Image

    cv2.imshow("Remerged",rgb)
    cv2.moveWindow('Remerged',width*2,height+35)
    cv2.waitKey(0)

    #Exchanging the Red and Green Channels
    brg = np.dstack((B,R,G)) #opencv uses BGR instead of RGB.
    
    cv2.imshow("BRG",brg)
    cv2.moveWindow('BRG',width*3,height+35)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    pass

if __name__ == '__main__' : main()