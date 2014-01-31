""" horizontalImg and verticalImg are pictures of the patient passed from the UI
"""
from HorizontalPhoto import *
from VerticalPhoto import *

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

    def getAllPupils(self):
        """ Returns a tuple of Pupil objects in the following order:
        (horizLeft,horizRight,vertLeft,vertRight)

        TODO: This function is crap obj oriented design and has no checks
        """
        return (self.horizontal.left.eyePupil,self.horizontal.right.eyePupil,
            self.vertical.left.eyePupil, self.vertical.right.eyePupil)

#################### Setters ##################################



################## Disease Detection ##########################

    def analyzeEyes(self,threshold):
        """ Analyze all eye diseases and return the results 

        Args:
            float threshold - the threshold of refractive error 
                              above which we will give a referral

        Return:
            TODO: dict????
        """ 
        results = self.strabismus()
        results = results + " " + self.astigmatism(threshold)
        results = results + " " + self.cataracts()
        return results

    def strabismus(self):
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

            Pseudo Code - by David and Arvind            
                                    
            1. Detect face, eyes, then pupil
            2. Detect White dot in both pupils
            3. Calculate the distance from Pupil-center to White-dot-center for both Pupils
            4. Calculate the angle of Pupil-center to White-dot-center line [ using numpy.arctan on (y component of distance) / (x component of distance) ]
            5. Compare the two vectors from both pupils [ compare distances & angles ] 
                1. For a healthy eye, the angles should be same (looking in the same direction)         
                2. We could also measure the severeness of the off pupil-center and white-dot-center offset (healthy eye would have both in center)
                3. If the White dot is not found (within the Pupil), severe Strabismus

        NOTE: It might be useful to make the calculations for this
        apparent to the user so they can judge for themself how accurate
        the program's result is. Maybe by returning something?
        """
        # strabismus detection logic goes here
        return "Strabismus detection called"

    def astigmatism(self,threshold):
        """ Analyze this patient for signs of astigmatism """
        # astigmatism logic goes here
        pupils = self.getAllPupils() #This call returns a tuple of Pupil objects
        if DEBUG:
            print str(pupils)

        refErrs = []

        for pupil in pupils:
            if pupil == None:
                print "Error: The horizontal photo's left pupil is not defined"
            else:
                refErrs.append( pupil.getCrescent() / pupil.getPupilArea()) # getPupilArea returns a float for the area of the pupil
        if DEBUG:
            print refErrs

        # flag to be set to false if any defects are found
        healthy = True

        # astigmatism is a difference in refractive error in the same eye
        # between the horiz and ver photos
        if abs(refErrs[0] - refErrs[2]) > threshold:
            healthy = False
            #TODO: This will need to be replaced with a structure to return. Perhaps a dict?
            print "Refer for astigmatism, info below:"
            print "Diff in refractive error: " + str(abs(refErrs[0] - refErrs[2]))
            print "horiz left: " + str(refErrs[0]) + " vert left: " + str(refErrs[2]) + "\n"
        if abs(refErrs[1] - refErrs[3]) > threshold:
            healthy = False
            #TODO: This will need to be replaced with a structure to return. Perhaps a dict?
            print "Refer for astigmatism, info below:"
            print "Diff in refractive error: " + str(abs(refErrs[1] - refErrs[3]))
            print "horiz right: " + str(refErrs[1]) + " vert right: " + str(refErrs[3]) + "\n"

        # anisometropia is a difference in refractive error 
        # between the left and right eye in the same photo
        if abs(refErrs[0] - refErrs[1]) > threshold:
            healthy = False
            #TODO: This will need to be replaced with a structure to return. Perhaps a dict?
            print "Refer for anisometropia, info below:"
            print "Diff in refractive error: " + str(abs(refErrs[0] - refErrs[1]))
            print "horiz left: " + str(refErrs[0]) + " horiz right: " + str(refErrs[1]) + "\n"
        if abs(refErrs[2] - refErrs[3]) > threshold:
            healthy = False
            #TODO: This will need to be replaced with a structure to return. Perhaps a dict?
            print "Refer for anisometropia, info below:"
            print "Diff in refractive error: " + str(abs(refErrs[2] - refErrs[3]))
            print "vert left: " + str(refErrs[2]) + " vert right: " + str(refErrs[3]) + "\n"
        
        if healthy:
            print "No astigmatism or anisometropia detected with a threshold of refractive error of " + str(threshold)

        return "Astigmatism detection called"

    def cataracts(self):
        """ Analyze this patient for signs of cataracts 

        Detect milky patches on the eye. If the patient has cataracts it will
        probably thrown pupil, whiteDot, crescent, and sclera detection off so
        it might be a good idea to work just from the original photo of the eye
        """
        # cataracts logic goes here
        return "Cataracts detection called"






    
        
