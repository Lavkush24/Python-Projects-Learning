import cv2 as cv
import numpy as np


# if you want to color conbersion flags

# flags = [i for i in dir(cv) if  i.startswith('COLOR_')]
# print(flags)


cap = cv.VideoCapture(0)

while(1):
    _,frame = cap.read()

    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    lower_blue = np.array([110,100,100])
    upper_blue = np.array([130,255,255])

    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])

    mask_red = cv.inRange(hsv,lower_red,upper_red)
    mask_blue = cv.inRange(hsv,lower_blue,upper_blue)

    # combine mask 
    combined_mask = mask_red + mask_blue

    res = cv.bitwise_and(frame,frame,mask=combined_mask)

    cv.imshow('frame',frame)
    cv.imshow('Mask',combined_mask)
    cv.imshow('result',res)

    k = cv.waitKey(5) & 0xFF
    if k == ord('q'):
        break

cv.destroyAllWindows()


