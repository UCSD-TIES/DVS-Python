import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint

# Circle detection parameters
CIRCLE_RESOLUTION_RATIO = 1
# The minimum distance between circle centerpoints
CIRCLE_MIN_DISTANCE = 32
# I'm not exactly sure what the THRESHOLD ones do. See link for more info:
# http://www.adaptive-vision.com/en/technical_data/documentation/3.0/filters/FeatureDetection/cvHoughCircles.html
CIRCLE_THRESHOLD_1 = 10
# The accumulator threshold. The higher this is the less circles you get.
CIRCLE_THRESHOLD_2 = 2
CIRCLE_MIN_RADIUS = 10
CIRCLE_MAX_RADIUS = 500

# Circle drawing parameters
CIRCLE_COLOR = (0, 0, 255)
THICKNESS = 3
LINE_TYPE = 8
SHIFT = 0

# Note : change the directory of the photo
im = cv2.imread('/home/arvind/DVS-Python/src/pics/redeye1.PNG')  # im type: numpy.ndarray
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
## cv.ShowImage("Test", cv.fromarray(imgray)) # Grayscale Picture
ret,thresh = cv2.threshold(imgray,127,255,0)  # ret : type float. thresh: type :numpy.ndarray
## cv.ShowImage("Test", cv.fromarray(thresh))    # Binary Picture
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("Number of Contours Found: " + str(len(contours)))
cv2.drawContours(im,contours,-1,(0,255,0),0)  # Final argument for drawContours() : 0 = Outline, -1 = Fill-In
cv.ShowImage("All Contours", cv.fromarray(im))
cv.WaitKey(0)
cv.DestroyWindow("All Contours")

#finding center coordinates of photo
photoCenterX = len(im[0])/2
photoCenterY = len(im)/2
print("Photo's Center Coordinates: (" + str(photoCenterX) + ", " + str(photoCenterY) + ")" )

'''
## Looping through each 
for i in contours:
    cnt = contours[i]
    M = cv2.moments(cnt)
    centroid_x = int(M['m10']/M['m00'])
    centroid_y = int(M['m01']/M['m00'])
    print("Contour " + str(i + 1) + " : (" + str(centroid_x) + ", " + str(centroid_y) + ")" )
'''


