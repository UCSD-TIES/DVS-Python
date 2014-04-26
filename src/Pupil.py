""" A class to perform actions on an eye. A pupil can get its own center and its
own crescent region
"""
from Eye import *
import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint
import os


DEBUG = False

class Pupil:
  """ This class has attributes:
      cv2.cv.cvmat pupilPhoto - a cropped photo showing only the pupil
      tuple pupil - a tuple representing the circluar region of the pupil. The tuple
                    is formatted as such: (centerX, centerY, radius)
      tuple center - the center point of the pupil region formatted as (x,y)
      tuple whiteDotCenter - the center of the whiteDot formatted as (x,y)
      float crescent - the area of the pupil's crescent region
  """

  def __init__(self, newPupilPhoto, pupilRegion):
    """ Initilaizes a pupil's region then calls findCenter and
        findCrescent() in an attempt to set the remaing attributes.
    """
    # Set the cropped photo of the pupil
    self.pupilPhoto = newPupilPhoto
    # Write the pupilPhoto to disk in order to debug the
    # single-segment buffer object error findCrescent is currently doing
    # TODO: Change code so we don't have to do a janky one time write to disk
    if DEBUG:
        print "PupilPhoto is of type: " + str(type(newPupilPhoto))
    cv2.imwrite("PUPILPHOTO.jpg",np.asarray(newPupilPhoto))

    # Set the pupil region to the region passed in
    self.pupil = pupilRegion

    # Initialize the other attributes to None so that they exist
    self.center = None
    if pupilRegion != None:
      self.center = (pupilRegion[0], pupilRegion[1])
    self.whiteDotCenter = None
    self.crescent = None
    # Set the attributes initialized to None by finding them
    self.findCrescent()
    self.findWhiteDot()

  def findWhiteDot(self):
    ## The code here is based on findPupil() from Eye.py
    """ Detects a whiteDot within a pupil region.

    Uses opencv libarary methods to detect the white dot in the center of the 
    pupil caused by the reflection of the flash.

    Algorithm Overview:
        
            Load the source image.
            GrayScale
            Invert it.
            Convert to binary image by thresholding it.
            Find all blobs.
            Remove noise by filling holes in each blob.
            Get blob which is big enough and has round shape.

    Then initializes whiteDot to the region found and sets whiteDotCenter. 
    Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    
    # Image Processing
    
    # read the im from disc using absolute path

    im = cv2.imread(os.path.join(os.path.dirname(__file__), 'PUPILPHOTO.jpg'))

    # TODO - change all the random explicit numbers in this method
    #         to descriptively named class level variables
    if DEBUG:
        print "im is of type: " + str(type(im))
    im2 = im.copy()
    imblur = cv2.blur(im,(3,3))
    imgray = cv2.cvtColor(imblur,cv2.COLOR_BGR2GRAY)

    if DEBUG:
        cv.ShowImage("Grayscaled", cv.fromarray(imgray)) # Grayscale Picture
        cv.WaitKey(0)
        cv.DestroyWindow("Grayscaled")
    ret,thresh = cv2.threshold(imgray,127,255,0)  # ret : type float. thresh: type :numpy.ndarray
    
    if DEBUG:
        cv.ShowImage("Binary", cv.fromarray(thresh))    # Binary Picture
        cv.WaitKey(0)
        cv.DestroyWindow("Binary")
    
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if DEBUG:
        print("Number of Contours Found: " + str(len(contours)))
        cv2.drawContours(im,contours,-1,(0,255,0),0)  # Final argument for drawContours() : 0 = Outline, -1 = Fill-In
        cv.ShowImage("All Contours", cv.fromarray(im))
        cv.WaitKey(0)
        cv.DestroyWindow("All Contours")

    # Finding center coordinates of photo
    photoCenterX = len(im[0])/2
    photoCenterY = len(im)/2

    if DEBUG:
        print("Photo's Center Coordinates: (" + str(photoCenterX) + ", " + str(photoCenterY) + ")" )


    min_area = maxint

    
    ## This is finding WhiteDot by comparing contour centroids
    shortestDist = maxint
    closestCnt = contours[0];
    closestX = closestY = 0
    for cnt in contours:
        M = cv2.moments(cnt)
        ## Ignores all contours with M00 = 0, 
        ## because that will cause divide by 0 error
        if (M['m00'] != 0.0):
            centroid_x = int(M['m10']/M['m00'])
            centroid_y = int(M['m01']/M['m00'])
            if DEBUG:
                print cnt
                print("\n")
                print M['m10'], M['m00']
                print M['m01'], M['m00']
                print ("\n\n")
        
            dist = np.sqrt(np.square(centroid_x - photoCenterX) + np.square(centroid_y - photoCenterY))
            if DEBUG:
                print ("Distance to center = " + str(dist))

            ## At the end of the loop, the closest contour to center of image is stored
            if (dist < shortestDist):
                closestX = centroid_x
                closestY = centroid_y
                shortestDist = dist
                closestCnt = cnt

    self.setWhiteDotCenter( (closestX,closestY) )

    if DEBUG:           
        #print (shortestDist)
        print ("Closest Contour: (" + str(closestX) + ", " + str(closestY) + ")")
        
        ## This only prints the one contour that is passed, on top of the image
        cv2.drawContours(im,[closestCnt],0,(255,0,0),-1)
        cv2.drawContours(im2, [closestCnt], 0, (255,0,0), 1)
        cv.ShowImage("White Dot with Contours", cv.fromarray(im))
        cv.WaitKey(0)
        cv.DestroyWindow("White Dot with Contours")
        cv.ShowImage("White Dot only", cv.fromarray(im2))
        cv.WaitKey(0)
        cv.DestroyWindow("White Dot only")



  def findCrescent(self):
    """ Detects a crescent within a pupil region.

    Uses opencv libarary methods to detect a crescent. Then initializes crescent
    to the area of the region found. Returns false if any errors are encountered

    Args:
      None

    Return:
      bool - True if there were no issues. False for any error
    """
    if DEBUG:
        print "self.pupilPhoto is of type: " + str(type(self.pupilPhoto))
    # Currently self.pupilPhoto is stored as a cvmat so we need to convert to a 
    # numpy array before working with it.
    #im = np.asarray(self.pupilPhoto)

    # read the im from disc using absolute path
    im = cv2.imread(os.path.join(os.path.dirname(__file__), 'PUPILPHOTO.jpg'))


    if DEBUG:
        print "im is of type: " + str(type(im))
    imblur = cv2.blur(im,(3,3))
    imgray = cv2.cvtColor(imblur,cv2.COLOR_BGR2GRAY)
    # TODO Take away magic (ex: 127,255,0) numbers here and make pretty
    # Variables at the top
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if DEBUG:
        print "Contours is of type: " + str(type(contours))
        print "Contours is of id: " + str(hex(id(contours)))
        print "Countours: " + str(contours)
        cv.ShowImage("Thresholded", cv.fromarray(thresh))
        cv.WaitKey(0)
        cv.DestroyWindow("Thresholded")
        cnt = contours[0]
        len(cnt)
        cv2.drawContours(im,contours,-1,(0,255,0),-1)
        cv.ShowImage("Coutours", cv.fromarray(im))
        cv.WaitKey(0)
        cv.DestroyWindow("Contours")

    max_area = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            best_cnt = cnt
            
    #set the max_area found into the actual structure
    self.setCrescent(max_area)

    #show it, or exit on waitkey
    #cv2.imshow('imblur',imblur)
    if DEBUG:
        #find centroids of best_cnt
        M = cv2.moments(best_cnt)
        cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
        cv2.circle(imblur, (cx,cy),5,255,-1)

        cv2.imshow('thresh', thresh)
        if cv2.waitKey(33) == 27:
            cv.DestroyAllWindows()

        cnt = contours[0]
        len(cnt)
        cv2.drawContours(imblur,contours,-1,(0,255,0),-1)
        cv2.circle(imblur, (cx,cy),5,255,-1)
        cv.ShowImage("Contour Shading", cv.fromarray(imblur))
        #cv.WaitKey(0)
        #cv.DestroyWindow("Testing")
        cv.WaitKey(0)
        cv.DestroyAllWindows()

  def toString(self):
    print "tuple pupil(in the form (centerX, centerY, radius)): " + str(self.pupil)
    print "tuple center(in the form (centerX, centerY, radius)): " + str(self.center)
    print "tuple whiteDotCenter(in the form (x,y)): " + str(self.whiteDotCenter)
    print "float crescent (the area of the crescent): " + str(self.crescent)
    

#################### Getters ##################################

  def getPupilRegion(self):
    """ Returns a tuple representing the pupil """
    return self.pupil

  def getCenter(self):
    """ Returns a tuple representing the center of the pupil """
    return self.center

  def getWhiteDotCenter(self):
    """ Returns a tuple representing the center of the whiteDot """
    return self.whiteDotCenter

  def getCrescent(self):
    """ Returns a region representing the crescent """
    return self.crescent

  def getPupilArea(self):
    """ Returns a float representing the area of the pupil """
    if self.pupil != None:
        return math.pi * self.pupil[2] * self.pupil[2] # pi * r^2
    else:
        # TODO: Implement a more graceful way of dealing with this error
        print "Error: Pupil is not defined"

#################### Setters ##################################

  def setPupilRegion(self,newRegion):
    """ Sets the pupil's region to the tuple passed in as argument """
    self.pupil = newRegion

  def setCenter(self,newCenter):
    """ Sets the pupil's center to the tuple passed in as argument """
    self.center = newCenter

  def setWhiteDotCenter(self,newCenter):
    """ Sets the whiteDot's center to the tuple passed in as argument """
    self.whiteDotCenter = newCenter

  def setCrescent(self,newCrescent):
    """ Sets the pupil's crescent to the region passed in as argument """
    self.crescent = newCrescent
