import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


img = cv.imread("samples/boxes.jpg")
assert img is not None, "check that path is exists? "

gray_img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# shi-tomasi detector 
corners = cv.goodFeaturesToTrack(gray_img,25,0.01,10)
corners = np.int32(corners)

for i in corners:
    x,y = i.ravel()
    cv.circle(img,(x,y),3,255,-1)

plt.imshow(img),plt.show()