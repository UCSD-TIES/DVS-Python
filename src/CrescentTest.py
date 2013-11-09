import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint

im = cv2.imread('/Users/AndreyDenisevich/DVS-Python/src/pics/redeye1.PNG')
print type(im)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv.ShowImage("Test", cv.fromarray(thresh))
cnt = contours[0]
len(cnt)
cv2.drawContours(im,contours,-1,(0,255,0),-1)
cv.ShowImage("Testing", cv.fromarray(im))
cv.WaitKey(0)
cv.DestroyWindow("Testing")
