import numpy as np

import cv2

import matplotlib.pyplot as plt

img = cv2.imread('portrait.jpg')

blur = cv2.GaussianBlur(img, (5,5), 3)

fig, (ax1, ax2) = plt.subplots(nrows = 1, ncols = 2)

# when showing images in matplotlib, convert image from BGR to RGB

ax1.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

ax1.set_title('Original')

ax2.imshow(cv2.cvtColor(blur, cv2.COLOR_BGR2RGB))

ax2.set_title('Gaussian Blurred With A 5x5 Kernel')

plt.show()