import cv2 as cv
import mediapipe as mp

cap = cv.VideoCapture(0)


mphands = mp.solutions.hands
hands = mphands.Hands()

while True:
    ret , frame = cap.read()

    imgRGB = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    result = hands.process(imgRGB)
    print(result)

    cv.imshow("image",frame)

    if cv.waitKey(1) == ord('q') :
        break
