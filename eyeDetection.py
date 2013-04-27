# Core Code: Eye Detection algorithm written by Janne Parkkila
# More Info: http://japskua.wordpress.com/about/
# Blog Post with code: http://japskua.wordpress.com/2010/08/04/detecting-eyes-with-python-opencv/

# The following program has been modified to work for UCSD's DVS team
# More info: http://globalties.ucsd.edu/dvs.html
# Github repo: https://github.com/UCSD-TIES/DVS-Python

import cv
import time
import Image


#NOTES
#   Right Now this code is somewhat slow and has not been tested
#     so it may not be very accurate.
#   Also, it could use a lot more commenting for new developers.


#Load the image to analyze

fileLocation = raw_input("Please designate the full path" +
                         "to the file you want to analyze\n")
result = cv.LoadImage(fileLocation)

def Load():

   return (faceCascade, eyeCascade)

def Display(image):
   cv.NamedWindow("Red Eye Test")
   cv.ShowImage("Red Eye Test", image)
   cv.WaitKey(0)
   cv.DestroyWindow("Red Eye Test")

def DetectRedEyes(image, faceCascade, eyeCascade):
   min_size = (20,20)
   image_scale = 2
   haar_scale = 1.2
   min_neighbors = 2
   haar_flags = 0

   # Allocate the temporary images
   gray = cv.CreateImage((image.width, image.height), 8, 1)
   smallImage = cv.CreateImage((cv.Round(image.width / image_scale),cv.Round (image.height / image_scale)), 8 ,1)

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

   cv.SetImageROI(image, (pt1[0],
pt1[1],
pt2[0] - pt1[0],
int((pt2[1] - pt1[1]) * 0.7)))
   eyes = cv.HaarDetectObjects(image, eyeCascade,
cv.CreateMemStorage(0),
haar_scale, min_neighbors,
haar_flags, (15,15))

   if eyes:
      # For each eye found
      for eye in eyes:
         # Draw a rectangle around the eye
         cv.Rectangle(image,
(eye[0][0],
eye[0][1]),
(eye[0][0] + eye[0][2],
eye[0][1] + eye[0][3]),
cv.RGB(255, 0, 0), 1, 8, 0)

   cv.ResetImageROI(image)
   return image

#NOTE: You will need to modify this path to point to the dir with your cascades
faceCascade = cv.Load("C:/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
eyeCascade = cv.Load("C:/opencv/data/haarcascades/haarcascade_eye.xml")

img = result
image = DetectRedEyes(img, faceCascade, eyeCascade)
cv.ShowImage("camera", image)
cv.WaitKey(0)
cv.DestroyWindow("camera")
