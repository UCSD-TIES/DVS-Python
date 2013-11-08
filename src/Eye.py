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
    for i in range(0,len(storage)):
        radius = storage[i, 2]
        center = (storage[i, 0], storage[i, 1])
        if DEBUG:
            print "Radius: " + str(radius)
            print "Center: " + str(center)
        cv.Circle(output, center, radius, CIRCLE_COLOR, 
            THICKNESS, LINE_TYPE, SHIFT)

############## Eye Class ###################

class Eye:
    """ This class has attributes :
      PIL  eyePhoto - a cropped photo of the eye
      tuple eyeRegion - a region that represents the exact location of the eye
      Pupil eyePupil - the eye's pupil
      
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
 
        # Set the rest of the attributes by finding them
        self.findPupil()


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
            print "We're here in findPupil()"
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
        cv.Smooth(cv.fromarray(dilate),smooth,
            cv.CV_GAUSSIAN,APERTURE_WIDTH,APERTURE_HEIGHT)
        if DEBUG:
            cv.ShowImage("Smooth", smooth)
            cv.WaitKey(0)
            cv.DestroyWindow("Smooth")

        cv.Canny(smooth, smooth, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2)
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
                dist = math.hypot(centerX - x, centerY - y)
                if dist < minDist:
                    minDist = dist
                    minCircleIndex = i

            finalCircle = None
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

        # Do the various setting that needs to be done for the class structure
        if finalCircle != None:
            # The pupil region is stored as a tuple : (centerXCoor, centerYCoor, radius)
            region = (finalCircle[0,0], finalCircle[0,1], finalCircle[0,2])
            self.setPupil(region)
            return True
        else:
            region = None
            self.setPupil(region)
            # A pupil was not found
            return False

    def pupilRemove(self, region):
        """ Crops the eye photo to show only the pupil
            and then returns it.

        Args:
            tuple region - the coordinates of the pupil circle in
            the form (centerX, centerY, radius)

        Return:
            photo  - TODO: I'm not sure of the type
        """
        # Converting to (topLeftX, topLeftY, width, height)
        if region[0]-region[2] < 0:
            topLeftX = 0
        else:
            topLeftX = region[0]-region[2]

        if region[1]-region[2] < 0:
            topLeftY = 0
        else:
            topLeftY = region[1]-region[2]

        if region[2] < 0:
            width = 0
        else:
            width = 2 * region[2]

        if region[2] < 0:
            height = 0
        else:
            height = 2 * region[2] 

        # These calculations will often give long (decimal) values. Pixel based coordinates
        # must be ints so we cast them
        crop = (np.int(topLeftX), np.int(topLeftY), np.int(width), np.int(height))
        if DEBUG:
            print "Region passed to pupil remove: " + str(region)
            print "And here's crop: " + str(crop)
            print "Before crop we have type: " + str(type(self.eyePhoto))
            print self.eyePhoto
            cv.ShowImage("We're cropping", self.eyePhoto)
            cv.WaitKey(0)
            cv.DestroyWindow("We're cropping")
        if crop[0] < 0:
            crop[0] = 0
        if crop[1] < 0:
            crop[1] = 0
        if crop[2] < 0:
            crop[2] = abs(crop[2])
        else:
            pupil = cv.GetSubRect(self.eyePhoto, crop)
            if DEBUG:
                print "After crop we have type: " + str(type(pupil))
                cv.ShowImage("Cropped", pupil)
                cv.WaitKey(0)
                cv.DestroyWindow("Cropped")
            return pupil
        return None

   
        
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
        pupilPhoto = self.pupilRemove(region)
        self.eyePupil = Pupil(pupilPhoto, region)

    


