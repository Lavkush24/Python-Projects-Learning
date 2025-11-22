import cv2 as cv
import numpy as np

img = np.zeros((512,512,3),np.uint8)

cv.rectangle(img,(0,512),(512,0),(255,255,255),-1)

cv.circle(img,(256,226),40,(255,0,0),30)
cv.circle(img,(191,326),40,(0,255,0),30)
cv.circle(img,(321,326),40,(0,0,255),30)


font = cv.FONT_HERSHEY_DUPLEX
cv.putText(img,'OpenCV',(180,430),font,1.4,(0,0,0),7,cv.LINE_AA)


cv.imshow("Opencv Logo",img)
if cv.waitKey(0) == ord('s'):
    print("exit")