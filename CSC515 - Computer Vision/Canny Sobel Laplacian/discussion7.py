
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random

def MSEs(img1, img2):
   h, w = img1.shape
   diff = cv2.subtract(img1, img2, dtype=cv2.CV_64F)
   err = np.sum(diff**2)
   mse = err/(float(h*w))
   return mse

def MSE(img1, img2):
   mse = np.square(np.subtract(img1,img2)).mean()
   return mse



def generate_image(thickness):
    width = 250
    height = 250
    #img = np.zeros((height,width))
    img = 255 * np.ones(shape=[height, width, 3], dtype=np.uint8)
    circle_center_coords = (64,64)
    radius = 25
    color = (0,0,0)
    img = cv2.circle(img, circle_center_coords, radius, color, thickness)
    start_point = (125, 125)
    end_point = (189, 189)
    color = (0,0, 0)
    img = cv2.rectangle(img, start_point, end_point, color, thickness)
    return img

def canny_edges(img):
    edges = cv2.Canny(img,1,200)

    #cv2.imshow('Cannied',edges)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return edges

    
def sobel_edges(img):
    # Blur the image for better edge detection
    #img_blur = cv2.GaussianBlur(img,(3,3), sigmaX=0, sigmaY=0)
    img_blur = img
      # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_8U, dx=1, dy=0, ksize=3) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_8U, dx=0, dy=1, ksize=3) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_8U, dx=1, dy=1, ksize=3) # Combined X and Y Sobel Edge Detection
    return sobelxy

    print("")
    pass

def laplacian_edges(img):
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(img, cv2.CV_8U)
    laplacian_edge = laplacian
    return laplacian_edge
    


def sp_noise(image,predicted_img,prob):
    '''
    Add salt and pepper noise to image
    prob: Probability of the noise
    '''
    output = np.zeros(image.shape,np.uint8)
    predicted_output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob 
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
                predicted_output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
                predicted_output[i][j] = 255
            else:
                output[i][j] = image[i][j]
                predicted_output[i][j] = predicted_img[i][j]
    return output, predicted_output



def main():

    #GENERATING IMAGES#
    img = generate_image(-1)
    expected_img = generate_image(1)
    expected_img = cv2.bitwise_not(expected_img)
    cv2.imshow('Expected', expected_img)
    cv2.waitKey(0)

    originals = []
    noisy_originals = []

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    expected_img = cv2.cvtColor(expected_img, cv2.COLOR_BGR2GRAY)

    noisy_img, noisy_predicted_img = sp_noise(img,expected_img,.05)
    #noisy_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #noisy_predicted_img= cv2.cvtColor(noisy_predicted_img, cv2.COLOR_BGR2GRAY)

    cv2.imshow('Original', img)
    cv2.imshow('Noisy Original', noisy_img)

    cv2.imshow('Predicted Original', expected_img)
    cv2.imshow('Noisy Predicted Original', noisy_predicted_img)
    originals.append(["Original",img])
    originals.append(["Predicted Original", expected_img])




    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #TESTING ORIGINALS
    cannied = canny_edges(img)
    #cannied = cv2.cvtColor(cannied, cv2.COLOR_BGR2GRAY)
    sobeled = sobel_edges(img)
   # sobeled = cv2.cvtColor(sobeled, cv2.COLOR_BGR2GRAY)
    laplacian = laplacian_edges(img)
    laplacian = cv2.cvtColor(laplacian, cv2.COLOR_BGR2GRAY)

    #MSE
    mse_cannied = MSE(expected_img, cannied)

    mse_sobel = MSE(expected_img, sobeled[:,:,0])
    
    mse_lap = MSE(expected_img, laplacian)



    #MSE RESULTS
    print("MSE Cannied",mse_cannied)
    print("MSE Sobel",mse_sobel)
    print('MSE Laplacian',mse_lap)


    cv2.imshow('Predicted', expected_img)
    cv2.imshow('Canny - Observed', cannied)
    cv2.imshow('Sobel - Observed', sobeled)
    cv2.imshow('Laplacian - Observed', laplacian)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    #NOISY IMAGES

    #FILTERING ON NOISY IMG
    noisy_cannied = canny_edges(noisy_img)
    noisy_sobeled = sobel_edges(noisy_img)
    noisy_laplacian = laplacian_edges(noisy_img)

    
    #MSE NOISY
    mse_noisy_cannied = MSE(expected_img, noisy_cannied)
    mse_noisy_sobel = MSE(expected_img, noisy_sobeled[:,:,0])
    mse_noisy_lap = MSE(expected_img, noisy_laplacian[:,:,0])

    #MSE RESULTS
    print()
    print("MSE Noisy Cannied",mse_noisy_cannied)
    print("MSE Noisy Sobel",mse_noisy_sobel)
    print('MSE Noisy Laplacian',mse_noisy_lap)



    cv2.imshow('img', noisy_img)
    cv2.imshow('Predicted Noisy', noisy_predicted_img)
    #cv2.imshow('imagem', imagem)
    cv2.imshow('Noisy Canny - Observed', noisy_cannied)
    cv2.imshow('Noisy Sobel - Observed', noisy_sobeled)
    cv2.imshow('Noisy Laplacian - Observed', noisy_laplacian)
    cv2.waitKey(0)
    
    
    

    cv2.destroyAllWindows()
    pass



if __name__ == "__main__":
    main()
