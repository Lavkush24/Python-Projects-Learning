import cv2 as cv
import numpy as np

img = cv.imread("samples/contour_test.jpeg")
assert img is not None, "Make sure path is exists ?"

grey_img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
ret, thresh = cv.threshold(grey_img,127,255,0)
contours, hierachy = cv.findContours(thresh,cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
# contours, hierachy = cv.findContours(thresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)


# finding contour in the image 
contour_img = cv.drawContours(img,contours,-1,(0,255,0),3)
# contour_img = cv.drawContours(grey_img,contours,-1,(255,0,0),3)

cv.imshow("contour with chain approx none",contour_img)
# cv.imshow("contour when chain approx simple",cv.cvtColor(grey_img,cv.COLOR_GRAY2BGR))
cv.waitKey(0)
