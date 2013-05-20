""" A class to perform actions on a vertical photo of a face
    This class inherits from it's parent FacePhoto
"""
from FacePhoto import *

class VerticalPhoto(FacePhoto):

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
        photo.rotate(90)
        # call FacePhoto(super)'s  init
        super(photo)
