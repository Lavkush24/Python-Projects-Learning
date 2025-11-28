import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt

img = cv.imread('samples/hello.png')
assert img is not None, "image is not exists or check path is exists!"

kernel = np.ones((5,5),np.float32)/25
dst = cv.filter2D(img,-1,kernel)


dst_blur = cv.blur(img,(5,5))

plt.subplot(121),plt.imshow(img),plt.title('original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst_blur),plt.title('Bluring')
plt.xticks([]), plt.yticks([])
plt.show()
