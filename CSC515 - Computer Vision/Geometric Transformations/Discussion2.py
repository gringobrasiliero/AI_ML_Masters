
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import mkdir, listdir
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Gets the full file path of a .jpg image in the local directory
def get_local_img_filepath():
    for x in listdir():
        if x.endswith(".jpg"):
            return x

def main():
    file = get_local_img_filepath()
    file="money.jpg"
    # Loading the image
    img = cv2.imread(file, 1)
     


    print(img)

    print('Shape of the image: {}'.format(img.shape))

    print('Image Height: {}'.format(img.shape[0]))

    print('Image Width: {}'.format(img.shape[1]))

    print('Image Dimension: {}'.format(img.ndim))
    height, width, channels = img.shape
    #img = cv2.resize(img, (height*2, width*2),interpolation= cv2.INTER_CUBIC )
    #img = cv2.resize(img, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)

    center = width/2, height/2
    rows, cols = img.shape[:2]
    #rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=270, scale=1)
    #rotated_image = cv2.warpAffine(
    #src=img, M=rotate_matrix, dsize=(width, height))
    
    # Define the 3 pairs of corresponding points 
    input_pts = np.float32([[0,0], [cols-1,0], [0,rows-1]])
    output_pts = np.float32([[cols-1,0], [0,0], [cols-1,rows-1]])
    
    # Calculate the transformation matrix using cv2.getAffineTransform()
    M= cv2.getAffineTransform(input_pts , output_pts)
    # Apply the affine transformation using cv2.warpAffine()
    #dst = cv2.warpAffine(img, M, (height,width))
    #out = cv2.hconcat([img, dst])

    rotated_image = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) 
   # cv2.imshow("Unchanged", out)
    cv2.imshow("Resized+Rotated", rotated_image)

    img_copy = np.copy(rotated_image)
    img_copy = cv2.cvtColor(img_copy,cv2.COLOR_BGR2RGB)
 
    plt.imshow(img_copy)
    plt.show() 
    
    input_pts = np.float32([[80,1286],[3890,1253],[3890,122],[450,115]])
    output_pts = np.float32([[100,100],[100,3900],[2200,3900],[2200,100]])

    #Splitting the Image
    #(B, G, R) = cv2.split(img)
    B = img[:,:,0]
    G = img[:,:,1]
    R = img[:,:,2]

    #Merging back into color image
    merged = cv2.merge((B,G,R))
    cv2.imwrite("temp.png", merged)
    cv2.imshow("Merged", merged) 

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

    


if __name__ == '__main__' : main()
