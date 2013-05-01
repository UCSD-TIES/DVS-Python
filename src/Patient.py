""" PLEASE NOTE: This is currently a psuedoclass and is not meant to be valid code
"""
# horizontal.jpg and vertical.jpg are pictures of the patient passed from the UI

class Patient:
    __init__(self, horizontal.jpg, vertical.jpg):
        self.Horizontal = HorizontalPhoto(horizontal.jpg)
        self.Vertical = VerticalPhoto(vertical.jpg)

    analyzeEyes(self):
        results = self.strabismus()
        results.append( self.astigmatism())
        results.append( self.cataracts())
        return results

    strabismus(self):
        # strabismus detection logic goes here

    astigmatism(self):
        # astigmatism logic goes here

    cataracts(self):
        # cataracts logic goes here




    
        
