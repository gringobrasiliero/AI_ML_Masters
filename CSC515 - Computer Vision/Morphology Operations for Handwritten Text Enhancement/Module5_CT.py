import cv2
from matplotlib import pyplot as plt

def subplot(eroded, dilated, opened, closed):
    fig = plt.figure(figsize=(20,7))
    # setting values to rows and column variables
    rows = 2
    columns = 2
    i=1
    j=1
    
    fig.add_subplot(rows,columns,j)
    plt.imshow(cv2.cvtColor(eroded, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Erosion")
    j+=1

    fig.add_subplot(rows,columns,j)
    plt.imshow(cv2.cvtColor(dilated, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Dilation")
    j+=1

    fig.add_subplot(rows,columns,j)
    plt.imshow(cv2.cvtColor(opened, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Opening")
    j+=1

    fig.add_subplot(rows,columns,j)
    plt.imshow(cv2.cvtColor(closed, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.title("Closing")
    j+=1

    plt.show()

def main():
    image = cv2.imread("Hello.jpg")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.bitwise_not(img)
    kernel_size = (5,5)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, kernel_size)
    erosion = cv2.erode(img,kernel,iterations = 1)

    dilation = cv2.dilate(img,kernel,iterations = 1)

    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    subplot(erosion, dilation, opening, closing)

    cv2.waitKey(0) 
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
