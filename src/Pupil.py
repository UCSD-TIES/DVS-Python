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
    pupil = pupilRegion
    center = None
    crescent = None
    findCenter()
    findCrescent()


  def findCenter():
    """ Calculates the center of a pupil region and sets the centerpoint

    Calculates the center of a pupil from it's region and then sets the point
    center. Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    # calculate the centerpoint
    setCenter(centerpoint)

  def findCrescent():
    """ Detects a crescent within a pupil region.

    Uses opencv libarary methods to detect a crescent. Then initializes crescent
    to the region found. Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    # crescent finding logic goes here
    setCrescent(crescentRegion)

#################### Getters ##################################

    def getPupilRegion():
      """ Returns a region representing the pupil """
      return pupil

    def getCenter():
      """ Returns a point representing the center of the pupil """
      return center

    def getCrescent():
      """ Returns a region representing the crescent """
      return crescent

#################### Setters ##################################

    def setPupilRegion(newRegion):
      """ Sets the pupil's region to the region passed in as argument """
      pupil = newRegion

    def setCenter(newCenter):
      """ Sets the pupil's center to the point passed in as arguments """
      center = newCenter

    def setCrescent(newCrescent):
      """ Sets the pupil's crescent to the region passed in as argument """
      crescent = newCrescent

      
      
    
