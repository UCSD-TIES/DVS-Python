import wx, os
from Controller import *
#use makepatient method from controller

IMGMASK = "JPEG Files(*.jpg;*.jpeg;*.jpe;*.jfif) " \
	"|*.jpg; *.jpeg; *.jpe; *.jfif|" \
	"Raw Files |*.cr2; *crw|" \
	"All Files |*.*"

class interaction():
	def __init__(self):
		self.patient = None          # This might not be used
		self.horizontalPath = None   # Path of horizontal image
		self.verticalPath = None     # Path of vertical image

		# These bitmaps are needed to draw on, can't draw on img Ctrls
		self.hBitMap = None
		self.vBitMap = None

	# BUTTONS

	# upload button, 1st page
	# Args: page - the panel the image is on (will be page 1)
	#       imgCtrl - Either veritcal or horizontal
	#       text - Text control - either vertical or horizontal
	#       orientation - specify which image is uploading, 1 for vertical and 0 for horizontal
	def upload(self, page, imgCtrl, text, orientation):
	  	# pops up box for user to upload image
	  	upBox = wx.FileDialog(page, "Choose an image.", os.getcwd(), "",
							IMGMASK, wx.OPEN)

	  	# Once the user hits the "OK" button
	  	if upBox.ShowModal() == wx.ID_OK:
			upPath = upBox.GetPath()            # Gets the path of the uploaded file
			text.SetValue(upPath)               # Sets path into the text control

		# Depending on which image is being uploaded, sets interaction object's
		# data field and paints the image onto the page.
	  	if orientation == 0:
	  		self.upPaint(page, upPath, imgCtrl, orientation)
	  		self.horizontalPath = upPath
	  	elif orientation == 1:
	  		self.upPaint(page, upPath, imgCtrl, orientation)
	  		self.verticalPath = upPath
		  
	# reset button, 1st page
	# Args: page - panel to clear images and paths (will be page 1)
	#       imgCtrl1 - vertical or horizontal image control to be cleared
	#       imgCtrl2 - Other control
	#       text1 - text control to be cleared
	#       text2 - other text control to be cleared
	def reset(self, page, imgCtrl1, imgCtrl2, text1, text2):
		empty = wx.EmptyImage(440,440)     # Create empty image

		# Sets the 2 image controls to empty
		imgCtrl1.SetBitmap(wx.BitmapFromImage(empty))
		imgCtrl2.SetBitmap(wx.BitmapFromImage(empty))

		# Resets path names
		text1.SetValue("Please upload an image.")
		text2.SetValue("Please upload an image.")
		page.Refresh()

		# Deletes interaction object's data 
		self.horizontalPath = None
		self.verticalPath = None
		self.hBitMap = None
		self.vBitMap = None

	# helper method for upload button, resizes and shows uploaded image
	# Args: page - the page passed in from upload() (page 1)
	#       upPath - path of the image to be shown
	#       imgCtrl - holds the newly shown image
	#       orientation - vertical or horizontal, taken from upload()
	def upPaint(self, page, upPath, imgCtrl, orientation):
		# Makes a new image using the file path
		newImg = wx.Image(upPath, wx.BITMAP_TYPE_ANY)

		# Getting width and height of this image
		width = newImg.GetWidth()
		height = newImg.GetHeight()
		maxSize = 440

	  # scale the image to preserving the aspect ratio
		'''   UNUSED - FOR NOW
	  	if width > height and width > maxSize:
			newWidth = maxSize
			newHeight = height / (width / float(maxSize))
	  	elif width > height and width < maxSize:
			newWidth = maxSize
			newHeight = height * (width / float(maxSize))
	  	elif width == maxSize:
			newWidth = maxSize

	  	if height > width and height > maxSize:
			newHeight = maxSize
			newWidth = width / (height / float(maxSize))
	  	elif height > width and height < maxSize:
			newHeight = maxSize
			newWidth = width * (height / float(maxSize))
	  	elif height == maxSize:
			newHeight = maxSize
		'''

		# Scales the image
	  	# This scaling works, but may have problems in future
	  	if width > height:
			newWidth = maxSize
		  	newHeight = maxSize * height/ width
	  	else:
		  	newHeight = maxSize
		  	newWidth = maxSize * width/ height
		
		# Finishes scaling and sets img into the imgCtrl  
	  	newImg = newImg.Scale(newWidth,newHeight)
	  	imgCtrl.SetBitmap(wx.BitmapFromImage(newImg))

	  	# Stores data for interaction obj depending on orientation
	  	if orientation == 0:
	  		self.hBitMap = wx.BitmapFromImage(newImg)
	  	elif orientation == 1:
	  		self.vBitMap = wx.BitmapFromImage(newImg)
	  	page.Refresh()

	# Next Button for first page
	# Args: hPhotoTxt - text control for horizontal image
	#       vPhotoTxt - text control for vertical image
	#       page1 - 1st page
	#       page2 - 2nd page
	#       hImgCtrl - horizontal image control of 2nd page
	#       vImgCtrl - vertical image control of 2nd page
	def next1(self, hPhotoTxt, vPhotoTxt, page1, page2, hImgCtrl, vImgCtrl):
		'''    These are checks that are turned off for convenience
		pleaseText = "Please upload an image."
		if hPhotoTxt == pleaseText and vPhotoTxt == pleaseText:
			errorTxt1 = "No Images Detected, Please Enter Images"
			errMsg1 = wx.MessageDialog(page, errorTxt1, "No Images Detected", wx.OK)
			errMsg1.ShowModal()
			errMsg1.Destroy()
		# When no horizontal image is entered
		elif hPhotoTxt == pleaseText:
			errorTxt2 = "No Horizontal Image Detected, Please Enter a Horizontal Image"
			errMsg2 = wx.MessageDialog(page, errorTxt2, "No Horizontal Image", wx.OK)
			errMsg2.ShowModal()
			errMsg2.Destroy()
		# When no vertical image is entered
		elif vPhotoTxt == pleaseText:
			errorTxt3 = "No Vertical Image Detected, Please Enter a Vertical Image"
			errMsg3 = wx.MessageDialog(page, errorTxt3, "No Vertical Image", wx.OK)
			errMsg3.ShowModal()
			errMsg3.Destroy()
		# Move to next panel
		else:
		'''
		self.patient = makePatient(self.horizontalPath, self.verticalPath)
		coors = getEyeCoors(self.patient)
		print coors

		# Paints the images of page 2 and hides the first page
		self.upPaint(page2, self.verticalPath, vImgCtrl, 1)
		self.upPaint(page2, self.horizontalPath, hImgCtrl, 0)
		page1.Hide()

		# Drawing rectangle with MemoryDC
		mdc = wx.MemoryDC()
		
		mdc.SelectObject(self.hBitMap)    # sets a bitmap to e modified
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
		mdc.DrawRectangle(coors[0][0], coors[0][1], coors[0][2], coors[0][3])
		mdc.DrawRectangle(coors[1][0], coors[1][1], coors[1][2], coors[1][3])
		hImgCtrl.SetBitmap(self.hBitMap)  # Sets modified bitmap back into the img ctrl

		mdc.SelectObject(self.vBitMap)    # sets a bitmap to e modified
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
		mdc.DrawRectangle(coors[2][0], coors[2][1], coors[2][2], coors[2][3])
		mdc.DrawRectangle(coors[3][0], coors[3][1], coors[3][2], coors[3][3])
		vImgCtrl.SetBitmap(self.vBitMap)  # Sets modified bitmap back into the img ctrl

		mdc.SelectObject(wx.NullBitmap)   # MemoryDC must be set back to a null bitmap when done
		self.ShowYourself(page2)          # Shows 2nd page
	'''
	UNUSED
	# Painting the Rectangle on the 2nd page
	def OnPaint(self, control):
		draw = wx.PaintDC(control)
		draw.Clear()
		draw.SetBrush(wx.Brush('#000000', wx.TRANSPARENT))
		draw.DrawRectangle(10, 10, 100, 100)
	'''
    # The "No" button on page2 - Moves from page 2 to 3
    # Args: page2 - 2nd page
    #       page3 - 3rd page
    #       hImgCtrl - 3rd page's horizontal image control
    #       vImgCtrl - 3rd page's vertical image control
	def No2(self, page2, page3, hImgCtrl, vImgCtrl):
		# displays image on 3rd page
		self.upPaint(page3, self.verticalPath, vImgCtrl, 1)
		self.upPaint(page3, self.horizontalPath, hImgCtrl, 0)
		page2.Hide()                    # Hides 2nd page
		self.ShowYourself(page3)        # Shows 3rd page



	# page movement functions
	# Page to be shown
	def ShowYourself(self, page):
		page.Raise()
		page.SetPosition((0,0))
		page.Fit()
		page.GetParent().GetSizer().Show(page)
		page.GetParent().GetSizer().Layout()
		page.Refresh()

	### Mouse events
	# Mouse event handler, on click press
	def mousePress(self, event):
                print "Mouse clicked"

        # Mouse event handler, on click release
        def mouseRelease(self, event):
                print "Mouse released"

        # Mouse event handler, on drag
        def mouseDrag(self, event):
                if event.Dragging():
                        x = event.GetX()
                        y = event.GetY()
                        print "Mouse dragged x:  %d, y: %d" % (x, y)

        ### Mouse event tests end
	'''
	def OnBack(self, event):
		self.Hide()
		self.GetParent().panel0.ShowYourself()
		self.GetParent().GetSizer().Layout()

	def OnNext(self, event):
		self.Hide()
		self.GetParent().panel2.ShowYourself()
		self.GetParent().GetSizer().Layout()

	def OnCancelAndExit(self, event):
		self.GetParent().ShutDown()
	'''
