import wx, os
from Controller import *
#use makepatient method from controller

IMGMASK = "JPEG Files(*.jpg;*.jpeg;*.jpe;*.jfif) " \
	"|*.jpg; *.jpeg; *.jpe; *.jfif|" \
	"Raw Files |*.cr2; *crw|" \
	"All Files |*.*"

class interaction():
	def __init__(self):
		self.patient = None
		self.horizontalPath = None
		self.verticalPath = None

	# BUTTONS

	# upload button, 1st page
	def upload(self, page, imgCtrl, text, orientation):
	  	# pops up box for user to upload image
	  	upBox = wx.FileDialog(page, "Choose an image.", os.getcwd(), "",
							IMGMASK, wx.OPEN)
	  	if upBox.ShowModal() == wx.ID_OK:
			upPath = upBox.GetPath()
			self.upPaint(page, upPath, imgCtrl)
			text.SetValue(upPath)
	  	if orientation == 0:
	  		self.horizontalPath = upPath
	  	elif orientation == 1:
	  		self.verticalPath = upPath
		  
	# reset button, 1st page
	def reset(self, page, imgCtrl1, imgCtrl2, text1, text2):
		empty = wx.EmptyImage(440,440)     # Create empty image
		# Sets the 2 image controls to empty
		imgCtrl1.SetBitmap(wx.BitmapFromImage(empty))
		imgCtrl2.SetBitmap(wx.BitmapFromImage(empty))
		# Resets path names
		text1.SetValue("Please upload an image.")
		text2.SetValue("Please upload an image.")
		page.Refresh()

	# display the uploaded picture
	def upPaint(self, page, upPath, imgCtrl):
		newImg = wx.Image(upPath, wx.BITMAP_TYPE_ANY)

		width = newImg.GetWidth()
		height = newImg.GetHeight()
		maxSize = 440

	  # scale the image to preserving the aspect ratio
		'''
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

	  	# This scaling works, but may have problems in future
	  	if width > height:
			newWidth = maxSize
		  	newHeight = maxSize * height/ width
	  	else:
		  	newHeight = maxSize
		  	newWidth = maxSize * width/ height
		  
	  	newImg = newImg.Scale(newWidth,newHeight)
	  	imgCtrl.SetBitmap(wx.BitmapFromImage(newImg))
	  	page.Refresh()

	# Next Button for first page
	def next1(self, hPhotoTxt, vPhotoTxt, page1, page2, hImgCtrl, vImgCtrl):
		'''
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
		#self.patient = makePatient(self.horizontalPath, self.verticalPath) 

		self.upPaint(page2, self.verticalPath, vImgCtrl)
		self.upPaint(page2, self.horizontalPath, hImgCtrl)
		page1.Hide()
		self.ShowYourself(page2)
		
		


	# page movement functions

	def ShowYourself(self, page):
		page.Raise()
		page.SetPosition((0,0))
		page.Fit()
		page.GetParent().GetSizer().Show(page)
		page.GetParent().GetSizer().Layout()
		page.Refresh()
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
