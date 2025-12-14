import cv2 as cv
import numpy as np

img = cv.imread("samples/temple.jpeg")
assert img is not None, "make sure path is exists?"

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

sift = cv.SIFT_create()
kp = sift.detect(gray,None)

img = cv.drawKeypoints(gray,kp,img)
cv.imwrite("samples/sift_image.jpeg", img)
img=cv.drawKeypoints(gray,kp,img,flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.imwrite('sift_keypoints.jpg',img)