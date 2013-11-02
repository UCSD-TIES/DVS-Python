import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint

im = cv2.imread('C:\Users\Brian H. Nguyen\DVS-Python\src\pics\star.jpg')
print type(im)
#mim = cv.GetMat(im)
#imarr = np.asarray(mim)
#print type(imarr)
#print imarr
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
cv.ShowImage("Test", cv.fromarray(imgray))
cv.WaitKey(0)
cv.DestroyWindow("Test")
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
