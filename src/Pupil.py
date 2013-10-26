""" A class to perform actions on an eye. A pupil can get its own center and its
own crescent region
"""

DEBUG = True

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
    self.findWhiteDot()

  def findWhiteDot(self):
    """ Detects a whiteDot within a pupil region.

    Uses opencv libarary methods to detect the white dot in the center of the 
    pupil caused by the reflection of the flash. Then initializes whiteDot
    to the region found and sets whiteDotCenter. Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    whiteDot = None
    self.setWhiteDot(whiteDot)
    if self.whiteDot != None:
      self.whiteDotCenter = (self.whiteDot[0], self.whiteDot[1])



  def findCrescent(self):
    """ Detects a crescent within a pupil region.

    Uses opencv libarary methods to detect a crescent. Then initializes crescent
    to the region found. Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    # crescent finding logic goes here
    # dummy variable
    crescentRegion = None
    self.setCrescent(crescentRegion)

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
