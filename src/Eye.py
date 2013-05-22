""" A class to perform actions on a eye. A eye can get its own pupil and
    its own keypoints or sclera (depending on the algorithm)
"""

from Pupil import *
import cv

DEBUG = True

class Eye:
    """ This class has attributes :
      img eyePhoto - a cropped photo of the left eye
      region eyeRegion - a region that represents the exact location of the eye
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
            cv.ShowImage("Cropped Eye Photo", photo)
            cv.WaitKey(0)
            cv.DestroyWindow("Cropped Eye Photo")
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

        Uses opencv libarary methods to detect a pupil. Then initializes eyePupil
        by constructing a new pupil object. Returns false if any errors are encountered

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error
        """
        # find pupil code goes here
        # Dummy code to make the var region exist
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

