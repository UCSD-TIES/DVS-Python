""" A class to perform actions on a eye. A eye can get its own pupil and
    its own keypoints or sclera (depending on the algorithm)
"""

from Pupil import *
import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint

DEBUG = True

########## Descriptive Variables for tweakable constants ###############

# Threshold parameters
LOWER_RED_RANGE = np.array((100,0,0))
UPPER_RED_RANGE = np.array((255,255,255))

# Erode and dilate parameters
ERODE_ITERATIONS = 1
DILATE_ITERATIONS = 1

# NOTE: tweaking any or all of these vars seems to only eliminate
#        erroneous circles, not move the position of the circles detected
# Circle detection parameters
CIRCLE_RESOLUTION_RATIO = 1
# The minimum distance between circle centerpoints
CIRCLE_MIN_DISTANCE = 32
# I'm not exactly sure what the THRESHOLD ones do. See link for more info:
# http://www.adaptive-vision.com/en/technical_data/documentation/3.0/filters/FeatureDetection/cvHoughCircles.html
# You will need to look at the above url on archive.org. The actual site no longer has that page.
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

# Smooth parameters
APERTURE_WIDTH = 9
APERTURE_HEIGHT = 9

# Canny parameters
CANNY_THRESHOLD_1 = 32
CANNY_THRESHOLD_2 = 2

############## Utility  Methods ###################
def draw_circles(storage, output):
    if DEBUG:
        print "We are in draw_circles"
    radius = storage[2]
    center = (storage[0], storage[1])
    if DEBUG:
        print "Radius: " + str(radius)
        print "Center: " + str(center)
    cv.Circle(output, center, radius, CIRCLE_COLOR, 
        THICKNESS, LINE_TYPE, SHIFT)



################# Utility Methods #########################################

def findPupil(eyePhoto):
        """ Detects a pupil in a photo of an eye and constructs a Pupil object

        Uses opencv libarary methods to detect a pupil. Algorithm found here:
        http://opencv-code.com/tutorials/pupil-detection-from-an-eye-image/
        Algorithm Overview:
            Load the source image.
            Threshold based on a range of red.
            Invert the photo.
            Erode and dilate to reduce noise.
            Find the contours.
            Smooth to improve canny edge detection.
            Canny edge detection.
            Hough circle detection.
            Choose the most central circle.
        Then initializes eyePupil by constructing a new pupil object. 
        Returns false if no pupil is found

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error
        """
        # Load the source image and convert to cv mat
        # eyePhoto is already stored as a mat. There is no need to convert
        #eye = cv.GetMat(eyePhoto)
        if DEBUG:
            print "We're here in findPupil()"
            print "EYE: " + str(eyePhoto)
            print "The type of eyePhoto is: " + str(type(eyePhoto))
        # Convert to a numpy array
        eyeArr = eyePhoto

        # Find the red in the photo
        thresh = cv2.inRange(eyeArr,LOWER_RED_RANGE,UPPER_RED_RANGE)
        if DEBUG:
            cv.ShowImage("Binary", cv.fromarray(thresh))
            cv.WaitKey(0)
            cv.DestroyWindow("Binary")


        # Invert the threshholded photo
        rows = len(thresh)
        for i in range(0,rows):
            for j in range(0,len(thresh[i])):
                thresh[i][j] = 255 - thresh[i][j]

        if DEBUG:
            cv.ShowImage("Inverted Thresh", cv.fromarray(thresh))
            cv.WaitKey(0)
            cv.DestroyWindow("Inverted Thresh")


        # Erode and dilate the image to get rid of noise
        erode = cv2.erode(thresh,None,iterations = ERODE_ITERATIONS)
        if DEBUG:
            cv.ShowImage("Erode", cv.fromarray(erode))
            cv.WaitKey(0)
            cv.DestroyWindow("Erode")
        dilate = cv2.dilate(erode,None,iterations = DILATE_ITERATIONS)
        if DEBUG:
            cv.ShowImage("Dilate", cv.fromarray(dilate))
            cv.WaitKey(0)
            cv.DestroyWindow("Dilate")

        # Find countours in the image
        contours, hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        # Draw the contours in white
        cv2.drawContours(dilate,contours,-1,(255,255,255),-1)
        if DEBUG:
            cv.ShowImage("Contours", cv.fromarray(dilate))
            cv.WaitKey(0)
            cv.DestroyWindow("Contours")

        print "type of dilate:  " + str(type(dilate))
        print "size of dilate:  " + str(dilate.size)
        
        cv2.imwrite("dilate.jpg", dilate   )
        big = bigContinWC(dilate)
        print big[0]

        
        eye = cv.fromarray(eyePhoto)
        draw_circles((big[0],big[1],3), eye)
        if DEBUG:
            cv.ShowImage("Biggest", eye)
            cv.WaitKey(0)
            cv.DestroyWindow("Biggest")
    

        
def bigContinWC(photo):
    '''
        Method to find the line in the photo with the largest
        continguous set of white pixels along that line.
        
        Will be optimized to use sampling (hopefully) so we don't 
        need to loop through every coordinate of the photo
        
        Expects photo to be a numpy.ndarray
        Return:
            stuff
    '''
    bigWC = -1
    bigX = -1
    bigY = -1
    lineX = -1
    lineY = -1
    for x in range(len(photo)):
        lineWC = 0
        wc =0
        tempCount = 0
        for y in range(len(photo[x])):
            pixel = photo[x][y]
            
            if pixel == 255:
                print "yes its white\n"
                tempCount = tempCount + 1
                print tempCount
            elif tempCount > wc:
                print "black"
                wc = tempCount
                lineY = y-wc
                lineX = x
                tempCount =0
        lineWC = wc
        if lineWC > bigWC:
            bigWC = lineWC
            bigX = lineX
            bigY = lineY
    return (bigX, bigY, bigWC)
                
     

        
#new code ladies and gentlemen
im = cv2.imread('C:/Users/Shannon/Documents/GitHub/DVS-Python/src/eyePhoto.png')
print type(im)
findPupil(im)

