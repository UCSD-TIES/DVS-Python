"""" This code drives the image analysis and detection and serves as glue
between the classes (Model in MVC) and the UI(View in MVC)
"""
from Patient import *
from FacePhoto import *
from HorizontalPhoto import *
from VerticalPhoto import *
from Eye import *
from Pupil import *
import cv2.cv as cv

DEBUG = False

def detectEyes(horizontalPath, verticalPath):
    """ Detects the eyes in both images and passes back a tuple of coordinates

    Args:
        string horizontalPath - the full path to the horizontal photo
        string verticalPath - the full path to the vertical photo

    Return:
        The coordinates of the eyes for horizontal and vertical
        Tuple of :
            tuple horizontalTuple - (leftCoordinates, rightCoordinates)
            tuple verticalTuple - (leftCoordinates, rightCoordinates)

    """
    # Load the images
    horizontalImg = cv.LoadImage(horizontalPath)
    verticalImg = cv.LoadImage(verticalPath)
    thisPatient = Patient(horizontalImg, verticalImg)
    if DEBUG:
        
        # show the variables as they have been populated
        print "Showing patient's horizontal image..."
        cv.ShowImage("Horizontal",thisPatient.getHorizontal())
        cv.WaitKey(0)
        cv.DestroyWindow("Horizonatl")
        print "Showing patient's vertical image..."
        cv.ShowImage("Vertical",thisPatient.getVertical())
        cv.WaitKey(0)
        cv.DestroyWindow("Vertical")
        print "Showing photo of the patient's horizontal left eye..."
        cv.ShowImage("Horizontal Left Eye",thisPatient.horizontal.left.eyePhoto)
        cv.WaitKey(0)
        cv.DestroyWindow("Horizontal Left Eye")
        print "Showing photo of the patient's horizonal right eye..."
        cv.ShowImage("Vertical Right Eye",thisPatient.horizontal.right.eyePhoto)
        cv.WaitKey(0)
        cv.DestroyWindow("Horizontal Right Eye")
        
        # ISSUE: These two print statemtents are not actually printing
        print "Patient: " + str(thisPatient)
        print "Attributes: " + str(thisPatient.__dict__)
        print "Here's our left region again: " + str(thisPatient.horizontal.left.eyeRegion)
        print "Here's our right region again: " + str(thisPatient.horizontal.right.eyeRegion)

    return thisPatient

def resetEyes(horizontalTuple, verticalTuple):
    """ Resets the eye regions to whatever 

    Args:
        tuple horizontalTuple - (leftCoordinates, rightCoordinates)
        tuple verticalTuple - (leftCoordinates, rightCoordinates)

    Return:
        ?
    """

def drawOnEyes(patient):
    """ Draws rectangles around the facephoto of a horizontal and vertical photo
        and displays them in succession
    """

######################Testing ######################
'''
# The following code replicates calls from the UI layer
patient = detectEyes("C:/Users/Shannon/Documents/GitHub/DVS-Python/Faces/OldNHappy.jpg",
           "C:/Users/Shannon/Documents/GitHub/DVS-Python/Faces/ObamaRotated.jpg")
#TODO: Encapsulate these calls.
# Take the horizontal image and draw bounding eye boxes
horizontalPhoto = patient.getHorizontal()
hLeft = patient.getEyeRegion(True,True)
hRight = patient.getEyeRegion(True,False)
# Draw Left and right eyes
if hLeft != None and hRight != None:
    cv.Rectangle(horizontalPhoto, (hLeft[0],hLeft[1]),(hLeft[2],hLeft[3]),
             cv.RGB(255,0,0,), 1, 8, 0)
    cv.Rectangle(horizontalPhoto, (hRight[0],hRight[1]),(hRight[2],hRight[3]),
             cv.RGB(255,0,0,), 1, 8, 0)
# Display the image
cv.ShowImage("Horizontal with eyes",horizontalPhoto)
cv.WaitKey(0)
cv.DestroyWindow("Horizontal with eyes")

# Do the same for vertical
verticalPhoto = patient.getVertical()
vLeft = patient.getEyeRegion(False,True)
vRight = patient.getEyeRegion(False,False)
# Draw Left and right eyes
if vLeft != None and vRight != None:
    cv.Rectangle(verticalPhoto, (vLeft[0],vLeft[1]),(vLeft[2],vLeft[3]),
             cv.RGB(255,0,0,), 1, 8, 0)
    cv.Rectangle(verticalPhoto, (vRight[0],vRight[1]),(vRight[2],vRight[3]),
             cv.RGB(255,0,0,), 1, 8, 0)
# Display the image
cv.ShowImage("Vertical with eyes",verticalPhoto)
cv.WaitKey(0)
cv.DestroyWindow("Vertical with eyes")


'''
