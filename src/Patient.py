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
        self.defects ={}
        self.info = {}


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

    def getInfo(self):
        """ Returns a dict with info/measurements in it (if any) """
        return self.info

    def getDefects(self):
        """ Returns a dict with info about defects found. If the dict is 
            empty then the patient is healthy """
        return self.defects

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
        self.strabismus()
        self.astigmatism(threshold)
        self.anisometropia(threshold)
        self.cataracts()
        self.pupillaryDistance()

    def pupillaryDistance(self):
        """ Calculates the Pupillary Distance (PD), prints it, and returns it
        """
        pupils = self.getAllPupils()
        hPD = 0
        vPD = 0
        # calculate PD from the horizontal photo
        if pupils[0] != None and pupils[1] != None:
            # These coordinates are relative to the pupil photo, not the photo at large
            leftCenterX = pupils[0].getPupilRegion()[0]
            leftCenterY = pupils[0].getPupilRegion()[1]
            rightCenterX = pupils[1].getPupilRegion()[0]
            rightCenterY = pupils[1].getPupilRegion()[1]
            # Recalculating to make the coordinates relative to the facephoto, not the pupil photo
            hLeft = self.getEyeRegion(True,True)
            hRight = self.getEyeRegion(True,False)
            relLeftCenterX = hLeft[0] + leftCenterX
            relLeftCenterY = hLeft[1] + leftCenterY
            relRightCenterX = hRight[0] + rightCenterX
            relRightCenterY = hRight[1] + rightCenterY
            hPD = math.sqrt((relLeftCenterX-relRightCenterX)**2 +(relLeftCenterY-relRightCenterY)**2)
        #print "Horiz PD: " + str(hPD)

        # calculate PD from the vertical photo
        if pupils [2] != None and pupils[3] != None:
            leftCenterX = pupils[2].getPupilRegion()[0]
            leftCenterY = pupils[2].getPupilRegion()[1]
            rightCenterX = pupils[3].getPupilRegion()[0]
            rightCenterY = pupils[3].getPupilRegion()[1]
            # Recalculating to make the coordinates relative to the facephoto, not the pupil photo
            vLeft = self.getEyeRegion(False,True)
            vRight = self.getEyeRegion(False,False)
            relLeftCenterX = vLeft[0] + leftCenterX
            relLeftCenterY = vLeft[1] + leftCenterY
            relRightCenterX = vRight[0] + rightCenterX
            relRightCenterY = vRight[1] + rightCenterY
            vPD = math.sqrt((relLeftCenterX-relRightCenterX)**2 +(relLeftCenterY-relRightCenterY)**2)
        #print "Vert PD: " + str(vPD)
        avgPD = (hPD + vPD) /2
        self.info["Pupillary Distance"] = str(avgPD)
        return "PD: " + str(avgPD) 

    def strabismus(self):
        """
        # possible error/situational cases:   - If distance between pupil and dot is minimal, and slope is 0 or undefined.
                                      - check both X and Y "distances" in 3rd check
                                      - in case of any center in "0" coordinates
                                      - should probably not have negatives except in test 3

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

            Pseudo Code - by David and Arvind            
                                    
            1. Calculate the distance from Pupil-center to White-dot-center for both Pupils
            2. Calculate the angle of Pupil-center to White-dot-center line [ using numpy.arctan on (y component of distance) / (x component of distance) ]
            3. Compare the two vectors from both pupils [ compare distances & angles ] 
                a. For a healthy eye, the angles should be same (looking in the same direction)         
                b. We could also measure the severeness of the off pupil-center and white-dot-center offset (healthy eye would have both in center)
                c. If the White dot is not found (within the Pupil), severe Strabismus

        NOTE: It might be useful to make the calculations for this
        apparent to the user so they can judge for themself how accurate
        the program's result is. Maybe by returning something?
        """
        #Threshold variables
        dThreshold = 0
        sThreshold = 0
        xThreshold = 0
        yThreshold = 0

      
        #Grabbing variables here ---------------------------------------------------------------------

        pupils = self.getAllPupils()

        # Calculate strab for the horizontal photo
        if pupils[0] != None and pupils[1] != None:
            # These coordinates are relative to the pupil photo, not the photo at large
            # Get the coordinates for the pupilCenter for both eyes
            pleftCenterX = pupils[0].getPupilRegion()[0]
            pleftCenterY = pupils[0].getPupilRegion()[1]

            prightCenterX = pupils[1].getPupilRegion()[0]
            prightCenterY = pupils[1].getPupilRegion()[1]

            # Get the coordinates for the white dot for both eyes
            wdleftCenterX = pupils[0].getWhiteDotCenter()[0]
            wdleftCenterY = pupils[0].getWhiteDotCenter()[1]

            wdrightCenterX = pupils[1].getWhiteDotCenter()[0]
            wdrightCenterY = pupils[1].getWhiteDotCenter()[1]
        else:
            return

        # 1.)  calculating difference of distances----------------------------------------------------------------


        leftDistance = math.sqrt((pleftCenterX-wdleftCenterX)**2 +(pleftCenterY-wdleftCenterY)**2)
        rightDistance = math.sqrt((prightCenterX-wdrightCenterX)**2 +(prightCenterY-wdrightCenterY)**2)

        # Calculate the slope of Pupil-center to White-dot-center line [ (y component of distance) / (x component of distance) ]
        # Compare the two vectors

        dDistance = abs(leftDistance - rightDistance); 

        # checks threshold distance
        if dDistance > dThreshold:                            # dThreshold should be near 0
           self.defects["Strabismus"] = True
           self.defects["Strabismus Distance Difference"] = str(dDistance)
           if DEBUG:
               print "Refer for strabismus, info below:"
               print "dDistance: " + str(dDistance) + "\n"
    


        # 2.)  calculating difference of slope--------------------------------------------------------------------

        lSlope = pleftCenterY / pleftCenterX;
        rSlope = prightCenterY /prightCenterX;
        x = float('nan');
        if lSlope == x:
            lSlope = 1000;
        if rSlope == x:
            rSlope = 1000;
        dSlope = abs(lSlope - rSlope);

        # checks threshold slope "distance"
        if dSlope > sThreshold:                   # sThreshold should be near 0
            self.defects["Strabismus"] = True
            self.defects["Strabismus Slope Difference"] = str(dSlope)
            if DEBUG:
                print "Refer for strabismus, info below:"
                print "dSlope: " + str(dSlope) + "\n"


        # 3.)  calculating difference of left x-axis------------------------------------------------------------------

        lxDifference = abs(wdleftCenterX - pleftCenterX);
        rxDifference = abs(wdrightCenterX - prightCenterX);

        xDifference = abs(lxDifference - rxDifference);

        #checks threshold x distance
        if xDifference > xThreshold:                              # xThreshold should be near 0
            self.defects["Strabismus"] = True
            self.defects["Strabismus X Difference"] = str(xDifference)
            if DEBUG:
                print "Refer for strabismus, info below:"
                print "xDifference: " + str(xDifference) + "\n"

        lyDistance = abs(wdleftCenterY - pleftCenterY);
        ryDistance = abs(wdrightCenterY - prightCenterY);

        yDifference = abs(lyDistance - ryDistance);

        # checks threshold y distance
        if yDifference > yThreshold:                             # yThreshold should be near 0
            self.defects["Strabismus"] = True
            self.defects["Strabismus Y Difference"] = str(yDifference)
            if DEBUG:
                print "Refer for strabismus, info below:"
                print "yDifference: " + str(yDifference) + "\n"

        return "strabismus called"
        # Calculate strab for the vertical photo


    def astigmatism(self,threshold):
        """ Analyze this patient for signs of astigmatism """
        # astigmatism logic goes here
        pupils = self.getAllPupils() #This call returns a tuple of Pupil objects
        if pupils == None:
            return
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
            self.defects["Astigmatism"] = True
            self.defects["Astigmatism Refractor Error Difference"] = str(abs(refErrs[0] - refErrs[2]))
            self.defects["Astigmatism Left"] = "H: " + str(refErrs[0]) + "   V: " + str(refErrs[2])
            if DEBUG:
                print "Refer for astigmatism, info below:"
                print "Diff in refractive error: " + str(abs(refErrs[0] - refErrs[2]))
                print "horiz left: " + str(refErrs[0]) + " vert left: " + str(refErrs[2]) + "\n"

        if abs(refErrs[1] - refErrs[3]) > threshold:
            healthy = False
            self.defects["Astigmatism"] = True
            self.defects["Astigmatism Refractor Error Difference"] = str(abs(refErrs[1] - refErrs[3]))
            self.defects["Astigmatism Right"] = "H: " + str(refErrs[1]) + "   V: " + str(refErrs[3])
            if DEBUG:
                print "Refer for astigmatism, info below:"
                print "Diff in refractive error: " + str(abs(refErrs[1] - refErrs[3]))
                print "horiz right: " + str(refErrs[1]) + " vert right: " + str(refErrs[3]) + "\n"
        
        if DEBUG and healthy:
            print "No astigmatism detected with a threshold of refractive error of " + str(threshold)

        return "Astigmatism detection called"

    def anisometropia(self,threshold):
        """ Analyze this patient for signs of anisometropia """
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

        # anisometropia is a difference in refractive error 
        # between the left and right eye in the same photo
        if abs(refErrs[0] - refErrs[1]) > threshold:
            healthy = False
            self.defects["Anisomet"] = True
            self.defects["Anisomet Refractor Error Difference"] = str(abs(refErrs[0] - refErrs[1]))
            self.defects["Anisomet Horizontal"] = "L: " + str(refErrs[0]) + "   R: " + str(refErrs[1])
            if DEBUG:
                print "Refer for anisometropia, info below:"
                print "Diff in refractive error: " + str(abs(refErrs[0] - refErrs[1]))
                print "horiz left: " + str(refErrs[0]) + " horiz right: " + str(refErrs[1]) + "\n"

        if abs(refErrs[2] - refErrs[3]) > threshold:
            healthy = False
            self.defects["Anisomet"] = True
            self.defects["Anisomet Refractor Error Difference"] = str(abs(refErrs[2] - refErrs[3]))
            self.defects["Anisomet Vertical"] = "L: " + str(refErrs[2]) + "   R: " + str(refErrs[3])
            if DEBUG:
                print "Refer for anisometropia, info below:"
                print "Diff in refractive error: " + str(abs(refErrs[2] - refErrs[3]))
                print "vert left: " + str(refErrs[2]) + " vert right: " + str(refErrs[3]) + "\n"
        
        if DEBUG and healthy:
            print "No anisometropia detected with a threshold of refractive error of " + str(threshold)

        return "Astigmatism detection called"

    def cataracts(self):
        """ Analyze this patient for signs of cataracts 

        Detect milky patches on the eye. If the patient has cataracts it will
        probably thrown pupil, whiteDot, crescent, and sclera detection off so
        it might be a good idea to work just from the original photo of the eye
        """
        # cataracts logic goes here
        return "Cataracts detection called"






    
        
