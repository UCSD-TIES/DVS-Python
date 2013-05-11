""" A class to perform actions on a photo of a face
    This class has two child classes:
      HorizonalPhoto
      VerticalPhoto
"""
# NOTE: photoImg is a photo of a face

class FacePhoto:
""" This class has attributes:
        Eye left - the left eye object
        Eye right - the right eye object
"""

    #TODO: Error checking and raising is not accounted for in psudeoclasses

    def __init__(self, photoImg):
        """ Initializes eye objects

        Calls findEyes() to initialize the eye attributes.

        Args:
            photo photoImg - an image of a face

        Return:
            None
        """
        left = None
        right = None
        findEyes(photoImg)

    def findEyes(photoImg):
        """ Detects eyes in a photo and initializes relevant attributes

        Uses opencv libarary methods to detect a face and then detect the
        eyes in that face. If there are exactly two eye regions found it
        populates the region attributes. If a face is not found or exactly two
        eye regions are not found the method returns false.

        Args:
            photo photoImg - an image of a face

        Return:
            bool - True if there were no issues. False for any error
        """
        # eyeDetection.py logic goes here
        # if there's 2 regions
        #     set left and right region
        # else
        #     don't set the left and right regions
        return "getEyes successfully called"

    def getEyes():
        getLeftEye()
        getRightEye()
        # return tuple of eyes

    def setEyes(leftRegion, rightRegion):
        setLeftEye(leftRegion)
        setRightEye(rightRegion)
        return "setEyes successfully called"
        
    def setLeftEye(region):
        # calls eyeRemove code
        # sets or resets left.jpg, leftRegion
        return "setLeftEye successfully called"

    def setRightEye(region):
        # calls eyeRemove code 
        # sets or resets right.jpg, rightRegion
        return "setRightEye successfully called"

    def eyeRemove(region):
        # really takes in four points per region
        # place eye region here

    def getEyes():
        return "get eyes successfully called"

    def getLeftEye():
        # return all left eye vars
        return "getLeftEye successfully called"

    def getRightEye():
        # return all right eye vars
        return "getRightEye successfully called"
    
        
    
