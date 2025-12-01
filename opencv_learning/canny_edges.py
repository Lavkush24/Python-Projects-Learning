import cv2 as cv 
import numpy as np
from matplotlib import pyplot as plt

def nothing(x):
    pass 

img = cv.imread('samples/roi.jpg',cv.IMREAD_GRAYSCALE)
assert img is not None, "image is not found ? check the path is exists"


cv.namedWindow("tracker")
cv.createTrackbar("thres_min","tracker",0,1000,nothing)
cv.createTrackbar("thres_max","tracker",0,1000,nothing)


while(1):
    min_thres = cv.getTrackbarPos("thres_min","tracker")
    max_thres = cv.getTrackbarPos("thres_max","tracker")

    img_edges = cv.Canny(img,min_thres,max_thres)
    cv.imshow("edges detected",img_edges)

    key = cv.waitKey(1)
    if key == ord('q'):
        break

cv.destroyAllWindows()
