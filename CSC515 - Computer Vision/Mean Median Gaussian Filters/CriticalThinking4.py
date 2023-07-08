import cv2
from matplotlib import pyplot as plt

def gaussian(img, size, sigma):
    img = cv2.GaussianBlur(img,size,sigma)
    return img

def mean_blur(img,kernel_size):
    blur = cv2.blur(img, kernel_size)
    return blur

def median_blur(img,kernel_size):
    blur = cv2.medianBlur(img, kernel_size)
    return blur

def subplot(gaus_one_images, gaus_two_images, mean_images, median_images):
    fig = plt.figure(figsize=(20,7))
    # setting values to rows and column variables
    rows = 3
    columns = 4
    i=1
    j=1
    
    for i in range(0,rows):
        fig.add_subplot(rows,columns,j)
        plt.imshow(cv2.cvtColor(gaus_one_images[i][1], cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(gaus_one_images[i][0])
        j+=1

        fig.add_subplot(rows,columns,j)
        plt.imshow(cv2.cvtColor(gaus_two_images[i][1], cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(gaus_two_images[i][0])
        j+=1

        
        fig.add_subplot(rows,columns,j)
        plt.imshow(cv2.cvtColor(mean_images[i][1], cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(mean_images[i][0])
        j+=1

        fig.add_subplot(rows,columns,j)
        plt.imshow(cv2.cvtColor(median_images[i][1], cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.title(median_images[i][0])
        
        j+=1

    plt.show()


def main():
    #OPEN IMAGE FILE
    img_file = "Mod4CT1.jpg"
    img = cv2.imread(img_file)
   
    #GAUSSIAN ONE IMAGES
    gaussian_one = []
    sigma = 1
    gaus_one_img_three = gaussian(img, (3,3), sigma)
    gaus_one_img_five = gaussian(img, (5,5), sigma)
    gaus_one_img_seven = gaussian(img, (7,7), sigma)
    #   Appending [Image Title, Image]
    gaussian_one.append(["Filter: Gaussian - Sigma: " + str(sigma) + " - Kernel: 3x3", gaus_one_img_three])
    gaussian_one.append(["Filter: Gaussian - Sigma: " + str(sigma) + " - Kernel: 5x5", gaus_one_img_five])
    gaussian_one.append(["Filter: Gaussian - Sigma: " + str(sigma) + " - Kernel: 7x7", gaus_one_img_seven])

    #GAUSSIAN TWO IMAGES
    gaussian_two = []
    sigma = 2
    gaus_two_img_three = gaussian(img, (3,3), sigma)
    gaus_two_img_five = gaussian(img, (5,5), sigma)
    gaus_two_img_seven = gaussian(img, (7,7), sigma)
    #   Appending [Image Title, Image]
    gaussian_two.append(["Filter: Gaussian - Sigma: " + str(sigma) + " - Kernel: 3x3", gaus_two_img_three])
    gaussian_two.append(["Filter: Gaussian - Sigma: " + str(sigma) + " - Kernel: 5x5", gaus_two_img_five])
    gaussian_two.append(["Filter: Gaussian - Sigma: " + str(sigma) + " - Kernel: 7x7", gaus_two_img_seven])

    #MEAN IMAGES
    mean_images = []
    mean_three = mean_blur(img,(3,3))
    mean_five = mean_blur(img,(5,5))
    mean_seven = mean_blur(img,(7,7))
    #   Appending [Image Title, Image]
    mean_images.append(["Filter: Mean - Kernel: 3x3", mean_three])
    mean_images.append(["Filter: Mean - Kernel: 5x5", mean_five])
    mean_images.append(["Filter: Mean - Kernel: 7x7", mean_seven])

    #MEDIAN IMAGES    
    median_images = []
    median_three = median_blur(img,3)
    median_five = median_blur(img,5)
    median_seven = median_blur(img,7)
    #   Appending [Image Title, Image]
    median_images.append(["Filter: Median - Kernel: 3x3", median_three])
    median_images.append(["Filter: Median - Kernel: 5x5", median_five])
    median_images.append(["Filter: Median - Kernel: 7x7", median_seven])
  
    #Plotting Images
    subplot(gaussian_one, gaussian_two, mean_images, median_images)

    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    pass













if __name__ == '__main__' : main()
