""" horizontalImg and verticalImg are pictures of the patient passed from the UI
"""
from HorizontalPhoto import *
from VerticalPhoto import *

class Patient:
    """ This class has attributes:
      HorizontalPhoto horizontal - an horizontal image object
      VerticalPhoto vertical - a vertical image object
    """
    def __init__(self, horizontalImg, verticalImg):
        """ Initialize the horizontal and vertical attributes by creating
            HorizontalPhoto and VerticalPhoto objects
        """
        horizontal = HorizontalPhoto(horizontalImg)
        vertical = VerticalPhoto(verticalImg)

    def analyzeEyes(self):
        """ Analyze all eye diseases and return the results """ 
        results = self.strabismus()
        results.append(self.astigmatism())
        results.append(self.cataracts())
        return results

    def strabismus(self):
        """ Analyze this patient for signs of strabismus """
        # strabismus detection logic goes here
        return "Strabismus detection called"

    def astigmatism(self):
        """ Analyze this patient for signs of astigmatism """
        # astigmatism logic goes here
        return "Astigmatism detection called"

    def cataracts(self):
        """ Analyze this patient for signs of cataracts """
        # cataracts logic goes here
        return "Cataracts detection called"




    
        
