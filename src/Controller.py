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
TEST = False
PRINT = False
     
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




def removePupilPhoto():
    """ Function call to remove photos of the pupil saved to disk during
    runtime of the program when called by frontend
 
    Path should be relative path
    
    Args:
        None
    Return:
        None
    Side Effects:
        Deletes PUPILPHOTO.jpg, hLeftEye.jpg, hRightEye.jpg,
    vLeftEye.jpg, and vRightEye.jpg from disk
    """
    
    os.remove(os.path.join(os.path.dirname(__file__), 'PUPILPHOTO.jpg'))
    os.remove(os.path.join(os.path.dirname(__file__), 'hLeftEye.jpg'))
    os.remove(os.path.join(os.path.dirname(__file__), 'hRightEye.jpg'))
    os.remove(os.path.join(os.path.dirname(__file__), 'vLeftEye.jpg'))
    os.remove(os.path.join(os.path.dirname(__file__), 'vRightEye.jpg'))

### Reset Methods ###

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
    
    RESET_EYE = True
    ### coordinate negative value check ###
    # horizontal left coordinate
    if horizontalTuple[0][0] < 0 or horizontalTuple[0][1] < 0:
        print "Error..Horizontal left coordinate cannot have negative value"
        RESET_EYE = False
    elif horizontalTuple[0][2] < 0 or horizontalTuple[0][3] < 0:
        print "Error..Horizontal left Coordinate cannot have negative value "
        RESET_EYE = False
        
    # horizontal right coordinate
    if horizontalTuple[1][0] < 0 or horizontalTuple[1][1] < 0:
        print "Error..Horizontal right coordinates cannot have negative value"
        RESET_EYE = False
    elif horizontalTuple[1][2] < 0 or horizontalTuple[1][3] < 0:
        print "Error..Horizontal right coordinates cannot have negative value"
        RESET_EYE = False
        
    # vertical left coordinate
    if verticalTuple[0][0] < 0 or verticalTuple[0][1] < 0:
        print "Error..Vertical left coordinate cannot have negative value"
        RESET_EYE = False
    elif verticalTuple[0][2] < 0 or verticalTuple[0][3] < 0:
        print "Error..Vertical left Coordinate cannot have negative value "
        RESET_EYE = False
        
    #vertical right coordinate
    if verticalTuple[1][0] < 0 or verticalTuple[1][1] < 0:
        print "Error..vertical right coordinates cannot have negative value"
        RESET_EYE = False
    elif verticalTuple[1][2] < 0 or verticalTuple[1][3] < 0:
        print "Error..vertical right coordinates cannot have negative value"
        RESET_EYE = False    
          
    ####  check end ###
    
    ###  Check if top left is less than bottom right  ####
    # horizontal tuple, left coordinate
    if horizontalTuple[0][0] > horizontalTuple[0][2]:
        print "Error.. Horizontal left: topLeft X cannot be greater than bottomRight X"
        RESET_EYE = False
    elif horizontalTuple[0][1] > horizontalTuple[0][3]:
        print "Error.. Horizontal left: topLeft Y cannot be greater than bottomRight Y"
        RESET_EYE = False
        
    #horizontal tuple, right coordinate
    if horizontalTuple[1][0] > horizontalTuple[1][2]:
        print "Error.. Horizontal right: topLeft X cannot be greater than bottomRight X"
        RESET_EYE = False
    elif horizontalTuple[1][1] > horizontalTuple[1][3]:
        print "Error.. Horizontal right: topLeft Y cannot be greater than bottomRight Y"
        RESET_EYE = False
        
    # vertical tuple, Left coordinate
    if verticalTuple[0][0] > verticalTuple[0][2]:
        print "Error.. Vertical left: topleftX cannot be greater than bottomRight X"
        RESET_EYE = False
    elif verticalTuple[0][1] > verticalTuple[0][3]:
        print "Error.. vertical left: topLeft Y cannot be greater than bottomRight Y"
        RESET_EYE = False
        
    # vertical tuple, right coordinate
    if verticalTuple[1][0] > verticalTuple[1][2]:
        print "Error.. Vertical right: topleftX cannot be greater than bottomRight X"
        RESET_EYE = False
    elif verticalTuple[1][1] > verticalTuple[1][3]:
        print "Error.. vertical right: topLeft Y cannot be greater than bottomRight Y"
        RESET_EYE = False
        
    ### end ###
    
    ### check if topLeft and bottomRight are equal, they shouldn't be equal  ###
    
    # Horizontal tuple, left coordinate
    if horizontalTuple[0][0] == horizontalTuple[0][2]:
        print "Error.. Horizontal left: topLeft X and bottomRight x cannot be equal"
        RESET_EYE = False
    elif horizontalTuple[0][1] == horizontalTuple[0][3]:
        print "Error.. Horizontal left: topLeft Y and bottomRight Y cannot be equal"
        RESET_EYE = False
        
     #horizontal tuple, right coordinate
    if horizontalTuple[1][0] == horizontalTuple[1][2]:
        print "Error.. Horizontal right: topLeft X and bottomRight X cannot be equal"
        RESET_EYE = False
    elif horizontalTuple[1][1] == horizontalTuple[1][3]:
        print "Error.. Horizontal right: topLeft Y and bottomRight Y cannot be equal"
        RESET_EYE = False
        
    # vertical tuple, left coordinate
    if verticalTuple[0][0] == verticalTuple[0][2]:
        print "Error.. vertical left: topLeft X and bottomRight X cannot be equal"
        RESET_EYE = False
    elif verticalTuple[0][1] == verticalTuple[0][3]:
        print "Error.. vertical left: topLeft Y and bottomRight Y cannot be equal"
        RESET_EYE = False
        
     #vertical tuple, right coordinate
    if verticalTuple[1][0] == verticalTuple[1][2]:
        print "Error.. vertical right: topLeft X and bottomRight X cannot be equal"
        RESET_EYE = False
    elif verticalTuple[1][1] == verticalTuple[1][3]:
        print "Error.. vertical right: topLeft Y and bottomRight Y cannot be equal"  
        RESET_EYE = False
        
    ### end  ####
    
    ### check if left coordinate & right coordinate equal  ###
    if horizontalTuple[0][0] == horizontalTuple[1][0]:
        if horizontalTuple[0][1] == horizontalTuple[1][1]:
            if horizontalTuple[0][2] == horizontalTuple[1][2]:
                if horizontalTuple[0][3] == horizontalTuple[1][3]:
                    print "Error.. horizontal, left and right coordinate cannot be equal"
                    RESET_EYE = False
    if verticalTuple[0][0] == verticalTuple[1][0]:
        if verticalTuple[0][1] == verticalTuple[1][1]:
            if verticalTuple[0][2] == verticalTuple[1][2]:
                if verticalTuple[0][3] == verticalTuple[1][3]:
                    print "Error.. vertical, left and right coordinate cannot be equal"
                    RESET_EYE = False
    
    ### ends ###
    
    ### do not need to check check if all values are 0 (rect of 0 area), front end will check this###
  
    if RESET_EYE:
        if horizontalTuple != None and thisPatient.horizontal != None:
            thisPatient.horizontal.setEyes(horizontalTuple[0],horizontalTuple[1])
        # Set vert photo data
        if verticalTuple != None and thisPatient.vertical != None:
            thisPatient.vertical.setEyes(verticalTuple[0],verticalTuple[1])

    else:  ### if RESET_EYE == False ###
        # TODO: Implement out a more graceful way of dealing with this error case
        print " Can't reset eyes... "

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
    """ Resets the white dots for the patient

    Args:
        Patient thisPatient - the patient to change
        tuple horizontalTuple - (leftCoordinates, rightCoordinates)
        tuple verticalTuple - (leftCoordinates, rightCoordinates)
        where leftCoordinates and rightCoordinates are formatted as 
        (centerX, centerY)


    Return:
        None
    """  
    if thisPatient.horizontal.left.eyePupil == None:
        # TODO: Again implement a more graceful way of dealing 
        #       with these error cases
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


