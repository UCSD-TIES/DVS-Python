" PLEASE NOTE: This is currently a psuedoclass and is not meant to be valid code

""" Controller PsuedoCode
thisPatient =  new Patient(Horizontal(photo from UI),   Vertical(photo from UI));
  // pass regions that horizontal and vertical’s  regions to the UI
  if user confirms
     continue
  else if user resets regions
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
