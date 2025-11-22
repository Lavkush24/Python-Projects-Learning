import cv2 as cv
import numpy as np
import sys

img = cv.imread('samples/hello.png')

if img is None:
    sys.exit("file is not found")

cv.imshow("Display window: ",img)
k = cv.waitKey(0)

if k == ord("s"):
    cv.imwrite("samples/starry_night.png",img)