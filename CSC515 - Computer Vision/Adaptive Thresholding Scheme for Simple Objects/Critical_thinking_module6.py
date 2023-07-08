import cv2
from matplotlib import pyplot as plt

def process_img(img_title, img_path, block_size, c):
    out_imgs = []
    image = []
    img = cv2.imread(img_path)
    image = ["Original Image - " + img_title, img]
    out_imgs.append(image)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = (5,5)
    gray= cv2.blur(gray,kernel)

    adaptive_thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                cv2.THRESH_BINARY,block_size,c)
    
    image = ["Adaptive Thresh Mean - " + img_title, adaptive_thresh]
    out_imgs.append(image)
    return out_imgs

def main():
    block_size = 5
    c=1
    scenes = []
    indoor_imgs = process_img("Indoors", 'indoors2.jpg', block_size, c)
    scenes.append(indoor_imgs)
    closeup_imgs = process_img("Closeup", 'duck.jpg', block_size, c)
    scenes.append(closeup_imgs)
    outdoor_imgs = process_img("Outdoor", 'outdoors.jpg', block_size, c)
    scenes.append(outdoor_imgs)
    i=0
    for scene in scenes:
        for image in scene:
            plt.subplot(3,2,i+1),plt.imshow(cv2.cvtColor(image[1], cv2.COLOR_BGR2RGB))
            plt.title(image[0])
            plt.xticks([]),plt.yticks([])
            i+=1
    plt.show()
    
if __name__ == "__main__":
    main()
