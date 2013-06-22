""" A class to perform actions on an eye. A pupil can get its own center and its
own crescent region
"""

class Pupil:
  """ This class has attributes:
      tuple pupil - a tuple representing the circluar region of the pupil. The tuple
                    is formatted as such: (centerX, centerY, radius)
      tuple center - the center point of the pupil region formatted as (x,y)
      region crescent - the region of the pupil's crescent
  """

  def __init__(self, pupilRegion):
    """ Initilaizes a pupil's region then calls findCenter and
        findCrescent() in an attempt to set the remaing attributes.
    """
    # Set the pupil region to the region passed in
    self.pupil = pupilRegion
    # Initialize the other attributes to None so that they exist
    self.center = None
    if pupilRegion != None:
      self.center = (pupilRegion[0], pupilRegion[1])
    crescent = None
    # Set the attributes initialized to None by finding them
    self.findCrescent()


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

  def getCrescent(self):
    """ Returns a region representing the crescent """
    return self.crescent

#################### Setters ##################################

  def setPupilRegion(self,newRegion):
    """ Sets the pupil's region to the tuple passed in as argument """
    self.pupil = newRegion

  def setCenter(self,newCenter):
    """ Sets the pupil's center to the tuple passed in as arguments """
    self.center = newCenter

  def setCrescent(self,newCrescent):
    """ Sets the pupil's crescent to the region passed in as argument """
    self.crescent = newCrescent
