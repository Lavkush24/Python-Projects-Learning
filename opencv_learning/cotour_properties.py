import cv2 as cv
import numpy as np


img = cv.imread('samples/cut.jpg')
assert img is not None, "check if path is exists? "


grey_scale = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
ret, thresh = cv.threshold(grey_scale,127,255,0)

contours, hierarchy = cv.findContours(thresh,1,2)

cnt = contours[0]
M = cv.moments(cnt)
# print(M)

# for find the centroid 
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])

print(cx, cy)


# contoru area
area = cv.contourArea(cnt)
# contour perimeter
perimeter = cv.arcLength(cnt,True)


# contour approximation
