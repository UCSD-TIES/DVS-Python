""" A class to perform actions on a vertical photo of a face
    This class inherits from it's parent FacePhoto
"""
from FacePhoto import *
import cv2.cv as cv
import cv2
import numpy as np

class VerticalPhoto(FacePhoto,object):

    def __init__(self, photo):
        """ Initialize the attributes of a FacePhoto

            This constructor rotates the photo so that we can process
            it as we would a vertical photo then calls FacePhoto's __init__
            method to populate the eyes, etc.

            Args:
              photo photo - a photo of a face

            Return:
              None
        """
        # Rotate photo
        # NOTE: Not sure if this will rotate the photo to be right side
        #       up or upside
        photo = self.rotateImage(photo,90)
        # call FacePhoto(super)'s  init
        super(VerticalPhoto,self).__init__(photo)

    def rotateImage(self, image, angle):
        image0 = image
        if hasattr(image, 'shape'):
            image_center = tuple(np.array(image.shape)/2)
            shape = tuple(image.shape)
        elif hasattr(image, 'width') and hasattr(image, 'height'):
            image_center = tuple(np.array((image.width/2, image.height/2)))
            shape = (image.width, image.height)
        else:
            raise Exception, 'Unable to acquire dimensions of image for type %s.' % (type(image),)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle,1.0)
        image = np.asarray( image[:,:] )

        rotated_image = cv2.warpAffine(image, rot_mat, shape, flags=cv2.INTER_LINEAR)

        # Copy the rotated data back into the original image object.
        cv.SetData(image0, rotated_image.tostring())

        return image0

        

        
        
