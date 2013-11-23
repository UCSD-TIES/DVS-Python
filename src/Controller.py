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
import os

DEBUG = False
TEST = True

CIRCLE_COLOR = (0, 255, 0)
THICKNESS = 1
LINE_TYPE = 8
SHIFT = 0

def makePatient(horizontalPath, verticalPath):
    """ Makes and returns a patient object

    Args:
        string horizontalPath - the full path to the horizontal photo
        string verticalPath - the full path to the vertical photo

    Return:
        Patient - the patient object created

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

def resetEyes(thisPatient, horizontalTuple, verticalTuple):
    """ Resets the eye regions to whatever 

    Args:
        Patient thisPatient - the patient to change
        tuple horizontalTuple - (leftCoordinates, rightCoordinates)
        tuple verticalTuple - (leftCoordinates, rightCoordinates)
        where leftCoordinates and rightCoordinates are formatted as 
        (topLeftX, topLeftY, bottomRightX, bottomRightY)


    Return:
        None
    """  
    # Set horizontal photo data?
    if horizontalTuple != None:
        # Set left eye coords?
        if horizontalTuple[0] != None:
            # I'm just gunna go direct because this isn't final code
            # TODO: write the appropriate methods for this
            if thisPatient.horizontal.left != None:
                thisPatient.horizontal.left.setEyeRegion(horizontalTuple[0])
            else:
                print "Error: thisPatient.horizontal.left == None"
        # Set right eye coords?
        if horizontalTuple[1] != None:
            if thisPatient.horizontal.right != None:
                thisPatient.horizontal.right.setEyeRegion(horizontalTuple[1])
            else:
                print "Error: thisPatient.horizontal.right == None"

    # Set vert photo data?
    if verticalTuple != None:
        # Set left eye coords?
        if verticalTuple[0] != None:
            if thisPatient.vertical.left != None:
                thisPatient.vertical.left.setEyeRegion(verticalTuple[0])
            else:
                print "Error: thisPatient.vertical.left == None"
        # Set right eye coords?
        if verticalTuple[1] != None:
            if thisPatient.vertical.right != None:
                thisPatient.vertical.right.setEyeRegion(verticalTuple[1])
            else:
                print "Error: thisPatient.vertical.right == None"

def resetPupils(thisPatient, horizontalTuple, verticalTuple):
    """ Resets (or sets) the pupil regions in the eyes

    If a tuple is passed in as None then that portion of the 
    data will not get reset.

    Args:
        tuple horizontalTuple - (leftPupil,rightPupil)
        tuple verticalTuple - (leftPupil, rightPupil)
        where leftPupil and rightPupil are of the form
        (centerX, centerY, radius)

    Return: 
        None 
    """
    # Set horizontal photo data?
    if horizontalTuple != None:
        # Set left pupil coords?
        if horizontalTuple[0] != None:
            # I'm just gunna go direct because this isn't final code
            # TODO: write the appropriate methods for this
            thisPatient.horizontal.left.setPupil(horizontalTuple[0])
        # Set right pupil coords?
        if horizontalTuple[1] != None:
            thisPatient.horizontal.right.setPupil(horizontalTuple[1])

    # Set vert photo data?
    if verticalTuple != None:
        # Set left pupil coords?
        if verticalTuple[0] != None:
            thisPatient.vertical.left.setPupil(verticalTuple[0])
        # Set right pupil coords?
        if verticalTuple[1] != None:
            thisPatient.vertical.right.setPupil(verticalTuple[1])

def resetWhiteDot(thisPatient, horizontalTuple, verticalTuple):
    """ Resets the eye regions to whatever 

    Args:
        Patient thisPatient - the patient to change
        tuple horizontalTuple - (leftCoordinates, rightCoordinates)
        tuple verticalTuple - (leftCoordinates, rightCoordinates)
        where leftCoordinates and rightCoordinates are formatted as 
        (topLeftX, topLeftY, bottomRightX, bottomRightY)


    Return:
        None
    """  
    if thisPatient.horizontal.left.eyePupil == None:
        print "Error: thisPatient.horizontal.left.eyePupil == None"
        return
    # Set horizontal photo data?
    if horizontalTuple != None:
        # Set left eye coords?
        if horizontalTuple[0] != None:
            # I'm just gunna go direct because this isn't final code
            # TODO: write the appropriate methods for this
            if thisPatient.horizontal.left != None:
                thisPatient.horizontal.left.eyePupil.setwhiteDot(horizontalTuple[0])
            else:
                print "Error: thisPatient.horizontal.left == None"
        # Set right eye coords?
        if horizontalTuple[1] != None:
            if thisPatient.horizontal.right != None:
                thisPatient.horizontal.right.eyePupil.setwhiteDot(horizontalTuple[1])
            else:
                print "Error: thisPatient.horizontal.right == None"

    if thisPatient.horizontal.right.eyePupil == None:
        print "Error: thisPatient.horizontal.left.eyePupil == None"
        return
    # Set vert photo data?
    if verticalTuple != None:
        # Set left eye coords?
        if verticalTuple[0] != None:
            if thisPatient.vertical.left != None:
                thisPatient.vertical.left.eyePupil.setwhiteDot(verticalTuple[0])
            else:
                print "Error: thisPatient.vertical.left == None"
        # Set right eye coords?
        if verticalTuple[1] != None:
            if thisPatient.vertical.right != None:
                thisPatient.vertical.right.eyePupil.setwhiteDot(verticalTuple[1])
            else:
                print "Error: thisPatient.vertical.right == None"

def drawOnEyes(thisPatient):
    """ Draws rectangles around the facephoto of a horizontal and vertical photo
        and displays them in succession
    """

######################Testing ######################

if (TEST):
    # The following code replicates calls from the UI layer
    print "Making patient object..."

    # Horizontal photos have the eyes along a horizontal axis
    horiz = os.path.dirname(os.path.abspath(sys.argv[0]))
    horiz += "/pics/Red06.jpg"
    vert = os.path.dirname(os.path.abspath(sys.argv[0]))
    vert += "/pics/Red11.jpg"
    patient = makePatient(horiz, vert)

    # Take the horizontal image and draw bounding eye boxes
    horizontalPhoto = patient.getHorizontal()

    # Reset the eye regions and pupil regions
    print "Resetting the eye regions and the pupil regions "
    #resetEyes( patient, ((100,100,150,150),(150,150,200,200)) , ((100,100,150,150),(150,150,200,200)) )
    #resetPupils( patient, ((125,125,10),(175,175,20)) , ((125,125,10),(175,175,20)) )

    resetWhiteDot(patient, ((100, 100, 10), (150, 150, 10)), ((100, 100,10),(150,150,10,10)))


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
            #pupil area for crescent ratio
        aRight = math.pow(hLeftPupil[2],2) * 3.14
    if hRightPupil != None:
        x = int(hRight[0] + hRightPupil[0])
        y = int(hRight[1] + hRightPupil[1])
        cv.Circle(horizontalPhoto, (x, y), hRightPupil[2], 
        CIRCLE_COLOR, THICKNESS, LINE_TYPE, SHIFT)
        #pupil area for crescent ratio
        aRight = math.pow(hRightPupil[2],2) * 3.14



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
    
    cv.WaitKey(0)
    cv.DestroyAllWindows()

    print "Horizontal Left Pupil: " + str( patient.horizontal.left.eyePupil.pupil)
    print "Horizontal Right Pupil: " + str( patient.horizontal.right.eyePupil.pupil)

