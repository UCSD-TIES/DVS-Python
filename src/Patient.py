""" horizontalImg and verticalImg are pictures of the patient passed from the UI
"""
from HorizontalPhoto import *
from VerticalPhoto import *
import math

DEBUG = False

class Patient:
    """ This class has attributes:
      HorizontalPhoto horizontal - an horizontal image object
      VerticalPhoto vertical - a vertical image object
    """
    def __init__(self, horizontalImg, horizontalPath, verticalImg, verticalPath):
        """ Initialize the horizontal and vertical attributes by creating
            HorizontalPhoto and VerticalPhoto objects
        """
        self.horizontal = HorizontalPhoto(horizontalImg, horizontalPath)
        self.vertical = VerticalPhoto(verticalImg, verticalPath)


#################### Getters ##################################

    def getHorizontal(self):
        return self.horizontal.facePhoto

    def getVertical(self):
        return self.vertical.facePhoto

    def getPupilRegion(self,horizontal, left):
        """ Returns the pupil region of the eye specified.

        Args:
            bool horizontal - if true, work with the horizontal photo
                                otherwise vertical
            bool left - if true get left eye else right

        Return:
            tuple - a tuple representing the circle found by pupil detection,
                    of the form (CenterX, CenterY, radius)
        """
        if horizontal:
            if left and self.horizontal.left != None and self.horizontal.left.eyePupil != None:
                return self.horizontal.left.eyePupil.pupil
            elif self.horizontal.right != None and self.horizontal.right.eyePupil != None:
                return self.horizontal.right.eyePupil.pupil
            else:
                # Default return
                return None
        else:
            if left and self.vertical.left != None and self.vertical.left.eyePupil != None:
                return self.vertical.left.eyePupil.pupil
            elif self.vertical.right != None and self.vertical.right.eyePupil != None:
                return self.vertical.right.eyePupil.pupil
            else:
                #Default Return
                return None
        

    def getEyeRegion(self,horizontal, left):
        """ Returns the region of the eye specified.

        Args:
            bool horizontal - if true, work with the horizontal photo
                                otherwise vertical
            bool left - if true get left eye else right

        Return:
            region - the region of the eye specified
        """
        if horizontal:
            if left and self.horizontal.left != None:
                return self.horizontal.left.eyeRegion
            elif self.horizontal.right != None:
                return self.horizontal.right.eyeRegion
            else:
                #Default Return
                return None
        else:
            if left and self.vertical.left != None:
                return self.vertical.left.eyeRegion
            elif self.vertical.right != None:
                return self.vertical.right.eyeRegion
            else:
                #Default Return
                return None

    def getEyePhoto(self,horizontal,left):
        """ Returns the photo of the eye specified.

        Args:
            bool horizontal - if true, work with the horizontal photo
                                otherwise vertical
            bool left - if true get left eye else right

        Return:
            region - the region of the eye specified
        """
        if horizontal:
            if left and self.horizontal.left != None:
                return self.horizontal.left.eyePhoto
            elif self.horizontal.right != None:
                return self.horizontal.right.eyePhoto
            else:
                #Default Return
                return None
        else:
            if left and self.vertical.left != None:
                return self.vertical.left.eyePhoto
            elif self.vertical.right != None:
                return self.vertical.right.eyePhoto
            else:
                #Default Return
                return None

#################### Setters ##################################



################## Disease Detection ##########################

    def analyzeEyes(self):
        """ Analyze all eye diseases and return the results """ 
        results = self.strabismus()
        results.append(self.astigmatism())
        results.append(self.cataracts())
        return results

    def strabismus(self):
        """

    //Declared variables used in the algorithm
        int lDistance;
        int rDistance;
        int dDistance;
        int dThreshold = ...;      //upperbound margin of error between whiteDot distances
        int lSlope;
        int rSlope;
        int dSlope;
        int sThreshhold = ...;
        int xDiff;
        int xThreshold = ...;


    //grabbing variables----------------------------------------------------------------------------
        mat leftDot = leftpupil.getWhiteDotCenter();
        mat rightDot = rightpupil.getWhiteDotCenter();
        dotLeftX = leftDot(0);
        dotLeftY = leftDot(1);
        dotRightX = rigthDot(0);
        dotLeftY = rightDot(1);

        mat leftPup = leftpupil.getCenter();
        mat rightPup = rightpupil.getCenter();
        pupLeftX = leftPup(0);
        pupLeftY = leftPup(0);
        pupRightX = rightPup(1);
        pupRightY = rightPup(1);


    //1.)  calculating difference of distances----------------------------------------------------------------
        //finding distances
        lDistance = math.sqrt(math.pow((dotLeftX - pupLeftX), 2) + math.pow((dotLeftY - pupLeftY), 2));
        rDistance = math.sqrt(math.pow((dotRightX - pupRightX), 2) + math.pow((dotLeftY - pupLeftY), 2));
        dDistance = math.abs(lDistance - rDistance);         

        //checks threshold distance
        if dDistance > dThreshold:                            //dThreshold should be near 0
            return true;

    //2.)  calculating difference of slope--------------------------------------------------------------------
        lSlope = div(pupLeftY, pupLeftX);
        rSlope = div(pupRightY, pupRightX);
        dSlope = math.abs(lSlope - rSlope);                   //sThreshold should be near 0

        //checks threshold slope "distance"
        if dSlope > sThreshhold:
            return true;


    //3.)  calculating difference of left x-axis------------------------------------------------------------------

        xDiff = math.abs(dotLeftX - dotRightX);

        //checks threshold x distance
        if xDiff > xThreshold:
            return true;


        """


        """ Analyze this patient for signs of strabismus

        Detect strabismus, also known as lazy eye, by calculating 
        difference between the relative position of the white dot 
        in the pupil and the outer edges of the pupil. If the dot
        is in a different location on one eye then the patient may 
        have strabismus.

        NOTE: This method will do nothing unless the patient has both
        photos, both leftEye and rightEye != None in each photo and 
        for each eye pupil and whiteDot != None

        Args:
            None

        Return:
            None

        NOTE: It might be useful to make the calculations for this
        apparent to the user so they can judge for themself how accurate
        the program's result is. Maybe by returning something?
        """
        # strabismus detection logic goes here
        return "Strabismus detection called"

    def astigmatism(self):
        """ Analyze this patient for signs of astigmatism """
        # astigmatism logic goes here
        return "Astigmatism detection called"

    def cataracts(self):
        """ Analyze this patient for signs of cataracts 

        Detect milky patches on the eye. If the patient has cataracts it will
        probably thrown pupil, whiteDot, crescent, and sclera detection off so
        it might be a good idea to work just from the original photo of the eye
        """
        # cataracts logic goes here
        return "Cataracts detection called"






    
        