### Get Methods ###



def getEyeCoors(thisPatient):
    """ Returns a tuple of coordinates that represent the bounding rectangles
        of the eyes. The tuple returned is formatted thus:

        (horizontalLeft, horizontalRight, verticalLeft, verticalRight)

         where each element in the tuple above is itself a tuple formatted as:

        (topLeftX, topLeftY, width, height)

        So if the bounding box for the horizontal photo's left eye had a top left 
        corner with coordinates (50,20), a width of 30, and a height of 5 we would return:

        ((50,20,30,5),(hrtlx,hrtly,hrw,hrh),(vltlx,vltly,vlw,vlh),(vrtlx,vrtly,vrw,vrh))

    """

    hLeft = thisPatient.getEyeRegion(True,True)
    hLeftX = 0
    hLeftY = 0
    hLeftWidth = 0
    hLeftHeight = 0
    if hLeft != None:
        hLeftX = hLeft[0]
        hLeftY = hLeft[1]
        hLeftWidth = hLeft[2] - hLeft[0]
        hLeftHeight = hLeft[3] - hLeft[1]

    hRight = thisPatient.getEyeRegion(True,False)
    hRightX = 0
    hRightY = 0
    hRightWidth = 0
    hRightHeight = 0
    if hRight != None:
        hRightX = hRight[0]
        hRightY = hRight[1]
        hRightWidth = hRight[2] - hRight[0]
        hRightHeight = hRight[3] - hRight[1]

    vLeft = thisPatient.getEyeRegion(False,True)
    vLeftX = 0
    vLeftY = 0
    vLeftWidth = 0
    vLeftHeight = 0
    if vLeft != None:
        vLeftX = vLeft[0]
        vLeftY = vLeft[1]
        vLeftWidth = vLeft[2] - vLeft[0]
        vLeftHeight = vLeft[3] - vLeft[1]

    vRight = thisPatient.getEyeRegion(False,False)
    vRightX = 0
    vRightY = 0
    vRightWidth = 0
    vRightHeight = 0
    if vRight != None:
        vRightX = vRight[0]
        vRightY = vRight[1]
        vRightWidth = vRight[2] - vRight[0]
        vRightHeight = vRight[3] - vRight[1]

    if DEBUG:
        print hLeft
        print hRight
        print vLeft
        print vRight

        print "Done eyecoors"

        print ((hLeft[0],hLeft[1],hLeftWidth,hLeftHeight),(hRight[0],hRight[1],hRightWidth,hRightHeight),
               (vLeft[0],vLeft[1],vLeftWidth,vLeftHeight),(vRight[0],vRight[1],vRightWidth,vRightHeight))

    return ((hLeftX,hLeftY,hLeftWidth,hLeftHeight),(hRightX,hRightY,hRightWidth,hRightHeight),
        (vLeftX,vLeftY,vLeftWidth,vLeftHeight),(vRightX,vRightY,vRightWidth,vRightHeight))

