# Day 1 (22 Nov 2025)
- ## learning the opencv with experiments 
    - creating a virtual enviroment .python_exp 
    - activate source .python_exp/bin/activate  
    - crete a start file start.py to test
        - the first to read and write operation  and show operation
            - read using cv.imread("path of the file")
            - write using cv.imwrite(name as you want to save,readed image)
            - to show cv.imshow(message to dashboard,readed image)

    - create video.py for interection with video 
        - create instace for read video cap
            - cv.videocapture() pass the path of video or 0 to n number for camera access in case multiple camera otherwise 0
        - also create write instance out and fourcc
            - fourcc = cv.VideoWriter_fourcc(*'XVID') it define video codec
            - out = cv.VideoWriter(path to save and name,fourcc,frame per sec, (sizel,sizew))
        - check if camera access is allowed
        - run loop read ret, frame
            - ret, frame = cap.read()
            - check ret is define it return true if read
        - do some operation on the frame 
        - show the frame 
            - cv.imshow('name', frame)
        - write using out.write(frame)
        - close all instaces out and cap and distroyallwindows()

    - next learn cursor as paint
        - learn about events and setmousecallbacK() 
        - make mouse.py 
        - in which define function for the draw circle and rectable filled and unfilled both type 
    - next learn about the tracker
        - cv.createTracker(parameter,image name,min,max,function)
        - excess trigger with cv.getTrackBarPos(parameter,image name)


    - (PRACTICE) create two application 
        - one using setmousecallback() --- create rectange and circle by triggering the particular command

        - second add the freature of changing color of paing in above 

# DAY 2 (23 Nov 2025)
- ## Learning OpenCV Core Operations
    - acccessing pixcel values and image properties and region of interest(ROI) and split and merge image
    