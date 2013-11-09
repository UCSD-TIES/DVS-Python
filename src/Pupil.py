""" A class to perform actions on an eye. A pupil can get its own center and its
own crescent region
"""
from Eye import *
import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint


DEBUG = True

########## Descriptive Variables for tweakable constants ###############
### I just directly copied them from the Eye.py for now,
### Do we need to change the Circle radius constants?

# Threshold parameters
LOWER_WHITE_RANGE = np.array((100,100,100))
UPPER_WHITE_RANGE = np.array((255,255,255))

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


class Pupil:
  """ This class has attributes:
      PIL pupilPhoto - a cropped photo showing only the pupil
      tuple pupil - a tuple representing the circluar region of the pupil. The tuple
                    is formatted as such: (centerX, centerY, radius)
      tuple center - the center point of the pupil region formatted as (x,y)
      tuple whiteDot - a tuple representing the circular region of the white dot created 
                      in the center of the pupil by the light from the flash. The tuple is 
                      formatted as such: (centerX, centerY, radius)
      tuple whiteDotCenter - the center of the whiteDot formatted as (x,y)
      region crescent - the region of the pupil's crescent
  """

  def __init__(self, newPupilPhoto, pupilRegion):
    """ Initilaizes a pupil's region then calls findCenter and
        findCrescent() in an attempt to set the remaing attributes.
    """
    # Set the cropped photo of the pupil
    self.pupilPhoto = newPupilPhoto
    # Set the pupil region to the region passed in
    self.pupil = pupilRegion
    # Initialize the other attributes to None so that they exist
    self.center = None
    if pupilRegion != None:
      self.center = (pupilRegion[0], pupilRegion[1])
    self.whiteDot = None
    self.whiteDotCenter = None
    crescent = None
    # Set the attributes initialized to None by finding them
    self.findCrescent()
    #self.findWhiteDot()

  def findWhiteDot(self):
    ## The code here is based on findPupil() from Eye.py
    """ Detects a whiteDot within a pupil region.

    Uses opencv libarary methods to detect the white dot in the center of the 
    pupil caused by the reflection of the flash.

    Algorithm Overview:
        
            Load the source image.
            GrayScale
            Invert it.
            Convert to binary image by thresholding it.
            Find all blobs.
            Remove noise by filling holes in each blob.
            Get blob which is big enough and has round shape.

    Then initializes whiteDot to the region found and sets whiteDotCenter. 
    Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    # pupilPhoto is being stored as a mat so there is no need to convert it.
    #pupil = cv.GetMat(self.pupilPhoto)
    if DEBUG:
        print "Pupil: " + str(pupil)
    if not pupil:
        print "CANT FIND IMAGE!"
        return False
    
    # Convert to a numpy array
    pupilArr = np.asarray(pupil)
    
    # Grayscale Image
    gray = cv2.cvtColor(pupilArr, cv.CV_BGR2GRAY)
     
    # Erode and dilate the image to get rid of noise
    erode = cv2.erode(gray,None,iterations = ERODE_ITERATIONS)
    if DEBUG:
        cv.ShowImage("Erode", cv.fromarray(erode))
        cv.WaitKey(0)
        cv.DestroyWindow("Erode")
    dilate = cv2.dilate(erode,None,iterations = DILATE_ITERATIONS)
    if DEBUG:
        cv.ShowImage("Dilate", cv.fromarray(dilate))
        cv.WaitKey(0)
        cv.DestroyWindow("Dilate")
    
    
    ## Plz add convolution here!! 
    ## Don't forget to change the input to thresh if u do convolution
    
    
    # Find the white in the photo (to binary image)
    thresh = cv2.inRange(erode,LOWER_WHITE_RANGE,UPPER_WHITE_RANGE)
    if DEBUG:
        cv.ShowImage("Binary", cv.fromarray(thresh))
        cv.WaitKey(0)
        cv.DestroyWindow("Binary")
        
    # Invert the threshholded photo
    ## Question: Do we need the invert?? I left in here since was in findPupil...
    rows = len(thresh)
    for i in range(0,rows):
        for j in range(0,len(thresh[i])):
            thresh[i][j] = 255 - thresh[i][j]
    
    if DEBUG:
        cv.ShowImage("Inverted Thresh", cv.fromarray(thresh))
        cv.WaitKey(0)
        cv.DestroyWindow("Inverted Thresh")
    
    # Find countours in the image
    contours, hierarchy = cv2.findContours(dilate,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    # Draw the contours in white
    cv2.drawContours(dilate,contours,-1,(255,255,255),-1)
    if DEBUG:
        cv.ShowImage("Contours", cv.fromarray(dilate))
        cv.WaitKey(0)
        cv.DestroyWindow("Contours")

    smooth = cv.fromarray(dilate)
    cv.Smooth(cv.fromarray(dilate),smooth, cv.CV_GAUSSIAN,APERTURE_WIDTH,APERTURE_HEIGHT)
    if DEBUG:
        cv.ShowImage("Smooth", smooth)
        cv.WaitKey(0)
        cv.DestroyWindow("Smooth")
    
    ## Canny -> finds the edges in the image
    ## Reference : http://docs.opencv.org/modules/imgproc/doc/feature_detection.html
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
                draw_circles(finalCircle,pupil)
    if DEBUG:
        cv.ShowImage("Pupil with Circles",pupil)
        cv.WaitKey(0)
        cv.DestroyWindow("Pupil with Circles")
    
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
    
    
    '''
    Placeholder if 
    self.setWhiteDot(whiteDot)
    if self.whiteDot != None:
        self.whiteDotCenter = (self.whiteDot[0], self.whiteDot[1])
    '''



  def findCrescent(self):
    """ Detects a crescent within a pupil region.

    Uses opencv libarary methods to detect a crescent. Then initializes crescent
    to the region found. Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    if DEBUG:
        print "self.pupilPhoto is of type: " + str(type(self.pupilPhoto))
    # Currently self.pupilPhoto is stored as a cvmat so we need to convert to a 
    # numpy array before working with it.
    im = np.asarray(self.pupilPhoto)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # TODO Take away magic 127,255,0 numbers here and make pretty
    # Variables at the top
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if DEBUG:
        cv.ShowImage("Thresholded", cv.fromarray(thresh))
        cv.WaitKey(0)
        cv.DestroyWindow("Thresholded")
        cnt = contours[0]
        len(cnt)
        cv2.drawContours(im,contours,-1,(0,255,0),-1)
    if DEBUG:
        cv.ShowImage("Coutours", cv.fromarray(im))
        cv.WaitKey(0)
        cv.DestroyWindow("Contours")
    # find the area of the crescent
    # store the area of the crescent

