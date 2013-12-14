import cv2.cv as cv
import cv2
import time
from PIL import Image
import sys
from Eye import *
import PIL
import os

""" A class to perform actions on a photo of a face
    This class has two child classes:
      HorizonalPhoto
      VerticalPhoto
"""
# NOTE: photoImg is a photo of a face

DEBUG = False


class FacePhoto():
    """ This class has attributes:
        IplImage facePhoto - a photo of the whole face
        string path - the path to the photo of the whole face
        Eye left - the left eye object
        Eye right - the right eye object
    """

    #TODO: Error checking and raising is not accounted for in psudeoclasses

    def __init__(self, photoImg, photoPath):
        """ Initializes eye objects

        Calls findEyes() to initialize the eye attributes.

        Args:
            photo photoImg - an image of a face

        Return:
            None
        """
        # Initialize the face photo to the value passed in
        self.facePhoto = photoImg
        self.path = photoPath
        # Initialize the other attributes to None so that they exist
        self.left = None
        self.right = None
        if DEBUG:
            print "In the facePhoto __init__"
        # Set attributes intialized to None by finding them.
        self.findEyes()

################# Utility Methods ######################

    def findEyes(self):
        """ Detects eyes in a photo and initializes relevant attributes

        Uses opencv libarary methods to detect a face and then detect the
        eyes in that face. If there are exactly two eye regions found it
        populates the region attributes. If a face is not found or exactly two
        eye regions are not found the method returns false.

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error
        """
        
        #imcolor = cv.LoadImage(self.path)
        imcolor = self.facePhoto

        #Path setups
        
        cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
        cwd += "/opencv/haarcascades/"
        frontalface = cwd + "haarcascade_frontalface_default.xml"
        eye = cwd + "haarcascade_eye.xml"

        #NOTE: You may need to modify this path to point to the dir with your cascades
        faceCascade = cv.Load(frontalface)
        eyeCascade = cv.Load(eye)
        

        # NOTE: You may need to modify this path to point to the dir with this file on your comp
        haarEyes = cv.Load(eye)
        storage = cv.CreateMemStorage()
        detectedEyes = cv.HaarDetectObjects(imcolor,haarEyes,storage)

        if DEBUG:
            print "detectedEyes = " + str(detectedEyes)

        if len(detectedEyes) == 2:
            if DEBUG:
                # TODO: Draw the rectangle here
                cv.Rectangle(imcolor,(detectedEyes[0][0][0], detectedEyes[0][0][1]), 
                    (detectedEyes[0][0][0] + detectedEyes[0][0][2], 
                    detectedEyes[0][0][1] + detectedEyes[0][0][3]),cv.RGB(155,155,200),2)
                cv.Rectangle(imcolor,(detectedEyes[1][0][0], detectedEyes[1][0][1]), 
                    (detectedEyes[1][0][0] + detectedEyes[1][0][2], 
                    detectedEyes[1][0][1] + detectedEyes[1][0][3]),cv.RGB(155,155,200),2)
                cv.ShowImage("Face with eyes",imcolor)
                cv.WaitKey(0)
                cv.DestroyWindow("Face with eyes")
            left = (detectedEyes[0][0][0], detectedEyes[0][0][1], 
                    detectedEyes[0][0][0] + detectedEyes[0][0][2], 
                    detectedEyes[0][0][1] + detectedEyes[0][0][3])
            right = (detectedEyes[1][0][0], detectedEyes[1][0][1], 
                    detectedEyes[1][0][0] + detectedEyes[1][0][2], 
                    detectedEyes[1][0][1] + detectedEyes[1][0][3])
            if DEBUG:
                print "left: " + str(left)
                print "right: " + str(right)
            self.setEyes(left, right)
            return True
        if DEBUG:
            print "Found more or less than 2 eyes, returning false"
        return False

    
    def eyeRemove(self, region):
        """ Crops an eye from the facePhoto and returns it as a seperate photo

        This method takes in a region which is interpreted to be a region representing
        and eye and crops the eye out. It then returns the cropped photo

        Args:
            region region - a region representing the eye

        Return:
            photo eyePhoto - a photo of just the eye
        """
        # really takes in four points per region
        crop = (region[0],region[1], region[2] - region[0], region[3] - region[1])
        if DEBUG:
            print "Region passed to eye remove: " + str(region)
            print "And here's crop: " + str(crop)
            print "Before crop we have type: " + str(type(self.facePhoto))
            print self.facePhoto
            cv.ShowImage("We're cropping", self.facePhoto)
            cv.WaitKey(0)
            cv.DestroyWindow("We're cropping")
        eye = cv.GetSubRect(self.facePhoto, crop)
        #eye = face.crop(region)
        if DEBUG:
            print "After crop we have type: " + str(type(eye))
            cv.ShowImage("Cropped", eye)
            cv.WaitKey(0)
            cv.DestroyWindow("Cropped")
        return eye

##################### Getters ############################

    def getEyes(self):
        """ Returns a tuple of the left and right eye objects """
        leftEye = self.getLeftEye()
        rightEye = self.getRightEye()
        return (leftEye, rightEye)

    def getLeftEye(self):
        """ Returns the left eye object """
        return self.left

    def getRightEye():
        """ Returns the right eye object """
        return self.right

##################### Setters ############################

    def setEyes(self, leftRegion, rightRegion):
        """ Sets or resets both eye objects """
        if DEBUG:
            print "We're here in setEyes now"
            print "leftregion: " + str(leftRegion)
            print "rightRegion: " + str(rightRegion)
        self.setLeftEye(leftRegion)
        self.setRightEye(rightRegion)
        return "setEyes successfully called"
        
    def setLeftEye(self,region):
        """ Constructs a new Eye object and stores it in left """
        if DEBUG:
            print "And we're setting the left eye now"
        # Crop out a photo of the eye to pass the Eye constructor
        left_eyePhoto = self.eyeRemove(region)
        # Constructs the left eye
        self.left = Eye(left_eyePhoto, region)
        return "setLeftEye successfully called"

    def setRightEye(self,region):
        """ Constructs a new Eye object and stores it in right """
        if DEBUG:
            print "And we're setting the right eye now"
        # Crop out a photo of the eye to pass the Eye constructor
        right_eyePhoto = self.eyeRemove(region)
        # Constructs the right eye
        self.right = Eye(right_eyePhoto, region)
        return "setRightEye successfully called"



    
        
    
