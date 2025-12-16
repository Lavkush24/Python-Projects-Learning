import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

img = cv.imread("samples/sift_image.jpeg")
assert img is not None , "make sure path is exists ? "

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

fast = cv.FastFeatureDetector_create()

kp = fast.detect(gray,None)
img2 = cv.drawKeypoints(img,kp,None,color=(0,255,0))

print( "Threshold: {}".format(fast.getThreshold()) )
print( "nonmaxSuppression:{}".format(fast.getNonmaxSuppression()) )
print( "neighborhood: {}".format(fast.getType()) )
print( "Total Keypoints with nonmaxSuppression: {}".format(len(kp)) )

cv.imwrite('samples/fast_true.jpeg', img2)

fast.setNonmaxSuppression(0)
kp = fast.detect(img, None)
 
print( "Total Keypoints without nonmaxSuppression: {}".format(len(kp)) )
 
img3 = cv.drawKeypoints(img, kp, None, color=(255,0,0))
 
cv.imwrite('samples/fast_false.jpeg', img3)