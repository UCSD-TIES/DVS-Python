import cv2.cv as cv
import cv2
import numpy as np
from PIL import Image
import PIL.ImageOps
import math
from sys import maxint

## Toggle bySize for different WhiteDot Approach method
## True -> find by center coordinates,  False -> find by contour size.
byDist = True

# Circle detection parameters
CIRCLE_RESOLUTION_RATIO = 1
# The minimum distance between circle centerpoints
CIRCLE_MIN_DISTANCE = 32
# I'm not exactly sure what the THRESHOLD ones do. See link for more info:
# http://www.adaptive-vision.com/en/technical_data/documentation/3.0/filters/FeatureDetection/cvHoughCircles.html
CIRCLE_THRESHOLD_1 = 10
# The accumulator threshold. The higher this is the less circles you get.
CIRCLE_THRESHOLD_2 = 2
CIRCLE_MIN_RADIUS = 10
CIRCLE_MAX_RADIUS = 500

# Circle drawing parameters
CIRCLE_COLOR = (0, 0, 255)
THICKNESS = 3
LINE_TYPE = 8
SHIFT = 0

# Image Processing
# Note : change the directory of the photo
im = cv2.imread('/home/arvind/DVS-Python/src/pics/redeye1.PNG')  # im type: numpy.ndarray
im2 = im.copy()
imblur = cv2.blur(im,(3,3))
imgray = cv2.cvtColor(imblur,cv2.COLOR_BGR2GRAY)
## cv.ShowImage("Test", cv.fromarray(imgray)) # Grayscale Picture
ret,thresh = cv2.threshold(imgray,127,255,0)  # ret : type float. thresh: type :numpy.ndarray
## cv.ShowImage("Test", cv.fromarray(thresh))    # Binary Picture
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("Number of Contours Found: " + str(len(contours)))
cv2.drawContours(im,contours,-1,(0,255,0),0)  # Final argument for drawContours() : 0 = Outline, -1 = Fill-In
cv.ShowImage("All Contours", cv.fromarray(im))
cv.WaitKey(0)
cv.DestroyWindow("All Contours")

# Finding center coordinates of photo
photoCenterX = len(im[0])/2
photoCenterY = len(im)/2
print("Photo's Center Coordinates: (" + str(photoCenterX) + ", " + str(photoCenterY) + ")" )


min_area = maxint

if byDist:
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
            ''' ## Print Statements for debugging
            print cnt
            print("\n")
            print M['m10'], M['m00']
            print M['m01'], M['m00']
            print ("\n\n")
            '''
            dist = np.sqrt(np.square(centroid_x - photoCenterX) + np.square(centroid_y - photoCenterY))
            ## print ("Distance to center = " + str(dist))
            ## At the end of the loop, the closest contour to center of image is stored
            if (dist < shortestDist):
                closestX = centroid_x
                closestY = centroid_y
                shortestDist = dist
                closestCnt = cnt
                
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



## JT's way, i image is just the pupil only then should work
else:
    ## This is finding WhiteDot by comparing contour sizes:
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            min_area = area
            best_cnt = cnt
    #find centroids of best_cnt
    M = cv2.moments(best_cnt)
    cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
    cv2.circle(imblur, (cx,cy),5,255,-1)
    
    #show it, or exit on waitkey
    #cv2.imshow('imblur',imblur)
    cv2.imshow('thresh', thresh)
    if cv2.waitKey(33) == 27:
        cv.DestroyAllWindows()

    cv2.drawContours(imblur,contours,-1,(0,255,0),-1)
    cv2.circle(imblur, (cx,cy),5,255,-1)
    cv.ShowImage("Contour Shading", cv.fromarray(imblur))
    #cv.WaitKey(0)
    #cv.DestroyWindow("Testing")
    cv.WaitKey(0)
    cv.DestroyAllWindows()