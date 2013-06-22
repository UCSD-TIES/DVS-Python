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

# Descriptive Variables for tweakable constants
LOWER_RED_RANGE = np.array((100,0,0))
UPPER_RED_RANGE = np.array((255,255,255))

ERODE_ITERATIONS = 1
DILATE_ITERATIONS = 1


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


############## Utility  Methods ###################
def draw_circles(storage, output):
    if DEBUG:
        print "We are in draw_circles"
    for i in range(0,len(storage)):
        radius = storage[i, 2]
        center = (storage[i, 0], storage[i, 1])
        if DEBUG:
            print "Radius: " + str(radius)
            print "Center: " + str(center)
        cv.Circle(output, center, radius, (0, 0, 255), 3, 8, 0)

############## Eye Class ###################

class Eye:
    """ This class has attributes :
      PIL  eyePhoto - a cropped photo of the eye
      tuple eyeRegion - a region that represents the exact location of the eye
      Pupil eyePupil - the eye's pupil
      region eyeSclera - the eye's sclera region
      point top - the keypoint of the eye located at the highest point at which
                  the top eyelid and the eyeball meet
      point bottom - the keypoint of the eye located at the lowest point at which
                     the lower eyelid and the eyeball meet
      point inner - the keypoint of the eye located nearest the tearduct
      point outer - the keypoint of the eye located on the outermost crease
                    of the eye
    """   

    def __init__(self, photo, region):
        """ Initializes eyePhoto and eyeRegion and calls findPupil, findSclera, and
            findKeypoints in an effort to populate the rest of the attributes
        """
        if DEBUG:
            print "We're here in eye's __init__"
            print "And our region is: " + str(region)
            print "This photo is a " + str(type(photo))
            #photo.show()
        # Initalize whole eye attributes to the values passed in
        self.eyePhoto = photo
        self.eyeRegion = region
        # Initialize the rest of the attributes to None so that they exist
        self.eyePupil = None
        self.eyeSclera = None
        self.top = None
        self.bottom = None
        self.inner = None
        self.outer = None
        # Set the rest of the attributes by finding them
        self.findPupil()
        self.findSclera()
        self.findKeypoints()

