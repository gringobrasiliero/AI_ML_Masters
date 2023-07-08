#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import listdir
import matplotlib.pyplot as plt
import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

def local_img_filepaths():
    file_paths = []
    for x in listdir():
        if x.endswith(".jpg"):
            file_paths.append(x)
    return file_paths


def get_images(img_files):
    images = []
    for file in img_files:
        img = cv2.imread(file)
        rows, columns, channels = img.shape
        #Splits the image in half to seperate the two images
        L_img= img[0:, 0:columns//2]
        R_img = img[0:, columns//2:]
        images.append(L_img)
        images.append(R_img)
    return images


def get_face(img):
    #Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Equalized Histogram
    equ = cv2.equalizeHist(gray)

    # read haacascade to detect faces in input image
    face_cascade = cv2.CascadeClassifier('C:\opencv\haarcascades\haarcascade_frontalface_default.xml')
    # detects faces in the input image
    faces = face_cascade.detectMultiScale(equ, 1.1, 2)

    rois=[]

    for (x,y,w,h) in faces:
       
       roi = img[y:y+h, x:x+w]
       #Zoom in on Face
       roi = cv2.resize(roi, (2*w, 2*h), interpolation = cv2.INTER_CUBIC)
       rois.append(roi)       
       # To draw a rectangle around the detected face  
       cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),1)   
    return img, rois

