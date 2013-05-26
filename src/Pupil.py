""" A class to perform actions on an eye. A pupil can get its own center and its
own crescent region
"""

class Pupil:
  """ This class has attributes:
      region pupil - the region of the pupil
      point center - the center point of the pupil region
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
    crescent = None
    # Set the attributes initialized to None by finding them
    self.findCenter()
    self.findCrescent()


  def findCenter(self):
    """ Calculates the center of a pupil region and sets the centerpoint

    Calculates the center of a pupil from it's region and then sets the point
    center. Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    # calculate the centerpoint
    # make a dummy var so that centerpoint exists
    centerpoint = (0,0)
    self.setCenter(centerpoint)

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
    """ Returns a region representing the pupil """
    return self.pupil

  def getCenter(self):
    """ Returns a point representing the center of the pupil """
    return self.center

  def getCrescent(self):
    """ Returns a region representing the crescent """
    return self.crescent

#################### Setters ##################################

  def setPupilRegion(self,newRegion):
    """ Sets the pupil's region to the region passed in as argument """
    self.pupil = newRegion

  def setCenter(self,newCenter):
    """ Sets the pupil's center to the point passed in as arguments """
    self.center = newCenter

  def setCrescent(self,newCrescent):
    """ Sets the pupil's crescent to the region passed in as argument """
    self.crescent = newCrescent
