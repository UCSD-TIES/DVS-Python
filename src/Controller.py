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

CIRCLE_COLOR = (0, 255, 0)
THICKNESS = 1
LINE_TYPE = 8
SHIFT = 0

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
    thisPatient = Patient(horizontalImg, horizontalPath, verticalImg, verticalPath)
    
    if DEBUG:
        # show the variables as they have been populated
        print "Showing patient's horizontal image..."
        cv.ShowImage("Horizontal",thisPatient.getHorizontal())
        cv.WaitKey(0)
        cv.DestroyWindow("Horizontal")
        print "Showing patient's vertical image..."
        cv.ShowImage("Vertical",thisPatient.getVertical())
        cv.WaitKey(0)
        cv.DestroyWindow("Vertical")
        print "Showing photo of the patient's horizontal left eye..."
        print thisPatient.horizontal.left.eyePhoto
        cv.ShowImage("Horizontal Left Eye",thisPatient.horizontal.left.eyePhoto)
        cv.WaitKey(0)
        cv.DestroyWindow("Horizontal Left Eye")
        print "Showing photo of the patient's horizonal right eye..."
        cv.ShowImage("Horizontal Right Eye",thisPatient.horizontal.right.eyePhoto)
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


# The following code replicates calls from the UI layer
print "Making patient object..."
# Horizontal photos have the eyes along a horizontal axis
patient = detectEyes("C:/Users/Shannon/Documents/GitHub/DVS-Python/Faces/red06.jpg",
           "C:/Users/Shannon/Documents/GitHub/DVS-Python/Faces/red11.jpg")
   
# Take the horizontal image and draw bounding eye boxes
horizontalPhoto = patient.getHorizontal()
hLeft = patient.getEyeRegion(True,True)
hRight = patient.getEyeRegion(True,False)
# Draw Left and right eyes
print "Drawing bounding boxes for the horizontal photo..."
if hLeft != None and hRight != None:
    cv.Rectangle(horizontalPhoto, (hLeft[0],hLeft[1]),(hLeft[2],hLeft[3]),
             cv.RGB(255,0,0,), 1, 8, 0)
    cv.Rectangle(horizontalPhoto, (hRight[0],hRight[1]),(hRight[2],hRight[3]),
             cv.RGB(255,0,0,), 1, 8, 0)
# Draw the Left and Right pupils
hLeftPupil = patient.getPupilRegion(True,True)
hRightPupil = patient.getPupilRegion(True,False)
if hLeftPupil != None:
    x = int(hLeft[0] + hLeftPupil[0])
    y = int(hLeft[1] + hLeftPupil[1])
    cv.Circle(horizontalPhoto, (x, y), hLeftPupil[2], 
        CIRCLE_COLOR, THICKNESS, LINE_TYPE, SHIFT)
if hRightPupil != None:
    x = int(hRight[0] + hRightPupil[0])
    y = int(hRight[1] + hRightPupil[1])
    cv.Circle(horizontalPhoto, (x, y), hRightPupil[2], 
    CIRCLE_COLOR, THICKNESS, LINE_TYPE, SHIFT)


# Display the image
cv.ShowImage("Horizontal with eyes",horizontalPhoto)
cv.WaitKey(0)
cv.DestroyWindow("Horizontal with eyes")

# Do the same for vertical
verticalPhoto = patient.getVertical()
vLeft = patient.getEyeRegion(False,True)
vRight = patient.getEyeRegion(False,False)
print "Drawing bounding boxes for the vertical photo..."
# Draw Left and right eyes
if vLeft != None and vRight != None:
    cv.Rectangle(verticalPhoto, (vLeft[0],vLeft[1]),(vLeft[2],vLeft[3]),
             cv.RGB(255,0,0,), 1, 8, 0)
    cv.Rectangle(verticalPhoto, (vRight[0],vRight[1]),(vRight[2],vRight[3]),
             cv.RGB(255,0,0,), 1, 8, 0)

# Draw the left and right Pupils
vLeftPupil = patient.getPupilRegion(False,True)
vRightPupil = patient.getPupilRegion(False,False)
if vLeftPupil != None:
    x = int(vLeft[0] + vLeftPupil[0])
    y = int(vLeft[1] + vLeftPupil[1])
    cv.Circle(horizontalPhoto, (x, y), vLeftPupil[2], 
        CIRCLE_COLOR, THICKNESS, LINE_TYPE, SHIFT)
if vRightPupil != None:
    x = int(vRight[0] + vRightPupil[0])
    y = int(vRight[1] + vRightPupil[1])
    cv.Circle(horizontalPhoto, (x, y), vRightPupil[2], 
        CIRCLE_COLOR, THICKNESS, LINE_TYPE, SHIFT)

# Display the image
cv.ShowImage("Vertical with eyes",verticalPhoto)
cv.WaitKey(0)
cv.DestroyWindow("Vertical with eyes")

#Display the eyes only of the horizontal photo
#if DEBUG: 
hLeftEyePhoto = patient.getEyePhoto(True,True)
hRightEyePhoto = patient.getEyePhoto(True,False)
cv.ShowImage("Horizontal's Left Eye",hLeftEyePhoto)
cv.WaitKey(0)
cv.DestroyWindow("Horizontal's Left Eye")

cv.ShowImage("Horizontal's Right Eye",hRightEyePhoto)
cv.WaitKey(0)
cv.DestroyWindow("Horizontal's Right Eye")

print "Horizontal Left Pupil: " + str( patient.horizontal.left.eyePupil.pupil)
print "Horizontal Right Pupil: " + str( patient.horizontal.right.eyePupil.pupil)



