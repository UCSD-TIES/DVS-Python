import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint

im = cv2.imread('/Users/AndreyDenisevich/DVS-Python/src/pics/redeye1.PNG')
print type(im)
imblur = cv2.blur(im,(3,3))
imgray = cv2.cvtColor(imblur,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv.ShowImage("Test", cv.fromarray(thresh))

max_area = 0
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > max_area:
        max_area = area
        best_cnt = cnt
        
#find centroids of best_cnt
M = cv2.moments(best_cnt)
cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
cv2.circle(imblur, (cx,cy),5,255,-1)

#show it, or exit on waitkey
#cv2.imshow('imblur',imblur)
cv2.imshow('thresh', thresh)
if cv2.waitKey(33) == 27:
    cv.DestroyAllWindows()

cnt = contours[0]
len(cnt)
cv2.drawContours(imblur,contours,-1,(0,255,0),-1)
cv2.circle(imblur, (cx,cy),5,255,-1)
cv.ShowImage("Contour Shading", cv.fromarray(imblur))
#cv.WaitKey(0)
#cv.DestroyWindow("Testing")
cv.WaitKey(0)
cv.DestroyAllWindows()