#################### Getters ##################################

  def getPupilRegion(self):
    """ Returns a tuple representing the pupil """
    return self.pupil

  def getCenter(self):
    """ Returns a tuple representing the center of the pupil """
    return self.center

  def getWhiteDot(self):
    """ Returns a tuple representing the whiteDot """
    return self.whiteDot

  def getWhiteDotCenter(self):
    """ Returns a tuple representing the center of the whiteDot """
    return self.whiteDotCenter

  def getCrescent(self):
    """ Returns a region representing the crescent """
    return self.crescent

#################### Setters ##################################

  def setPupilRegion(self,newRegion):
    """ Sets the pupil's region to the tuple passed in as argument """

    self.pupil = newRegion

  def setCenter(self,newCenter):
    """ Sets the pupil's center to the tuple passed in as argument """
    self.center = newCenter

  def setwhiteDot(self,newRegion):
    """ Sets the whiteDot's region to the tuple passed in as argument """
    self.whiteDot = newRegion

  def setWhiteDotCenter(self,newCenter):
    """ Sets the whiteDot's center to the tuple passed in as argument """
    self.WhiteDotCenter = newCenter

  def setCrescent(self,newCrescent):
    """ Sets the pupil's crescent to the region passed in as argument """
    self.crescent = newCrescent
