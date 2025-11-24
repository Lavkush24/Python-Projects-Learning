import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt


Blue = [255,0,0]

img = cv.imread('samples/roi.jpg')
assert img is not None, "file could not read, check the os.paht.exits()"

# accessing the modify pixel values 
# we access pixels values by row and column coordinates

px = img[100,100]  
print(px)  # if it print values B,G,R manner

# excess red values only
red = img[100,100,2]
print(red)

# modify 
img[100,100] = [0,0,0]
print(img[100,100])






# Image properties
print(img.shape)  # it give tupple of row,column,channel(if image has color)

# total pixel 
print(img.size)



# # image ROI
# ball = img[240:275,276:324]
# img[76:111,334:382] = ball


# #splitting ans merging of the images

# b,g,r = cv.split(img)
# # img = cv.merge((b,g,r))

# # img[:,:,2] = 0

# img = cv.merge((b,g,r))





# Making border of the images 
replicate = cv.copyMakeBorder(img,10,10,10,10,cv.BORDER_REPLICATE)
reflect = cv.copyMakeBorder(img,10,10,10,10,cv.BORDER_REFLECT)
reflect101 = cv.copyMakeBorder(img,10,10,10,10,cv.BORDER_REFLECT_101)
wrap = cv.copyMakeBorder(img,10,10,10,10,cv.BORDER_WRAP)
constant= cv.copyMakeBorder(img,10,10,10,10,cv.BORDER_CONSTANT,value=Blue)

plt.subplot(231),plt.imshow(img,'gray'),plt.title('ORIGINAL')
plt.subplot(232),plt.imshow(replicate,'gray'),plt.title('REPLICATE')
plt.subplot(233),plt.imshow(reflect,'gray'),plt.title('REFLECT')
plt.subplot(234),plt.imshow(reflect101,'gray'),plt.title('REFLECT_101')
plt.subplot(235),plt.imshow(wrap,'gray'),plt.title('WRAP')
plt.subplot(236),plt.imshow(constant,'gray'),plt.title('CONSTANT')

plt.show()

cv.imshow("image",img)
cv.waitKey(0)

cv.destroyAllWindows()