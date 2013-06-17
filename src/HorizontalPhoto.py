""" A class to perform actions on a horizontal photo of a face
    This class inherits from it's parent FacePhoto
"""
from FacePhoto import *

class HorizontalPhoto(FacePhoto):

    # Simply inherits all methods from FacePhoto
    def __init__(self, photo, path):
        """ Initialize the attributes of a FacePhoto

            This calls FacePhoto's __init__
            method to populate the eyes, etc.

            Args:
              photo photo - a photo of a face

            Return:
              None
        """
        # call FacePhoto(super)'s  init
        FacePhoto.__init__(self, photo, path)

        
