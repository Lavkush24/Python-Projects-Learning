import cv2 as cv
import numpy as np

# Load the two images of apple and orange
A = cv.imread("samples/apple.jpg")
O = cv.imread("samples/orange.jpg")
assert A is not None,"check the path of the image. it exits?"
assert O is not None,"check the path of the image. it exits?"

A = cv.resize(A,(O.shape[1],O.shape[0]))

print("A shape:", A.shape)
print("O shape:", O.shape)



# Find the Gaussian Pyramids for apple and orange (in this particular example, number of levels is 6)
G = A.copy()
gpa = [G]
for i in range(6):
    G = cv.pyrDown(G)
    gpa.append(G)

G = O.copy()
gpo = [G]
for i in range(6):
    G = cv.pyrDown(G)
    gpo.append(G)


# From Gaussian Pyramids, find their Laplacian Pyramids
lpa = [gpa[5]]
for i in range(5,0,-1):
    GE = cv.pyrUp(gpa[i])
    GE = cv.resize(GE, (gpa[i-1].shape[1], gpa[i-1].shape[0]))
    L = cv.subtract(gpa[i-1],GE)
    lpa.append(L)

lpo = [gpo[5]]
for i in range(5,0,-1):
    GE = cv.pyrUp(gpo[i])
    GE = cv.resize(GE, (gpa[i-1].shape[1], gpa[i-1].shape[0]))
    L = cv.subtract(gpo[i-1],GE)
    lpo.append(L)

# Now join the left half of apple and right half of orange in each levels of Laplacian Pyramids

LS = []
for la,lo in zip(lpa,lpo):
    rows,cols,dpt = la.shape
    ls = np.hstack((la[:,0:cols//2], lo[:,cols//2:]))
    LS.append(ls)


# Finally from this joint image pyramids, reconstruct the original image.
ls_ = LS[0]
for i in range(1,6):
    ls_ = cv.pyrUp(ls_)
    ls_ = cv.resize(ls_, (LS[i].shape[1], LS[i].shape[0]))
    ls_ = cv.add(ls_, LS[i])


real = np.hstack((A[:,:cols//2],O[:,cols//2:]))
 
cv.imwrite('samples/Pyramid_blending2.jpg',ls_)
cv.imwrite('samples/Direct_blending.jpg',real)