import cv2 as cv 
import numpy as np

img = cv.imread("samples/sift_image.jpeg")
assert img is not None , "make sure path is exists ? "

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

# set hassian thershold to 400 
surf = cv.xfeatures2d.SURF_create(400)

kp, des = surf.detectAndCompute(img,None)

len(kp)
