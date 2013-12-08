import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint

img = cv2.imread('/Users/AndreyDenisevich/DVS-Python/src/pics/redeye1.PNG')

IplImage* imgHSV = cvCreateImage(cvGetSize(img), 8, 3);
cv2.cvtColor(img, imgHSV, CV_BGR2HSV);
IplImage* imgThreshed = cvCreateImage(cvGetSize(img), 8, 1);
cvInRangeS(imgHSV, cvScalar(20, 100, 100), cvScalar(0, 0, 255), imgThreshed);

img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)