def getEyePhotos(thisPatient):
    """"
        Write eye photos to disk in jpg formatted
             bcuz what front end wants front end gets
        Pass back a tuple of the paths to the photos
            in the format (hLeftPath, hRightPath, vLeftPath, vRightPath)
    """

    # Get Photos
    hLeftEyePhoto = thisPatient.getEyePhoto(True,True)
    hRightEyePhoto = thisPatient.getEyePhoto(True,False)
    vLeftEyePhoto = thisPatient.getEyePhoto(False,True)
    vRightEyePhoto = thisPatient.getEyePhoto(False,False)

    #Write to disk
    cv2.imwrite("hLeftEye.jpg",np.asarray(hLeftEyePhoto))
    cv2.imwrite("hRightEye.jpg",np.asarray(hRightEyePhoto))
    cv2.imwrite("vLeftEye.jpg",np.asarray(vLeftEyePhoto))
    cv2.imwrite("vRightEye.jpg",np.asarray(vRightEyePhoto))

    # Make path strings
    hLeftPath = os.path.dirname(os.path.abspath(sys.argv[0]))
    hLeftPath += "/hLeftEye.jpg"  
    hRightPath = os.path.dirname(os.path.abspath(sys.argv[0]))
    hRightPath += "/hRightEye.jpg"  
    vLeftPath = os.path.dirname(os.path.abspath(sys.argv[0]))
    vLeftPath += "/vLeftEye.jpg"  
    vRightPath = os.path.dirname(os.path.abspath(sys.argv[0]))
    vRightPath += "/vRightEye.jpg"  

    # Pass back paths
    return(hLeftPath, hRightPath, vLeftPath, vRightPath)

def drawOnEyes(thisPatient):
    """ Draws rectangles around the facephoto of a horizontal and vertical photo
        and displays them in succession

    cv.Rectangle(image,(topleftX,topLeftY),(bottomRightX,bottomRightY),
                cv.RGB(255,0,0),1,8,0)
    """


######################Testing ######################

if (TEST):
    # The following code replicates calls from the UI layer
    print "Making patient object..."

    # Horizontal photos have the eyes along a horizontal axis
    horiz = os.path.dirname(os.path.abspath(sys.argv[0]))
    horiz += "/pics/homemade/jthorizontal.jpg"  
    vert = os.path.dirname(os.path.abspath(sys.argv[0]))
    vert += "/pics/homemade/andrewvertical.jpg"
    patient = makePatient(horiz, vert)

    # Take the horizontal image and draw bounding eye boxes
    horizontalPhoto = patient.getHorizontal()
    
    # Reset the eye regions and pupil regions
    # print "Resetting the eye regions and the pupil regions..."
    resetEyes( patient, ((455,572,647,695),(771,537,958,650)) ,((467,596,620,718),(746,614,887,704)) )
    #resetEyes (patient, ((1,10,20,30), (2,11,21,32)), ((101,102,140,156), (123,141,202,200)))

    # Pass in pupil coordinates relative to the eye photo 
    #resetPupils( patient, ((93,64,17),(91,62,19)) , ((33,32,8 ),(32,28,8)) )
    #resetEyes( patient, ((100,100,150,150),(150,150,200,200)) , ((101,101,151,151),(151,151,201,201)) )
    
    # negative value
