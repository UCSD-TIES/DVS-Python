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
		self.heightRatio = None
		self.widthRatio = None

		# These bitmaps are needed to draw on, can't draw on img Ctrls
		self.hBitMap = None
		self.vBitMap = None

		# Images to make bitmaps out of, will store original image for resets
		self.hImg = None
		self.vImg = None

		# Coordinates for user input in tuple
		# set of tuples for horizontal and vertical, outer tuple is (left eye, right eye)
		# inner tuple is (Top Left X, Top Left Y, Bot Right X, Bot Right Y)
		self.hcoors = [[0,0,0,0],[0,0,0,0]]
		self.vcoors = [[0,0,0,0],[0,0,0,0]]

		# For drawing and only for drawing
		self.startX = 0
		self.startY = 0
		self.overlay = wx.Overlay()
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
	def reset(self, page, horImgCtrl, verImgCtrl, text1, text2, pageNum):
		if pageNum == 1:
			empty = wx.EmptyImage(440,440)     # Create empty image

			# Sets the 2 image controls to empty
			horImgCtrl.SetBitmap(wx.BitmapFromImage(empty))
			verImgCtrl.SetBitmap(wx.BitmapFromImage(empty))
			# Resets path names
			text1.SetValue("Please upload an image.")
			text2.SetValue("Please upload an image.")

			# Deletes interaction object's data 
			self.horizontalPath = None
			self.verticalPath = None
			self.hBitMap = None
			self.vBitMap = None

		elif pageNum == 3:
			horImgCtrl.SetBitmap(self.hBitMap)
			verImgCtrl.SetBitmap(self.vBitMap)

		page.Refresh()

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

		self.heightRatio = float(newHeight)/float(height)
		self.widthRatio = float(newWidth)/float(width)
		print "OG Height:", height, "| OG Width", width, "| New Height:", newHeight, "| New Width:", newWidth
		print "Height Ratio:", self.heightRatio, "| Width Ratio:", self.widthRatio
		# Finishes scaling and sets img into the imgCtrl  
	  	newImg = newImg.Scale(newWidth,newHeight)
	  	imgCtrl.SetBitmap(wx.BitmapFromImage(newImg))

	  	# Stores data for interaction obj depending on orientation
	  	if orientation == 0:
	  		self.hBitMap = wx.BitmapFromImage(newImg)
	  		self.hImg = newImg
	  	elif orientation == 1:
	  		self.vBitMap = wx.BitmapFromImage(newImg)
	  		self.vImg = newImg
	  	page.Refresh()

	# Next Button for first page
	# Args: hPhotoTxt - text control for horizontal image
	#       vPhotoTxt - text control for vertical image
	#       page1 - 1st page
	#       page2 - 2nd page
	#       hImgCtrl - horizontal image control of 2nd page
	#       vImgCtrl - vertical image control of 2nd page
	def next1(self, hPhotoTxt, vPhotoTxt, page1, page2, hImgCtrl, vImgCtrl):
		pleaseText = "Please upload an image."
		if hPhotoTxt == pleaseText and vPhotoTxt == pleaseText:
			errorTxt1 = "Missing images, please upload."
			errMsg1 = wx.MessageDialog(page1, errorTxt1, "No Images Detected", wx.OK)
			errMsg1.ShowModal()
			errMsg1.Destroy()
			
		self.patient = makePatient(self.horizontalPath, self.verticalPath)
		coors = getEyeCoors(self.patient)                 # this coors is local, just for drawing
		print coors

		# Paints the images of page 2 and hides the first page
		self.upPaint(page2, self.verticalPath, vImgCtrl, 1)
		self.upPaint(page2, self.horizontalPath, hImgCtrl, 0)
		page1.Hide()

		# Drawing rectangle with MemoryDC
		mdc = wx.MemoryDC()
		
		mdc.SelectObject(self.hBitMap)    # sets a bitmap to e modified
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))

		# Rectangles are drawn with DC.DrawRectangle(X, Y, width, Height)
		mdc.DrawRectangle(coors[0][0]*self.widthRatio, coors[0][1]*self.heightRatio, coors[0][2]*self.widthRatio, coors[0][3]*self.heightRatio)
		mdc.DrawRectangle(coors[1][0]*self.widthRatio, coors[1][1]*self.heightRatio, coors[1][2]*self.widthRatio, coors[1][3]*self.heightRatio)
		hImgCtrl.SetBitmap(self.hBitMap)  # Sets modified bitmap back into the img ctrl

		img = self.vBitMap.ConvertToImage()	# To get width
		width = img.GetWidth()
		#img = img.Rotate90()
		#self.vBitMap = wx.BitmapFromImage(img)
		mdc.SelectObject(self.vBitMap)    # sets a bitmap to e modified
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
		# THIS MIGHT BE WRONG
		#mdc.DrawRectangle((coors[2][1]+coors[2][3])*self.heightRatio, (width - coors[2][0]-coors[2][2])*self.widthRatio, coors[2][3], coors[2][2])
		#mdc.DrawRectangle((coors[3][1]+coors[3][3])*self.heightRatio, (width - coors[3][0]-coors[3][2])*self.widthRatio, coors[3][3], coors[3][2])
		mdc.DrawRectangle(coors[2][0]*self.widthRatio, coors[2][1]*self.heightRatio, coors[2][2]*self.widthRatio, coors[2][3]*self.heightRatio)
		mdc.DrawRectangle(coors[3][0]*self.widthRatio, coors[3][1]*self.heightRatio, coors[3][2]*self.widthRatio, coors[3][3]*self.heightRatio)
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
	# orientation: vertical is 1, horizontal is 0
	def mousePress(self, event, orientation):
		#print "Mouse clicked"
		newX = event.GetX()
		newY = event.GetY()
		self.startX = newX
		self.startY = newY
		if orientation == 0:
			if self.hcoors[0][0] == 0:      # if hcoors is empty, assume left eye
				self.hcoors[0][0] = newX
				self.hcoors[0][1] = newY
			elif self.hcoors[1][0] == 0:    # if right eye has no value yet
				self.whichEye(0, newX, newY, 0)  # check which eye new value belongs to
		elif orientation == 1:
			if self.vcoors[0][0] == 0:
				self.vcoors[0][0] = newX
				self.vcoors[0][1] = newY
			elif self.vcoors[1][0] == 0:
				self.whichEye(1, newX, newY, 0)


	# Helper function checks which eye inputed values belong to
	# orientation: vertical is 1, horizontal is 0
	# point: 0 if starting point, 1 if ending point, of the rectangle
	def whichEye(self, orientation, newX, newY, point):
		if point == 1:                              # for ending point
			if orientation == 0:
				if newX > self.hcoors[0][2]:        # values for right eye
					self.hcoors[1][2] = newX
					self.hcoors[1][3] = newY
				else:							# New eye values are for left eye
					self.hcoors[1][2] = self.hcoors[0][2]
					self.hcoors[1][3] = self.hcoors[0][3]
					self.hcoors[0][2] = newX
					self.hcoors[0][3] = newY
			if orientation == 1:
				if newX > self.vcoors[0][2]:    # New eye values are for right eye
					self.vcoors[1][2] = newX
					self.vcoors[1][3] = newY
				else:							# New eye values are for left eye
					self.vcoors[1][2] = self.vcoors[0][2]
					self.vcoors[1][3] = self.vcoors[0][3]
					self.vcoors[0][2] = newX
					self.vcoors[0][3] = newY

		# For starting point
		if point == 0:
			if orientation == 0:
				if newX > self.hcoors[0][0]:    # New eye values are for right eye
					self.hcoors[1][0] = newX
					self.hcoors[1][1] = newY
				else:							# New eye values are for left eye
					self.hcoors[1][0] = self.hcoors[0][0]
					self.hcoors[1][1] = self.hcoors[0][1]
					self.hcoors[0][0] = newX
					self.hcoors[0][1] = newY
			if orientation == 1:
				if newX > self.vcoors[0][0]:    # New eye values are for right eye
					self.vcoors[1][0] = newX
					self.vcoors[1][1] = newY
				else:							# New eye values are for left eye
					self.vcoors[1][0] = self.vcoors[0][0]
					self.vcoors[1][1] = self.vcoors[0][1]
					self.vcoors[0][0] = newX
					self.vcoors[0][1] = newY


		

	# Mouse event handler, on click release
	# orientation: vertical is 1, horizontal is 0
	def mouseRelease(self, event, imgCtrl, orientation):
		#print "Mouse released"
		endX = event.GetX()
		endY = event.GetY()



		# Managing how the user is drawing
		# User might not draw from top left to bottom right
		if self.startX > endX:
			temp = self.startX
			self.startX = endX
			endX = temp
		if self.startY > endY:
			temp = self.startY
			self.startY = endY
			endY = temp

		if orientation == 0:
			if self.hcoors[0][2] == 0:      # if hcoors is empty, assume left eye
				self.hcoors[0][2] = endX
				self.hcoors[0][3] = endY
			elif self.hcoors[1][2] == 0:
				self.whichEye(orientation, endX, endY, 1)
		elif orientation == 1:
			if self.vcoors[0][2] == 0:
				self.vcoors[0][2] = endX
				self.vcoors[0][3] = endY
			elif self.vcoors[1][2] == 0:
				self.whichEye(orientation, endX, endY, 1)
		'''
		elif orientation == 1:
			if self.vstartX > self.vendX:
				temp = self.vstartX
				self.vstartX = self.vendX
				self.vendX = temp
			if self.vstartY > self.vendY:
				temp = self.vstartY
				self.vstartY = self.vendY
				self.vendY = temp
		'''

		
		
		mdc = wx.MemoryDC()
		bdc = wx.BufferedDC(mdc)
		bitmap = imgCtrl.GetBitmap()
		bdc.SelectObject(bitmap)
		bdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))

		bdc.DrawRectangle(self.startX, self.startY, endX - self.startX, endY - self.startY)
		print "startX: %d startY: %d endX: %d endY: %d" % (self.startX, self.startY, endX, endY)
		'''
		elif orientation == 1:
			bdc.DrawRectangle(self.vstartX, self.vstartY, self.vendX - self.vstartX, self.vendY - self.vstartY)
			print "startX: %d startY: %d endX: %d endY: %d" % (self.vstartX, self.vstartY, self.vendX, self.vendY)
		'''
		bdc.SelectObject(wx.NullBitmap)
		imgCtrl.SetBitmap(bitmap)
		self.startX = 0
		self.startY = 0
		print self.hcoors
		print self.vcoors


	# Mouse event handler, on drag
	def mouseDrag(self, event, imgCtrl):

		
		if event.Dragging():
			x = event.GetX()
			y = event.GetY()
			rect = wx.RectPP( (self.startX,self.startY), (x,y))

			dc = wx.ClientDC(imgCtrl)

			odc = wx.DCOverlay(self.overlay, dc)
			odc.Clear()

			dc.SetPen(wx.Pen("black", 2))
			dc.SetBrush(wx.TRANSPARENT_BRUSH)
			dc.DrawRectangleRect(rect)

			self.overlay.DrawRectangleRect(rect)

			del odc
		'''
			#print "Mouse dragged x:  %d, y: %d" % (x, y)
			# DRAWING HERE WAS SO YOU CAN SEE THE RECTANGLE BEING DRAWN
			# DOESN'T WORK SO MOVED TO UPON RELEASE
			
			mdc = wx.MemoryDC()
			bdc = wx.BufferedDC(mdc)
			bitmap = imgCtrl.GetBitmap()
			bdc.SelectObject(bitmap)
			bdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
			bdc.DrawRectangle(self.startX, self.startY, x - self.startX, y - self.startY)
			bdc.SelectObject(wx.NullBitmap)
			imgCtrl.SetBitmap(bitmap)
			
		'''

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
	# corrected = 1 if user corrected detection
	def seeResult(self, page3, resultPage, corrected):
		page3.Hide() # Hides 3nd page 
		self.ShowYourself(resultPage) # Shows result page

		if corrected == 1:
			x = self.widthRatio
			y = self.heightRatio
			hTuple = ((int (self.hcoors[0][0]/x),int (self.hcoors[0][1]/y),int (self.hcoors[0][2]/x),int (self.hcoors[0][3]/y)),
			          (int (self.hcoors[1][0]/x),int (self.hcoors[1][1]/y),int (self.hcoors[1][2]/x),int (self.hcoors[1][3]/y)))
			vTuple = ((int (self.vcoors[0][0]/x),int (self.vcoors[0][1]/y),int (self.vcoors[0][2]/x),int (self.vcoors[0][3]/y)),
			          (int (self.vcoors[1][0]/x),int (self.vcoors[1][1]/y),int (self.vcoors[1][2]/x),int (self.vcoors[1][3]/y)))
			resetEyes(self.patient, hTuple, vTuple)
		self.patient.analyzeEyes(0.17)
		all_info = self.patient.getInfo()
		all_defects = self.patient.getDefects()

		y = 100
		for line in all_defects.keys():
			print "[" + line + "]" + " = " + str(all_defects[line])
			wx.StaticText(resultPage, -1, line, (200, y), (-1, -1), wx.ALIGN_CENTER)
			wx.StaticText(resultPage, -1, str(all_defects[line]), (500, y), (-1, -1), wx.ALIGN_CENTER)
			y += 30

		print "\n"
		for line in all_info.keys():
			print "[" + line + "]" + " = " + str(all_info[line])
			wx.StaticText(resultPage, -1, line, (200, y), (-1, -1), wx.ALIGN_CENTER)
			wx.StaticText(resultPage, -1, str(all_info[line]), (500, y), (-1, -1), wx.ALIGN_CENTER)
			y += 30
		print "\n"
