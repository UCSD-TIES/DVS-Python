import cv2

'''
must catch error if eyes not found in eye detection software of image
the following program simply crops out two regions of interest
'''

# test image here
image = cv2.cv.LoadImage("C:\Users\JT\Desktop\image1.jpg")

# test variables for getting Region of Interest
a=50
b=150
c=250
d=350

a2=100
b2=200
c2=300
d2=400

# cast exception eyes not found
# try
# except NullPointerException as e
# print "eye regions not found"

# crop from region
left_eye = cv2.cv.GetSubRect(image,(a,b,c,d))
right_eye = cv2.cv.GetSubRect(image,(a2,b2,c2,d2))

# display cropped images
cv2.cv.ShowImage('left eye', left_eye)
cv2.cv.ShowImage('right eye', right_eye)
cv2.waitKey(0)
cv2.destroyAllWindows()