#    resetEyes( patient, ((-1, 0, 30, 40), (0, 20, 30, 40)), (( 101, 101,151,151), (151,151, 201, 201)))
    
    # topleft x greater than bottom right x
#    resetEyes( patient, ((10,10, 5, 5), (0, 20, 30, 40)), ((101, 101, 151, 151), (151, 151, 201, 201)))
    
    # topleft x equal to bottom right x
#    resetEyes( patient, ((0, 10, 0, 20), (0, 20, 30, 40)), ((101, 101, 151, 151), (151, 151, 201, 201)))
    
    # left coordinate and right coordinate equal
#    resetEyes( patient, ((0, 10, 20, 30), (0, 10, 20, 30)), ((101, 101, 151, 151), (151, 151, 201, 201)))

#    resetEyes( patient, ((1, 10, 20, 30), (2, 11, 21, 31)), ((101, 102, 140, 156), (123, 141, 202, 200)))
    
    #resetPupils( patient, ((125,125,10),(175,175,20)) , ((125,125,10),(175,175,20)) )

    # TODO: We don't actually need the circle of the white dot  and findWhiteDot
    # finds a contour which isn't quite a cirlce so we'll just deal with
    # whiteDotCenter now. resetWhiteDot will probably take some tweaking
    # resetWhiteDot(patient, ((100, 100, 10), (150, 150, 10)), (( 100, 100,10),(150,150,10,10)))

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
        cv.Circle(verticalPhoto, (x, y), vLeftPupil[2], 
            CIRCLE_COLOR, THICKNESS, LINE_TYPE, SHIFT)
    if vRightPupil != None:
        x = int(vRight[0] + vRightPupil[0])
        y = int(vRight[1] + vRightPupil[1])
        cv.Circle(verticalPhoto, (x, y), vRightPupil[2], 
            CIRCLE_COLOR, THICKNESS, LINE_TYPE, SHIFT)

    # Display the image
    cv.ShowImage("Vertical with eyes",verticalPhoto)
    cv.WaitKey(0)
    cv.DestroyWindow("Vertical with eyes")

    #Display the eyes only of the horizontal photo
    if DEBUG: 
        hLeftEyePhoto = patient.getEyePhoto(True,True)
        hRightEyePhoto = patient.getEyePhoto(True,False)
        cv.ShowImage("Horizontal's Left Eye",hLeftEyePhoto)
        cv.WaitKey(0) 
        cv.DestroyWindow("Horizontal's Left Eye")

        cv.ShowImage("Horizontal's Right Eye",hRightEyePhoto)
        cv.WaitKey(0)
        cv.DestroyWindow("Horizontal's Right Eye")
    
    if PRINT:
        getEyeCoors(patient)

        print "\nHorizontal Left Pupil: "
        if patient.horizontal.left.eyePupil != None:
            patient.horizontal.left.eyePupil.toString()
        else:
            print "Cannot print"

        print "\nHorizontal Right Pupil: "
        if patient.horizontal.right.eyePupil != None:
            patient.horizontal.right.eyePupil.toString()
        else:
            print "Cannot print"

        print "\nVertical Left Pupil: "
        if patient.vertical.left.eyePupil != None:
            patient.vertical.left.eyePupil.toString()
        else:
            print "Cannot print"
              
        print "\nVertical Right Pupil: "
        if patient.vertical.right.eyePupil != None:
            patient.vertical.right.eyePupil.toString()
        else:
            print "Cannot print"

    print "Here are the eye photo paths: "
    print getEyePhotos()

    print "Beginning eye analysis...\n"
    patient.analyzeEyes(0.17)
    
    allInfo = patient.getInfo()
    allDefects = patient.getDefects()

    # Print all the results
    for key in  allDefects.keys():
        print "[" + key + "]" + " = " + str(allDefects[key] )
    print "\n"
    for key in  allInfo.keys():
        print "[" + key + "]" + " = " + str(allInfo[key] )
    print "\n"
    
    #Added method just for testing. Can be deleted or commented out in actual
    # working code.
    removePupilPhoto()

    removePupilPhoto()

