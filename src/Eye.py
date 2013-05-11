""" A class to perform actions on a eye. A eye can get its own pupil and
    its own keypoints or sclera (depending on the algorithm)
"""

class Eye:
""" This class has attributes :
      img eyePhoto - a cropped photo of the left eye
      region eyeRegion - a region that represents the exact location of the eye
      Pupil eyePupil - the eye's pupil
      region eyeSclera - the eye's sclera region
      point top - the keypoint of the eye located at the highest point at which
                  the top eyelid and the eyeball meet
      point bottom - the keypoint of the eye located at the lowest point at which
                     the lower eyelid and the eyeball meet
      point inner - the keypoint of the eye located nearest the tearduct
      point outer - the keypoint of the eye located on the outermost crease
                    of the eye
"""   

    def __init__(self):
        eyePhoto = None
        eyeRegion = None

    def findPupil():
        # find the pupil and initializes the pupil object
        # find the pupil's region

    def findSclera():
        # find the sclera and initilizes the sclera region

    def findKeypoints():
        # find top, bottom, inner, and outer
        
    ######## getters and setters for all attributes ###########

    ############# Old defunk code that needs to be deleted ########
    def getEyePhoto():
        #return leftImg
        return "getEye successfully called"

    def getLeftRegion():
        # return leftRegion
        return "getLeftRegion successfully called"

    def getLeftCrescent():
        #return leftCrescent
        return "getLeftCrescent successfully called"

    def getRightImg():
        #return right.jpg
        return "getRightImg successfully called"

    def getRightRegion():
        #return rightRegion
        return "getRightRegion successfully called"

    def getRightCrescent():
        #return rightCrescent
        return "getRightCrescent successfully called"

    def setLeftImg(photo):
        #this.leftImg = photo
        return "setLeftImg successfully called"

    def setLeftRegion(region):
        #this.leftRegion = region
        return "setLeftRegion successfully called"

    def setLeftCrescent(keypoints):
        #this.leftCresent.setKeypoints(keypoints)
        return "setLeftCrescent successfully called"

    def setRightImg(photo):
        #this.rightImg = photo
        return "setRightImg successfully called"

    def setRightRegion(region):
        #this.rightRegion = region
        return "setRightRegion successfully called"

    def setRightCrescent(keypoints):
        #this.rightCrescent.setKeypoints(keypoints)
        return "setRightCrescent successfully called"

