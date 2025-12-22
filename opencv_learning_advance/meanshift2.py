import cv2 as cv
import numpy as np

capture = cv.VideoCapture('samples/2053100-uhd_3840_2160_30fps.mp4')

# to track we need to define the initial location
ret, frame = capture.read()

# intital position
x,y,w,h = 600,500,400,300
track_window = (x,y,w,h)

# setup roi(reason of interest) for tracking
roi = frame[y: y+h,x: x+w]
hsv_roi = cv.cvtColor(roi,cv.COLOR_BGR2HSV)

mask = cv.inRange(hsv_roi,np.array((0.,60.,32.)),np.array((180.,255.,255)))
roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
cv.normalize(roi_hist,roi_hist,0,255,cv.NORM_MINMAX)

# setup termination of criteria 
term_crit = ( cv.TermCriteria_EPS | cv.TermCriteria_COUNT,10,1 )
cv.imshow("roi",roi)

while(1):
    ret,frame = capture.read()

    if ret == True:
        # frame = cv.resize(frame,(640,480))
        hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)
        dist = cv.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        ret, track_window = cv.meanShift(dist,track_window,term_crit)

        x,y,w,h = track_window
        final_img = cv.rectangle(frame,(x,y),(x+w,y+h),255,3)

        cv.imshow("dist",dist)
        cv.imshow("final_img",final_img)
        k = cv.waitKey(30) & 0xFF
        if k == ord('q'):
            break
    else:
        break