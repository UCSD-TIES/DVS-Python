"""" PLEASE NOTE: This is currently a psuedoclass and is not meant to be valid code

"""
from Patient import Patient

# in this script we assume the UI has passed us vertImg and horizImg,
#   two image objects

# Initialize the Patient object
thisPatient = Patient( vertImg, horizImg)

# Display the horizontal photo with the eye regions that we
#   detected
#for region in thisPatient.vertical.getRegions():

"""
Controller PsuedoCode
thisPatient =  new Patient(Horizontal(photo from UI),   Vertical(photo from UI));
  // pass regions that horizontal and vertical’s  regions to the UI
  if user confirms
     continue
  else if user resets regions
     if the user gives != 2 regions
        reprompt
     else
        reset the relevant regions using setter methods
  // crescents and pupils will be detected when the new 
  //    patient is made
  // pass the keypoints of all the eyes to the UI
  if the user confirms
     continue
  else if user resets keypoints
     reset keypoints using setter methods
 print thisPatient.analyzeEyes();

 """
     
