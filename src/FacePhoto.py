import cv2.cv as cv
import cv2
import time
import Image
import sys
from Eye import *
""" A class to perform actions on a photo of a face
    This class has two child classes:
      HorizonalPhoto
      VerticalPhoto
"""
# NOTE: photoImg is a photo of a face

DEBUG = True

class FacePhoto():
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
        self.facePhoto = photoImg
        # Initialize the other attributes to None so that they exist
        self.left = None
        self.right = None
        # Set attributes intialized to None by finding them.
        self.findEyes()

################# Utility Methods ######################

    def findEyes(self):
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
        # Load the image the user chose

        #NOTE: You may need to modify this path to point to the dir with your cascades
        faceCascade = cv.Load("C:/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
        eyeCascade = cv.Load("C:/opencv/data/haarcascades/haarcascade_eye.xml")

        # Detect the eyes and make an image with bounding boxes on it
        image = self.DetectEyes(self.facePhoto, faceCascade, eyeCascade)
        return "findEyes successfully called"
    
    ## Load the face and eye cascade when the analysis is done ##
    def Load():
       return (faceCascade, eyeCascade)

    ## The actual eye detection logic ##
    def DetectEyes(self, image, faceCascade, eyeCascade):
        min_size = (20,20)
        image_scale = 2
        haar_scale = 1.2
        min_neighbors = 2
        haar_flags = 0

        # Allocate the temporary images
        gray = cv.CreateImage((image.width, image.height), 8, 1)
        smallImage = cv.CreateImage((cv.Round(image.width / image_scale),
                                    cv.Round (image.height / image_scale)), 8 ,1)

        # Convert color input image to grayscale
        cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

        # Scale input image for faster processing
        cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)

        # Equalize the histogram
        cv.EqualizeHist(smallImage, smallImage)

        # Detect the faces
        faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
                                    haar_scale, min_neighbors, haar_flags, min_size)

        # If faces are found
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
                face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))
                cv.SetImageROI(image, (pt1[0], pt1[1], pt2[0] - pt1[0],
                                      int((pt2[1] - pt1[1]) * 0.7)))

        # If there are no faces found there's no reason to continue
        else:
            if DEBUG:
                print "No faces found, returning false"
            return False
      

        # NOTE: This returns the eye regions we're interested in
        eyes = cv.HaarDetectObjects(image, eyeCascade, cv.CreateMemStorage(0),
                                   haar_scale, min_neighbors, haar_flags, (15,15))

        if DEBUG:
            ## Draw rectangles around the eyes found ##
            if eyes:
                # For each eye found
                for eye in eyes:
                    # Draw a rectangle around the eye
                    cv.Rectangle(image,(eye[0][0], eye[0][1]),
                                 (eye[0][0] + eye[0][2],eye[0][1] + eye[0][3]),
                                 cv.RGB(255, 0, 0), 1, 8, 0)

        
        if DEBUG:
            # Display the image with bounding boxes
            cv.ShowImage("Face with Eyes", image)

            # Destroy the window when the user presses any key
            cv.WaitKey(0)
            cv.DestroyWindow("Face with Eyes")
                
        #calls set eyes if two regions found, otherwise returns false
        if len(eyes) == 2:
            self.setEyes(eyes[0][0], eyes[1][0])
            return True
        if DEBUG:
            print "Found more or less than 2 eyes, returning false"
        return False

    
    def eyeRemove(self, region):
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
        print str(region)
        eye = cv2.cv.GetSubRect(self.facePhoto, region)
        return eye

##################### Getters ############################

    def getEyes(self):
        """ Returns a tuple of the left and right eye objects """
        leftEye = self.getLeftEye()
        rightEye = self.getRightEye()
        return (leftEye, rightEye)

    def getLeftEye(self):
        """ Returns the left eye object """
        return self.left

    def getRightEye():
        """ Returns the right eye object """
        return self.right

##################### Setters ############################

    def setEyes(self, leftRegion, rightRegion):
        """ Sets or resets both eye objects """
        self.setLeftEye(leftRegion)
        self.setRightEye(rightRegion)
        return "setEyes successfully called"
        
    def setLeftEye(self,region):
        """ Constructs a new Eye object and stores it in left """
        # Crop out a photo of the eye to pass the Eye constructor
        left_eyePhoto = self.eyeRemove(region)
        # Constructs the left eye
        left = Eye(left_eyePhoto, region)
        return "setLeftEye successfully called"

    def setRightEye(self,region):
        """ Constructs a new Eye object and stores it in right """
        # Crop out a photo of the eye to pass the Eye constructor
        right_eyePhoto = self.eyeRemove(region)
        # Constructs the right eye
        right = Eye(right_eyePhoto, region)
        return "setRightEye successfully called"



    
        
    
