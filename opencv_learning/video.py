import cv2 as cv


cap = cv.VideoCapture(0)

fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('samples/output.avi',fourcc, 20.0,(640,480))

if not cap.isOpened():
    print("cannot open camera")
    exit()

while True:
    ret,frame = cap.read()

    if not ret:
        print("cannot receive frame. Existing... ")
        break

    # ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT, 320)
    # ret = cap.set(cv.CAP_PROP_FRAME_WIDTH,240)

    # gray =  cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    frame = cv.flip(frame,0)

    out.write(frame)

    cv.imshow('frame',frame)
    if cv.waitKey(0) == ord('q'):
        break

cap.release()
out.release()
cv.destroyAllWindows()
