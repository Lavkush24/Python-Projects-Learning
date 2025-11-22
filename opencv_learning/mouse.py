import cv2 as cv
import numpy as np

img = np.zeros((512,512,3), np.uint8)

def draw_circle(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDBLCLK:
        cv.circle(img,(x,y),100,(255,0,0),-1)


drawing = False
mode = True
ix, iy = -1,-1
pos = False

def draw_rec_cir(event,x,y,flags,param):
    global ix,iy,drawing,mode,img

    if event == cv.EVENT_LBUTTONDOWN:
        ix,iy = x,y
        drawing = True
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            temp = img.copy()
            if mode == True:
                cv.rectangle(temp,(ix,iy),(x,y),(255,0,0),2)
            else:
                cv.circle(img,(x,y),5,(0,255,0),-1)
            cv.imshow('image', temp)
    elif event == cv.EVENT_LBUTTONUP:
        # jx,jy = x,y
        drawing = False
        if mode == True:
            cv.rectangle(img,(ix,iy),(x,y),(255,0,0),2)
        else:
            cv.circle(img,(x,y),5,(0,255,0),-1)
        

cv.namedWindow('image')
cv.setMouseCallback('image',draw_rec_cir)

while(1):
    cv.imshow('image',img)
    k = cv.waitKey(0) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == ord('q'):
        print("quit application...")
        break
cv.destroyAllWindows()