################# Utility Methods #########################################

    def findPupil(self):
        """ Detects a pupil in a photo of an eye and constructs a Pupil object

        Uses opencv libarary methods to detect a pupil. Algorithm found here:
        http://opencv-code.com/tutorials/pupil-detection-from-an-eye-image/
        Algorithm Overview:
            Load the source image.
            Invert it.
            Convert to grayscale.
            Convert to binary image by thresholding it.
            Find all blobs.
            Remove noise by filling holes in each blob.
            Get blob which is big enough and has round shape.
        Then initializes eyePupil by constructing a new pupil object. 
        Returns false if any errors are encountered

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error
        """
        # Load the source image and convert to cv mat
        eye = cv.GetMat(self.eyePhoto)
        if DEBUG:
            print "EYE: " + str(eye)
        if not eye:
            return False
        # Convert to a numpy array
        eyeArr = np.asarray(eye)

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

        smooth = cv.fromarray(dilate)
        cv.Smooth(cv.fromarray(dilate),smooth,cv.CV_GAUSSIAN,9,9)
        if DEBUG:
            cv.ShowImage("Smooth", smooth)
            cv.WaitKey(0)
            cv.DestroyWindow("Smooth")

        cv.Canny(smooth, smooth, 32, 2)
        if DEBUG:
            cv.ShowImage("Canny", smooth)
            cv.WaitKey(0)
            cv.DestroyWindow("Canny")

        storage = cv.CreateMat((self.eyePhoto).width, 1, cv.CV_32FC3)
        CIRCLE_MAX_RADIUS = self.eyePhoto.width
        cv.HoughCircles(smooth, storage, cv.CV_HOUGH_GRADIENT, CIRCLE_RESOLUTION_RATIO, CIRCLE_MIN_DISTANCE, 
            CIRCLE_THRESHOLD_1, CIRCLE_THRESHOLD_2, CIRCLE_MIN_RADIUS, CIRCLE_MAX_RADIUS)

        if DEBUG:
            print "STORAGE: " + str(storage)
            print np.asarray(storage)
            
        if storage.rows != 0 and storage.cols != 0:
            # NOTE: Each circle is stored as centerX, centerY, radius
            storage = np.asarray(storage)

            # Find the most centered circle
            centerX = self.eyePhoto.width / 2
            centerY = self.eyePhoto.height / 2
            if DEBUG:
                print "CenterX = " + str(centerX)
                print "CenterY = " + str(centerY)
            minDist = maxint
            minCircleIndex = -1
            for i in range(len(storage) - 1):
                #radius = storage[i, 0, 2]
                if DEBUG:
                    print "We're on circle elimination with i = "  + str(i)
                    print "MinDist = " + str(minDist)
                    print "minCircleIndex = " + str(minCircleIndex)
                x = storage[i, 0, 0]
                y = storage[i, 0, 1]
                dist = math.hypot(centerX-x, centerY-y)
                if dist < minDist:
                    minDist = dist
                    minCircleIndex = i

            if minCircleIndex != -1:
                finalCircle = np.array([[storage[minCircleIndex, 0, 0], storage[minCircleIndex, 0, 1],storage[minCircleIndex, 0, 2]]])
                if DEBUG:
                    print "Final Circle = " + str(finalCircle)
                    print "We're drawin some circles now"
                draw_circles(finalCircle,eye)

        if DEBUG:
            cv.ShowImage("Eye with Circles",eye)
            cv.WaitKey(0)
            cv.DestroyWindow("Eye with Circles")

        '''
        if DEBUG:
            print "--------------Pupil Extraction from blobs detected--------------"

        # Loop through the blobs to find one of the right shape/size
        for i in range(0, len(contours)):
            area = cv2.contourArea(contours[i])
            rect = cv2.boundingRect(contours[i])
            x = rect[0]
            y = rect[1]
            width = rect[2]
            height = rect[3]
            radius = width/2
            if DEBUG:
                print "Rect = " + str(rect)
                print "Area = " + str(area)
                print "First abs = " + str(abs(1-(width / height)))
                print "pi * r squared = " + str(math.pi * math.pow(radius,2))
            if area >= 30 and \
            abs(1-(width / height)) < .2 and \
            abs(1 - (area/((math.pi) * math.pow(radius, 2)))) <= .2:
                if DEBUG:
                    print "Found a circle here guys!!!!!!!!!!!!!"
                cv2.cv.circle(eye, cv.point(x + radius, y + radius, CV_RGB(255,0,0), 2))

        if DEBUG:
            cv.ShowImage("Pupil Circled", eye)
            cv.WaitKey(0)
            cv.DestroyWindow("Pupil Circled")
        '''

        # Do the various setting that needs to be done for the class structure
        region = None
        self.setPupil(region)
        return "findPupil successfully called"

    def findSclera(self):
        """ Detects a sclera in a photo of an eye and sets the sclera region

        Uses opencv libarary methods to detect a sclera. Then sets the sclera
        region. Returns false if any errors are encountered

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error.
        """
        # find sclera code goes here
        # Dummy code to make the var region exist
        region = None
        self.setSclera(region)
        return "findSclera successfully called"

    def findKeypoints(self):
        """ Detects the four main keypoints of an eye and sets their attributes

        Detects the four keypoints of an eye - top, bottom, inner, and outer.
        Sets the relevant attributes. Returns false if any errors are encountered.

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error.
        """
        # find top, bottom, inner, and outer logic goes here
        # Dummy code to make the vars exist
        topPoint = 0
        bottomPoint = 0
        innerPoint = 0
        outerPoint = 0
        self.setKeypoints( topPoint, bottomPoint, innerPoint, outerPoint)
        return "findKeyPoints successfully called."
        
#################### Getters ##################################

    def getEyePhoto(self):
        """ Returns a photo of the eye """
        return self.eyePhoto

    def getEyeRegion(self):
        """ Returns a region representing the eye """
        return self.eyeRegion

    def getPupil(self):
        """ Returns the Pupil object for this eye """
        return self.eyePupil

    def getSclera(self):
        """ Returns a region representing the sclera of this eye """
        return self.eyeSclera

    def getKeypoints(self):
        """ Returns a tuple (top, bottom, inner, outer) of the keypoints of this eye """
        return (self.top, self.bottom, self.inner, self.outer)

#################### Setters ##################################

    def setEyePhoto(self,photo):
        """ Sets eyePhoto to the photo passed in as argument"""
        self.eyePhoto = photo

    def setEyeRegion(self,region):
        """ Sets eyeRegion to the region passed in as argument"""
        self.eyeRegion = region

    def setPupil(self,region):
        """ Sets eyePupil to a new Pupil object constructed from
            the region passed in as argument"""
        self.eyePupil = Pupil(region)

    def setSclera(self,region):
        """ Sets eyeScelra to the region passed in as argument"""
        self.eyeSclera = region

    def setKeypoints(self,newTop, newBottom, newInner, newOuter):
        """ Sets all the keypoints according to those passed in as argument """
        self.top = newTop
        self.bottom = newBottom
        self.inner = newInner
        self.outer = newOuter




