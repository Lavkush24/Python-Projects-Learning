import cv2 as cv
import numpy as np


img = cv.imread("samples/roi.jpg")
assert img is not None, "check the path of image"

lower_reso = cv.pyrDown(img)
lower_reso2 = cv.pyrDown(lower_reso)
lower_reso3 = cv.pyrUp(lower_reso)


while(1):
    cv.imshow("actual image", img)
    cv.imshow("lower reso image" ,lower_reso)
    # cv.imshow("lower reso image 2" ,lower_reso2)
    cv.imshow("lower reso image 3" ,lower_reso3)

    if cv.waitKey(1) == ord('q'):
        break