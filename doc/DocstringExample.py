""" This is a short description of what this file does. This description should
    be one or two lines
"""

class DocString:
""" If this is a class list the attributes here:

    type name - This is a description of an attribute.
    int awesome - This is an example of what a real attribute description
                  would be like
"""

# NOTE: If there's a programatic choice you've made that isn't obvious
#       or anything else that a developer needs to make note of make
#       a comment like this prefaced by "NOTE:".

    def __init__():
        """ If the method is obvious just leave a one line docstring """
        awesome = 0

    def makeDocStringAwesome(awesomeLevel):
        """ This is a short one line description of the method.

        A longer description of the method's function that will include
        more detail and may span multiple lines. This particular method
        makes DocString's awesome attribute as awesome as the user specifies.
        Negative awesomeness levels are not accepted.

        Args:
            int awesomeLevel - the level of awesome the user would like
                               DocString to be.
                               
        Return:
            bool - True if awesome was set. False if awesome was not set because
                   awesomeLevel was invalid.
        """
        if awesomeLevel < 0:
            return False
        # Short comments describing functionality can be written like this.
        awesome = awesomeLevel
        return True