def get_eyes(face, face_coords):
    eyes_found = False
    # read haacascade to detect faces in input image
    face_cascade = cv2.CascadeClassifier('C:\opencv\haarcascades\haarcascade_eye.xml')
    # detects faces in the input image
    eyes = face_cascade.detectMultiScale(face, scaleFactor=1.1, minNeighbors=2, minSize=(40,40), maxSize = (60,60))
    fx, fy, fw, fh = face_coords
    num_eyes = len(eyes)
    
    if num_eyes >= 2:
        for i in range(num_eyes):
            if eyes_found:
                break
            eye_one = eyes[i]
            eye_one_x, eye_one_y, eye_one_w, eye_one_h = eye_one
            center_x_one = eye_one_x + (eye_one_w//2)
            center_y_one = eye_one_y + (eye_one_h//2)
            
            facee = cv2.cvtColor(face,cv2.COLOR_GRAY2RGB)
            #Marking Center of Eye 1 with Red Dot
            image = cv2.circle(facee , (center_x_one,center_y_one), radius=1, color=(0, 0, 255), thickness=1)
            
            for j in range(num_eyes):
                if eyes_found:
                   break
                eye_two = eyes[j]
                eye_two_x, eye_two_y, eye_two_w, eye_two_h = eye_two
                center_x_two = eye_two_x + (eye_two_w//2)
                center_y_two = eye_two_y + (eye_two_h//2)

                if eye_one_x != eye_two_x and eye_one_y != eye_two_y and eyes_found == False:
                    #Marking Center of Eye 2 with Green Dot
                    image = cv2.circle(image , (center_x_two,center_y_two), radius=1, color=(0, 255, 0), thickness=1)

                    deg = math.atan2( (center_y_two - center_y_one) , (center_x_two - center_x_one) )
                    degrees = math.degrees(deg)

                    # angle between the two eye centers must be less than 25 to increase accuracy of eye detection
                    if degrees <= 25 and degrees >= -25:
                        print("MET EYE CRITERIA")
                        eyes_found = True
    if eyes_found:        
        face = cv2.rectangle(image,(eye_one_x,eye_one_y),(eye_one_x+eye_one_w,eye_one_y+eye_one_h),(255,0,255),2)
        face = cv2.rectangle(face,(eye_two_x,eye_two_y),(eye_two_x+eye_two_w,eye_two_y+eye_two_h),(255,0,255),2)
        print("EYES FOUND")
        cv2.imshow('Detected Eyes',face)
        cv2.moveWindow('Detected Eyes',350,0)
        cv2.waitKey(0)
        return eye_one, eye_two
    else:
        print("NO EYES FOUND")
        return None, None

def rotate_face(eye_one, eye_two, img):
    height, width = img.shape[:2]
    
    eye_one_x, eye_one_y, eye_one_w, eye_one_h = eye_one
    eye_two_x, eye_two_y, eye_two_w, eye_two_h = eye_two
    center_x_one = eye_one_x + (eye_one_w//2)
    center_y_one = eye_one_y + (eye_one_h//2)
    center_x_two = eye_two_x + (eye_two_w//2)
    center_y_two = eye_two_y + (eye_two_h//2)
    
    #Radian of the two eye centers
    radian = math.atan2( (center_y_two - center_y_one) , (center_x_two - center_x_one) )
    #converts Radians to Degrees
    degrees = math.degrees(radian)
   

    #Marking the center of eyes 
    display_img = cv2.cvtColor(img,cv2.COLOR_GRAY2RGB)
    display_img = cv2.circle(display_img , (center_x_one,center_y_one), radius=1, color=(0, 0, 255), thickness=1)
    display_img = cv2.circle(display_img , (center_x_two,center_y_two), radius=1, color=(0, 0, 255), thickness=1)
    
    rot_mat = cv2.getRotationMatrix2D(center=(width/2, height/2), angle=degrees, scale=1)
    
    #display_img has the center of eyes marked with a red dot.
    display_img = cv2.warpAffine(src=display_img, M=rot_mat, dsize=(width, height))
    
    #result gets included with final resulting images without markings
    result = cv2.warpAffine(src=img, M=rot_mat, dsize=(width, height))

    cv2.imshow('Rotated Face',display_img)
    cv2.moveWindow('Rotated Face',700,0)
    cv2.waitKey(0)
    return result
    
def resize_images(images):
    avg_width=0
    avg_height=0
    #Getting average Height and Width of images
    for img in images:
        rows,columns = img.shape
        avg_width+=columns
        avg_height+=rows

    avg_height = avg_height//(len(images))
    avg_width = avg_width//(len(images))
    avg_area = avg_height*avg_width
    
    for i in range(len(images)):
        height, width = images[i].shape
        img_area = height*width
        
        if img_area < avg_area:
            #INTER_CUBIC for ZOOMING
            images[i] = cv2.resize(images[i], (avg_width, avg_height), interpolation = cv2.INTER_CUBIC)
        else:
            #INTER_AREA for SHRINKING
            images[i] = cv2.resize(images[i], (avg_width, avg_height), interpolation = cv2.INTER_AREA)
    return images

def display_image_list(imgs):
    fig = plt.figure("Final Results",figsize=(20,7))
  
    rows = 1
    columns = len(imgs)

    j=1
    for img in imgs:
        height, width = img.shape[:2]
        fig.add_subplot(rows,columns,j)
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title("Subject_"+ str(j) + " | " + " H: " + str(height)+ " | " + " W: " + str(width))

        j+=1
    plt.show()
    
def main():
    #Gets the file paths of .jpg images in current Directory, so no need to rename files when testing.
    img_files = local_img_filepaths()

    images = get_images(img_files)
    processed_images = []   
    for img in images:
        rows, columns, channels = img.shape
        img, faces = get_face(img)
        cv2.imshow('Got Face',img)
        cv2.moveWindow('Got Face',0,0)
        cv2.waitKey(0)
        for face in faces:
            face_coords = [0,0,rows,columns]

            #Image in grayscale
            gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            #Adjusted image for the effect on illumination
            equ = cv2.equalizeHist(gray)

            #Find Eyes
            eye_one, eye_two = get_eyes(equ, face_coords)
            #Rotate Image
            result = rotate_face(eye_one, eye_two, equ)
            
            processed_images.append(result)
            
    #Resize Images to Consistent Size
    processed_images = resize_images(processed_images)
    
    cv2.destroyAllWindows()
    #Display Final Results
    display_image_list(processed_images)
    pass













if __name__ == '__main__' : main()
