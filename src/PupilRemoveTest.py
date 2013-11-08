 
import cv2.cv as cv

DEBUG = True
 
def pupilRemove(image, region):
        """ Crops the eye photo to show only the pupil
            and then returns it.

        Args:
            tuple region - the coordinates of the pupil circle in
            the form (centerX, centerY, radius)

        Return:
            photo  - TODO: I'm not sure of the type
        """
        # Converting to (topLeftX, topLeftY, width, length)
        if region[0]-region[2] < 0:
            topLeftX = 0
        else:
            topLeftX = region[0]-region[2]

        if region[1]-region[2] < 0:
            topLeftY = 0
        else:
            topLeftY = region[1]-region[2]

        if region[2] < 0:
            width = 0
        else:
            width = region[2] + region[2]

        if region[2] < 0:
            length = 0
        else:
            length = region[2]+region[2] 

        crop = (topLeftX, topLeftY, width, length)
        if DEBUG:
            print "Region passed to pupil remove: " + str(region)
            print "And here's crop: " + str(crop)
            print "Before crop we have type: " + str(type(image))
            print image
            cv.ShowImage("We're cropping", image)
            cv.WaitKey(0)
            cv.DestroyWindow("We're cropping")
        if crop[0] < 0:
            crop[0] = 0
        if crop[1] < 0:
            crop[1] = 0
        if crop[2] < 0:
            crop[2] = abs(crop[2])
        else:
            pupil = cv.GetSubRect(image, crop)
            if DEBUG:
                print "After crop we have type: " + str(type(pupil))
                cv.ShowImage("Cropped", pupil)
                cv.WaitKey(0)
                cv.DestroyWindow("Cropped")
            return pupil
        return None

############ Main ##################

# Load the photo from file
# give it to pupilRemove


pupilRemove(cv.LoadImage("C:\Users\Shannon\Documents\GitHub\DVS-Python\src\pics\Red06.jpg"),(100,100,10))