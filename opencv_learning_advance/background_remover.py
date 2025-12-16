import cv2 as cv
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by OpenCV. You can process both videos and images.')


parser.add_argument('--input',type=str,help='path to the video and image sequence',default='samples/Megamind.avi')
parser.add_argument('--algo',type=str,help='bg substraction method',default='MOG2')
args = parser.parse_args()

if args.algo == 'MOG2':
    backsub = cv.createBackgroundSubtractorMOG2()
else:
    backsub = cv.createBackgroundSubtractorKNN()

capture = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
if not capture.isOpened():
    print('unable to open'+ ' ' + args.input)
    exit(0)

while True:
    ret,frame = capture.read()
    if frame is None:
        break

    fgmask = backsub.apply(frame)

    cv.rectangle(frame,(10,2),(100,20),(255,255,255),-1)
    cv.putText(frame,str(capture.get(cv.CAP_PROP_POS_FRAMES)),(15,15),cv.FONT_HERSHEY_COMPLEX,0.5,(0,0,0))


    cv.imshow("Frame", frame)
    cv.imshow("FG Mask",fgmask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break