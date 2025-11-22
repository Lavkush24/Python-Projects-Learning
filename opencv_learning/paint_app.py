import cv2 as cv
import numpy as np

drawing = False
mode = True
x,y = -1,-1
pen_color = (225,225,225)


def nothing(x):
    pass

def paint(event,x,y,flags,params):
    global x1,y1,drawing,img2,temp,mode,pen_color

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        x1,y1 = x,y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            temp = img2.copy()
            if mode == True:
                cv.rectangle(temp,(x1,y1),(x,y),pen_color,2)
            else:
                cv.circle(img2,(x,y),5,pen_color,-1)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            cv.rectangle(img2,(x1,y1),(x,y),pen_color,2)
        else:
            cv.circle(img2,(x,y),5,pen_color,-1)


# img = np.zeros((512,512),np.uint8)
img2 = np.zeros((768,1024,3),np.uint8)
temp = img2.copy()
cv.namedWindow('control')

cv.createTrackbar('R','control',0,255,nothing)
cv.createTrackbar('G','control',0,255,nothing)
cv.createTrackbar('B','control',0,255,nothing)

switch = '0: OFF\n1:ON'
cv.createTrackbar(switch,'control',0,1,nothing)

cv.setMouseCallback('control',paint)

while(1):
    if drawing:
        cv.imshow('control', temp)
    else:
        cv.imshow('control', img2)

    k = cv.waitKey(1) & 0xFF

    if k == ord('m'):
        mode = not mode
    elif k == ord('q'):
        print("quit application")
        break

    r = cv.getTrackbarPos('R','control')
    g = cv.getTrackbarPos('G','control')
    b = cv.getTrackbarPos('B','control')
    s = cv.getTrackbarPos(switch,'control')

    if s == 1:
        pen_color = (b,g,r)

cv.destroyAllWindows()

    