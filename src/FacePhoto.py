""" PLEASE NOTE: This is currently a psuedoclass and is not meant to be valid code
"""
# photo.jpg is a photo of a face

class FacePhoto:

    #Note: Error checking and raising is not accounted for in psudeoclasses

    __init__(self, photo.jpg):
        getEyes(photo.jpg)

    getFace(self):
        # face detection logic goes here
        # returns face region
        

    getEyes(photo.jpg):
        # eyeDetection.py logic goes here
        # this method will populate left.jpg
        #                           right.jpg
        #                           leftRegion (region of the original
        #                                       photo that represents the left eye)
        #                           rightRegion
        #                           leftCrescent (a crescent object)
        #                           rightCrescent ( a crescent object)

    setLeftEye(region):
        # sets or resets left.jpg, leftRegion, and leftCrescent

    setRightEye(region):
        # sets or resets right.jpg, rightRegion, and rightCrescent

    getLeftEye():
        # return all left eye vars

    getRightEye():
        # return all right eye vars
    
    getLeftJPG():
        return left.jpg

    getLeftRegion():
        return leftRegion

    getLeftCrescent():
        return leftCrescent

    getRightJPG():
        return right.jpg

    getRightRegion():
        return rightRegion

    getRightCrescent():
        return rightCrescent

    setLeftJPG(photo):
        this.leftJPG = photo

    setLeftRegion(region):
        this.leftRegion = region

    setLeftCrescent(keypoints):
        this.leftCresent.setKeypoints(keypoints)

    setRightJPG(photo):
        this.rightJPG = photo

    setRightRegion(region):
        this.rightRegion = region

    setRightCrescent(keypoints):
        this.rightCrescent.setKeypoints(keypoints)

    
    
