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
    
    - create color tracking application



# DAY 3 (24 Nov 2025)
- ## Geomatric transformation   
    - Learned function  
        - cv.warpAffine() take input 2*3 matrix
        - cv.warpPerspective() take input 3*3 matrix transformation     

    - scaling   (To resize the image)
        - cv.resize(img,shape,fx,fy(if shape none),interpolation=cv.inter_cubic(many other))

    - Translation ( shifting of object location)
        - create a matrix eg if you want shift (100,50)  np.float32([[1,0,100],[0,1,50]])
        - cv.wrapAffine(img,Matrix,(cols(width),rows(height)))

    - Rotation
        - for rotation similar to translation i need to change only the matrix that i create
        - i need specal matrix by using getRotationMatrix2D((center),degeree,scaling)

    - affineTransform and perspective Transform
        - getAffineTransform(pt1,pt2)  parllel remain parallel
        - getPerspectiveTransform(pt1,pt2) staright remain straight line
        

# DAY 4 (28 Nov 2025)
- ## Image Filtering 
    - cv.filter2D(img, ,filter)
    - we create filter as kernel of matrix that apply on each pixel of the  image

    - ### image bluring
    - 1. Averaging 2. Gaussian Blurring 3. Bilateral filtering
    - 1. cv.blur(img,(5,5)) or cv.boxFilter()
    - 2. cv.gaussianBlur(img,(5,5),0)
    - 3. cv.medianBlur(img,)

# DAY 5 (1 Dec 2025)
- ## Morphological transformation
    - cv.erode(img,kernel,iteration=1) it siply work like the soil erosion. erode the boundry of the images by moving like the 2d convolution.
    - cv.dilate(img,kernel,iteration=1) just opposite of the erosion as it increase the white region
    - cv.morphologyEx(img,cv.MORPH_OPEN,kernel) erosion followed by dilation
    - cv.morphologyEx(img,cv.MORPH_CLOSE,kernel) dilation followed by erosion
    and some other features for  opearation similar to these operations

- Canny edges detection 
    - applciatioin where i can control the min and max threshold values so see how they affect the image edge detection



# DAY 6 (12 Dec 2025)
- ## Image pyramids
    - image pyramid is the stack of high resolutin to low resolution images stack . the stack is look like pyramid that why it is known as the image pyramid.
        - have two type 1. gaussian pyramid  2. Laplacian pyramid
        #### two functions to access them 1. cv.pyrUp() 2. cv.pyrDown()


# DAY 7 (13 Dec 2025)
- ## Contour Features
    - use full tool for object detection and recognition it detect the same colout around the corner or the boundry 
    - function use is cv.findcontours() it take three atrgument i. image  ii. contour retrivel mode iii. contour approximation method
    - its better to apply threshold and canny edge detection
- ## how to draw contour
    - function use is cv.drawContours(img,contour passed as pythonlist , color(0,255,0), thickness)
- ## Contour Properties
    - Moments it give all values like area, perimeter , and mometns value by using moment()