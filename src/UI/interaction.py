import wx, os

IMGMASK = "JPEG Files(*.jpg;*.jpeg;*.jpe;*.jfif) " \
          "|*.jpg; *.jpeg; *.jpe; *.jfif|" \
          "Raw Files |*.cr2; *crw|" \
          "All Files |*.*"

class interaction:

    uploadText = ""

    def __init__(self):
        uploadText = "Please upload an image"


    def getFilePath(self):
        return self.uploadText





##########################BUTTONS##############################
    # upload button
    def upload(self, panel):
       #Pops up box for user to upload image
       upBox = wx.FileDialog(panel, "Choose a file", os.getcwd(), "",
                             IMGMASK, wx.OPEN)
       if upBox.ShowModal() == wx.ID_OK:
          uploadText = upBox.GetPath()
       else:
          uploadText = "Please upload an image"
