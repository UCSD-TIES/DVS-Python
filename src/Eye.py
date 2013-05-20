""" A class to perform actions on a eye. A eye can get its own pupil and
    its own keypoints or sclera (depending on the algorithm)
"""

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
        # Initalize whole eye attributes to the values passed in
        eyePhoto = photo
        eyeRegion = region
        # Initialize the rest of the attributes to None so that they exist
        eyePupil = None
        eyeSclera = None
        top = None
        bottom = None
        inner = None
        outer = None
        # Set the rest of the attributes by finding them
        findPupil()
        findSclera()
        findKeypoints()

################# Utility Methods #########################################

    def findPupil():
        """ Detects a pupil in a photo of an eye and constructs a Pupil object

        Uses opencv libarary methods to detect a pupil. Then initializes eyePupil
        by constructing a new pupil object. Returns false if any errors are encountered

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error
        """
        # find pupil code goes here
        setPupil(region)
        return "findPupil successfully called"

    def findSclera():
        """ Detects a sclera in a photo of an eye and sets the sclera region

        Uses opencv libarary methods to detect a sclera. Then sets the sclera
        region. Returns false if any errors are encountered

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error.
        """
        # find sclera code goes here
        setSclera(region)
        return "findSclera successfully called"

    def findKeypoints():
        """ Detects the four main keypoints of an eye and sets their attributes

        Detects the four keypoints of an eye - top, bottom, inner, and outer.
        Sets the relevant attributes. Returns false if any errors are encountered.

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error.
        """
        # find top, bottom, inner, and outer logic goes here
        setKeypoints( topPoint, bottomPoint, innerPoint, outerPoint)
        return "findKeyPoints successfully called."
        
#################### Getters ##################################

    def getEyePhoto():
        """ Returns a photo of the eye """
        return eyePhoto

    def getEyeRegion():
        """ Returns a region representing the eye """
        return eyeRegion

    def getPupil():
        """ Returns the Pupil object for this eye """
        return eyePupil

    def getSclera():
        """ Returns a region representing the sclera of this eye """
        return eyeSclera

    def getKeypoints():
        """ Returns a tuple (top, bottom, inner, outer) of the keypoints of this eye """
        return (top, bottom, inner, outer)

#################### Setters ##################################

    def setEyePhoto(photo):
        """ Sets eyePhoto to the photo passed in as argument"""
        eyePhoto = photo

    def setEyeRegion(region):
        """ Sets eyeRegion to the region passed in as argument"""
        eyeRegion = region

    def setPupil(region):
        """ Sets eyePupil to a new Pupil object constructed from
            the region passed in as argument"""
        eyePupil = Pupil(region)

    def setSclera(region):
        """ Sets eyeScelra to the region passed in as argument"""
        eyeSclera = region

    def setKeypoints(newTop, newBottom, newInner, newOuter):
        """ Sets all the keypoints according to those passed in as argument """
        top = newTop
        bottom = newBottom
        inner = newInner
        outer = newOuter

