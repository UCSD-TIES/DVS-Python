""" PLEASE NOTE: This is currently a psuedoclass and is not meant to be valid code
"""
# photoImg is a photo of a face

class FacePhoto:

    #Note: Error checking and raising is not accounted for in psudeoclasses

    def __init__(self, photoImg):
        getEyes(photoImg)

    def getFace(self):
        # face detection logic goes here
        # returns face region
        return "getFace successfully called"
        

    def getEyes(photoImg):
        # eyeDetection.py logic goes here
        # if there's 2 regions
        #     set left and right region
        # else
        #     don't set the left and right regions
        return "getEyes successfully called"

    def setEyes(leftRegion, rightRegion):
        setLeftEye(leftRegion)
        setRightEye(rightRegion)
        return "setEyes successfully called"
        
    def setLeftEye(region):
        # sets or resets left.jpg, leftRegion, and leftCrescent
        return "setLeftEye successfully called"

    def setRightEye(region):
        # sets or resets right.jpg, rightRegion, and rightCrescent
        return "setRightEye successfully called"

    def getLeftEye():
        # return all left eye vars
        return "getLeftEye successfully called"

    def getRightEye():
        # return all right eye vars
        return "getRightEye successfully called"
    
    def getLeftImg():
        #return leftImg
        return "getLeftImg successfully called"

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

    
    
