""" horizontalImg and verticalImg are pictures of the patient passed from the UI
"""
class Patient:
    def __init__(self, horizontalImg, verticalImg):
        self.Horizontal = HorizontalPhoto(horizontalImg)
        self.Vertical = VerticalPhoto(verticalImg)

    def analyzeEyes(self):
        results = self.strabismus()
        results.append( self.astigmatism())
        results.append( self.cataracts())
        return results

    def strabismus(self):
        # strabismus detection logic goes here
        return "Strabismus detection called"

    def astigmatism(self):
        # astigmatism logic goes here
        return "Astigmatism detection called"

    def cataracts(self):
        # cataracts logic goes here
        return "Cataracts detection called"




    
        
