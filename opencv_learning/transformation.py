import cv2 as cv
import numpy as np

img = cv.imread('samples/roi.jpg')
assert img is not None ,'file is not found, or check the path is exists ? '

res = cv.resize(img,None,fx=2,fy=2,interpolation=cv.INTER_CUBIC)


# or

height, width = img.shape[:2]

res2 = cv.resize(img,(2*height,2*width),interpolation=cv.INTER_CUBIC)

# cv.imshow('original',img)
# cv.imshow('Modified',res)
# cv.imshow("Modified version 2",res)


# image Tanslation 
img = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
row,col = img.shape
M = np.float32([[1,0,100],[0,1,50]])
dst = cv.warpAffine(img,M,(col,row))

# cv.imshow('Translated',dst)


# Rotation of the image
# need a special matrex by using cv.getRotationMatrix2D

R = cv.getRotationMatrix2D(((col-1)/2.0,(row-1)/2.0),90,1)
rot = cv.warpAffine(img,R,(col,row))
cv.imshow("Rotated",rot)

k = cv.waitKey(0) & 0xFF

if k == ord('q'):
    print("quit")

cv.destroyAllWindows()