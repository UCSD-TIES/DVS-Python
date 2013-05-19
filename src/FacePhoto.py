""" A class to perform actions on a photo of a face
    This class has two child classes:
      HorizonalPhoto
      VerticalPhoto
"""
# NOTE: photoImg is a photo of a face

class FacePhoto:
    """ This class has attributes:
        photo facePhoto - a photo of the whole face
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
        # Initialize the face photo to the value passed in
        facePhoto = photoImg
        # Initialize the other attributes to None so that they exist
        left = None
        right = None
        # Set attributes intialized to None by finding them.
        findEyes(photoImg)

################# Utility Methods ######################

    def findEyes():
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
        # eyeDetection.py logic goes here
        # if there's 2 regions
        #     construct left and right eye objects; set left and right
        # else
        #     don't set the left and right attributes or construct Eye objects
        return "findEyes successfully called"

    
    def eyeRemove(region):
        """ Crops an eye from the facePhoto and returns it as a seperate photo

        This method takes in a region which is interpreted to be a region representing
        and eye and crops the eye out. It then returns the cropped photo

        Args:
            region region - a region representing the eye

        Return:
            photo eyePhoto - a photo of just the eye
        """
        # really takes in four points per region
        # place eye region here
        eye = cv2.cv.GetSubRect(image, region)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return "eyeRemove successfully called"

##################### Getters ############################

    def getEyes():
        """ Returns a tuple of the left and right eye objects """
        leftEye = getLeftEye()
        rightEye = getRightEye()
        return (leftEye, rightEye)

    def getLeftEye():
        """ Returns the left eye object """
        return left

    def getRightEye():
        """ Returns the right eye object """
        return right

##################### Setters ############################

    def setEyes(leftRegion, rightRegion):
        """ Sets or resets both eye objects """
        setLeftEye(leftRegion)
        setRightEye(rightRegion)
        return "setEyes successfully called"
        
    def setLeftEye(region):
        """ Constructs a new Eye object and stores it in left """
        # Crop out a photo of the eye to pass the Eye constructor
        left_eyePhoto = eyeRemove(region)
        # Constructs the left eye
        left = Eye(eyePhoto, region)
        return "setLeftEye successfully called"

    def setRightEye(region):
        """ Constructs a new Eye object and stores it in right """
        # Crop out a photo of the eye to pass the Eye constructor
        right_eyePhoto = eyeRemove(region)
        # Constructs the right eye
        right = Eye(eyePhoto, region)
        return "setRightEye successfully called"



    
        
    
