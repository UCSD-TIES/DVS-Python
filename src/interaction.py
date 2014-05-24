import wx, os
import wx, os
from Controller import *
#from xlwt import Workbook
#use makepatient method from controller

IMGMASK = "JPEG Files(*.jpg;*.jpeg;*.jpe;*.jfif) " \
	"|*.jpg; *.jpeg; *.jpe; *.jfif|" \
	"Raw Files |*.cr2; *crw|" \
	"All Files |*.*"

class interaction():
	def __init__(self):
		self.patientData = []
		self.patient = None          # This might not be used
		self.horizontalPath = None   # Path of horizontal image
		self.verticalPath = None     # Path of vertical image
		self.heightRatio = None
		self.widthRatio = None
		self.rRatio = None
		self.lRatio = None

		self.hRightPath = None
		self.hLeftPath = None
		self.vRightPath = None
		self.vLeftPath = None

		# These bitmaps are needed to draw on, can't draw on img Ctrls
		self.hBitMap = None
		self.vBitMap = None

		self.hlBitMap = None
		self.hrBitMap = None
		self.vlBitMap = None
		self.vrBitMap = None

		# Images to make bitmaps out of, will store original image for resets
		self.hImg = None
		self.vImg = None

		self.hlImg = None
		self.hrImg = None
		self.vlImg = None
		self.vrImg = None

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
	
	# specialized upPaint function for cropped pupil photos
	# Args: page - the page passed in from upload() (page 1)
	#       upPath - path of the image to be shown
	#       imgCtrl - holds the newly shown image
	#       orientation - vertical or horizontal, taken from upload()
	#		eyeNum - flag of which eye is being painted
	def upPupilPaint(self, page, upPath, imgCtrl, eyeNum):
		# Makes a new image using the file path
		newImg = wx.Image(upPath, wx.BITMAP_TYPE_ANY)

		# Getting width and height of this image
		width = newImg.GetWidth()
		height = newImg.GetHeight()
		maxSize = 100

		# Scales the image
		# This scaling works, but may have problems in future
		if width > height:
			newWidth = maxSize
			newHeight = maxSize * height/ width
		else:
			newHeight = maxSize
			newWidth = maxSize * width/ height
		if eyeNum == 0 | eyeNum == 2:
			self.lRatio = float(newHeight)/float(height)
		elif eyeNum == 1 | eyeNum == 3:
			self.rRatio = float(newHeight)/float(height)

		print "OG Height:", height, "| OG Width", width, "| New Height:", newHeight, "| New Width:", newWidth
		print "Left Eye Photos Ratio:", self.lRatio, "| Right Eye Photos Ratio:", self.rRatio
		# Finishes scaling and sets img into the imgCtrl  
		newImg = newImg.Scale(newWidth,newHeight)
		imgCtrl.SetBitmap(wx.BitmapFromImage(newImg))

		if eyeNum == 0:
			self.hlBitMap = wx.BitmapFromImage(newImg)
			self.hlImg = newImg
		elif eyeNum == 1:
			self.hrBitMap = wx.BitmapFromImage(newImg)
			self.hrImg = newImg
		elif eyeNum == 2:
			self.vlBitMap = wx.BitmapFromImage(newImg)
			self.vlImg = newImg
		elif eyeNum == 3:
			self.vrBitMap = wx.BitmapFromImage(newImg)
			self.vrImg = newImg

		page.Refresh()

	# Next Button for first page
	# Args: hPhotoTxt - text control for horizontal image
	#       vPhotoTxt - text control for vertical image
	#       page1 - 1st page
	#       page2 - 2nd page
	#       hImgCtrl - horizontal image control of 2nd page
	#       vImgCtrl - vertical image control of 2nd page
	def next0(self, page0, page1, name, birth, gender, ethnicity, language,
			  roomNumber, school, screeningComment, referral):

		self.patient = Patient()

		if name != "":
			self.patient.name = name

		if birth != "":
			self.patient.birth = birth

		if gender != "":
			self.patient.gender = gender

		if ethnicity != "":
			self.patient.ethnicity = ethnicity

		if language != "":
			self.patient.language = language

		if roomNumber != "":
			self.patient.roomNumber = roomNumber

		if school != "":
			self.patient.school = school

		if screeningComment != "":
			self.patient.screeningComment = screeningComment

		if referral != "":
			self.patient.referral = referral

		page0.Hide()
		self.ShowYourself(page1)          # Shows 2nd page

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
			
		print self.patient.name
			
		#self.patient = makePatient(self.horizontalPath, self.verticalPath)
		setPatient(self.horizontalPath, self.verticalPath, self.patient)
		coors = getEyeCoors(self.patient)                 # this coors is local, just for drawing
		print coors

		# Paints the images of page 2 and hides the first page
		self.upPaint(page2, self.verticalPath, vImgCtrl, 1)
		self.upPaint(page2, self.horizontalPath, hImgCtrl, 0)
		page1.Hide()

		# Drawing rectangle with MemoryDC
		mdc = wx.MemoryDC()
		
		mdc.SelectObject(self.hBitMap)    # sets a bitmap to be modified
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))

		# Rectangles are drawn with DC.DrawRectangle(X, Y, width, Height)
		mdc.DrawRectangle(coors[0][0]*self.widthRatio, coors[0][1]*self.heightRatio, coors[0][2]*self.widthRatio, coors[0][3]*self.heightRatio)
		mdc.DrawRectangle(coors[1][0]*self.widthRatio, coors[1][1]*self.heightRatio, coors[1][2]*self.widthRatio, coors[1][3]*self.heightRatio)
		hImgCtrl.SetBitmap(self.hBitMap)  # Sets modified bitmap back into the img ctrl

		#img = self.vBitMap.ConvertToImage()	# To get width
		#width = img.GetWidth()
		#img = img.Rotate90()
		#self.vBitMap = wx.BitmapFromImage(img)
		mdc.SelectObject(self.vBitMap)    # sets a bitmap to be modified
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

	# The "Yes" button on page2 - Moves from page 2 to 4
	# Args: page2 - 2nd page
	#       page4 - 4th page
	def Yes2(self, page2, page4, hRightImgCtrl, 
				hLeftImgCtrl, vRightImgCtrl, vLeftImgCtrl):
		EyePhotos = getEyePhotos(self.patient)
		self.hRightPath = EyePhotos[0]
		self.hLeftPath = EyePhotos[1]
		self.vRightPath = EyePhotos[2]
		self.vLeftPath = EyePhotos[3]
		# displays image on 4th page
		self.upPupilPaint(page4, self.hRightPath, hRightImgCtrl, 1)
		self.upPupilPaint(page4, self.hLeftPath, hLeftImgCtrl, 0)
		self.upPupilPaint(page4, self.vRightPath, vRightImgCtrl, 3)
		self.upPupilPaint(page4, self.vLeftPath, vLeftImgCtrl, 2)
		page2.Hide()                    # Hides 2nd page

		setPatient(self.horizontalPath, self.verticalPath, self.patient)
		coors = getPupilCoors(self.patient)  # this coors is local, just for drawing
		print coors

		# Drawing circles with MemoryDC
		mdc = wx.MemoryDC()
		
		mdc.SelectObject(self.hlBitMap)    # sets a bitmap to be modified
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
		mdc.DrawCircle(coors[0][0]*self.lRatio, coors[0][1]*self.lRatio, coors[0][2]) #DrawCircle(Xpos, Ypos, radius)
		hLeftImgCtrl.SetBitmap(self.hlBitMap)  # Sets modified bitmap back into the img ctrl

		mdc.SelectObject(self.hrBitMap)
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
		mdc.DrawCircle(coors[1][0]*self.rRatio, coors[1][1]*self.rRatio, coors[1][2])
		hRightImgCtrl.SetBitmap(self.hrBitMap)

		mdc.SelectObject(self.vlBitMap)
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
		mdc.DrawCircle(coors[2][0]*self.lRatio, coors[2][1]*self.lRatio, coors[2][2])
		vLeftImgCtrl.SetBitmap(self.vlBitMap)

		mdc.SelectObject(self.vrBitMap)
		mdc.SetBrush(wx.Brush('#CCFF99', wx.TRANSPARENT))
		mdc.DrawCircle(coors[3][0]*self.rRatio, coors[3][1]*self.rRatio, coors[3][2])
		vRightImgCtrl.SetBitmap(self.vrBitMap)

		mdc.SelectObject(wx.NullBitmap)   # MemoryDC must be set back to a null bitmap when done
		
		self.ShowYourself(page4)        # Shows 4th page

	
	# The "No" button on page4 - Moves from page 4 to 5
	# Args: page4 - 4nd page
	#       page5 - 5rd page
	#       hImgCtrl - 5rd page's horizontal image control
	#       vImgCtrl - 5rd page's vertical image control
	def No4(self, page4, page5, hRightImgCtrl, 
				hLeftImgCtrl, vRightImgCtrl, vLeftImgCtrl):
		# displays image on 4th page
		self.upPupilPaint(page5, self.hRightPath, hRightImgCtrl, 1)
		self.upPupilPaint(page5, self.hLeftPath, hLeftImgCtrl, 0)
		self.upPupilPaint(page5, self.vRightPath, vRightImgCtrl, 3)
		self.upPupilPaint(page5, self.vLeftPath, vLeftImgCtrl, 2)
		page4.Hide()                    # Hides 2nd page
		self.ShowYourself(page5)        # Shows 5th page


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
			if 'wxMac' in wx.PlatformInfo:
				dc.SetBrush(wx.Brush(wx.Colour(0xC0, 0xC0, 0xC0, 0x80)))
			else:
				dc.SetBrush(wx.TRANSPARENT_BRUSH)
			dc.DrawRectangleRect(rect)

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

		defectSize = len(all_defects)
		infoSize = len(all_info)

		print "all_defects size: ", defectSize
		print "all_info size:    ", infoSize

		defectsArray = [[0 for x in xrange(2)] for y in xrange(defectSize)]
		infoArray = [[0 for x in xrange(2)] for y in xrange(infoSize)]

		refer = 0
		lineCounter = 0
		for line in all_defects.keys():
			if line == "Anisomet" or line == "Strabismus" or line == "Astigmatism": refer = 1
			defectsArray[lineCounter][0] = line
			defectsArray[lineCounter][1] = str(all_defects[line])
			lineCounter += 1
		defectsArray.sort()

		lineCounter = 0
		for line in all_info.keys():
			infoArray[lineCounter][0] = line
			infoArray[lineCounter][1] = str(all_info[line])
			lineCounter += 1
		infoArray.sort()

		# print info to the console
		for line in defectsArray: print line
		for line in infoArray: print line

		# display defects to result page
		y = 100
		for line in defectsArray:
			wx.StaticText(resultPage, -1, line[0], (200, y), (-1, -1), wx.ALIGN_CENTER)
			wx.StaticText(resultPage, -1, line[1], (500, y), (-1, -1), wx.ALIGN_CENTER)
			y += 30
		print "\n"

		# display info to result page
		y += 30
		for line in infoArray:
			wx.StaticText(resultPage, -1, line[0], (200, y), (-1, -1), wx.ALIGN_CENTER)
			wx.StaticText(resultPage, -1, line[1], (500, y), (-1, -1), wx.ALIGN_CENTER)
			y += 30
		print "\n"

		# display refer result to result page
		y = 480
		referText = "Refer" if refer == 1 else "Not Refer"

		font1 = wx.Font(30, wx.NORMAL, wx.ITALIC, wx.NORMAL)
		result = wx.StaticText(resultPage, -1, referText, (850, y), (-1, -1), wx.ALIGN_CENTRE)
		result.SetFont(font1)
	def startOver(self, resultPage, page1, horImgCtrl, verImgCtrl, text1, text2, pageNum):

		# Hides result page
		resultPage.Hide()

		self.reset(page1, horImgCtrl, verImgCtrl, text1, text2, pageNum)

		# Shows first page
		page1.Show()

	def saveData(self, page, name, birth, gender, ethnicity, language,
			  roomNumber, school, screeningComment, referral):		
	   
	   # Creates a patient object to be saved into data structure
    	   patient = Patient()

	   if name.GetValue() != "":
	       patient.name = name.GetValue()

	   if birth.GetValue() != "":
	       patient.birth = birth.GetValue()

	   if gender.GetValue() != "":
	       patient.gender = gender.GetValue()

	   if ethnicity.GetValue() != "":
	       patient.ethnicity = ethnicity.GetValue()

	   if language.GetValue() != "":
	       patient.language = language.GetValue()

	   if roomNumber.GetValue() != "":
	       patient.roomNumber = roomNumber.GetValue()

	   if school.GetValue() != "":
	       patient.school = school.GetValue()

           if screeningComment.GetValue() != "":
	       patient.screeningComment = screeningComment.GetValue()

	   if referral.GetValue() != "":
	       patient.referral = referral.GetValue()
			
	   # Saves patient data into data structure
	   self.patientData.append(patient)
	   msg = "Patient Data was saved into the database."
           savedMsg = wx.MessageDialog(page, msg, "Patient Data Saved", wx.OK)
           savedMsg.ShowModal()
           
           # Clears inputs after patient data is saved
           name.Clear()
           birth.Clear()
           gender.Clear() 
           ethnicity.Clear()
           language.Clear()
           roomNumber.Clear()
           school.Clear()
           screeningComment.Clear()
           referral.Clear()											
															
	def exportData(self,page):

            # Exports data in Excel file
            book = Workbook()
            
            # index for sheet page
            i = 1
            
	    for patient in self.patientData:
            
                sheet = book.add_sheet('Patient Data' + str(i))     
                sheet.write(0,0,'Name')
                sheet.write(0,1,patient.name)
                
                row1 = sheet.row(1)
                row1.write(0,'Date of Birth')
                row1.write(1,patient.birth)
                
                row2 = sheet.row(2)
                row2.write(0,'Gender')
                row2.write(1,patient.gender)
                
                row3 = sheet.row(3)
                row3.write(0,'Ethnicity')
                row3.write(1,patient.ethnicity)
                
                row4 = sheet.row(4)
                row4.write(0,'Language')
                row4.write(1,patient.language)
                
                row5 = sheet.row(5)
                row5.write(0,'Room Number')
                row5.write(1,patient.roomNumber)
                
                row6 = sheet.row(6)
                row6.write(0,'School')
                row6.write(1,patient.school)
                
                row7 = sheet.row(7)
                row7.write(0,'Screening Comment')
                row7.write(1,patient.screeningComment)
                
                row8 = sheet.row(8)
                row8.write(0,'Referral')
                row8.write(1,patient.referral)
                
                sheet.col(0).width = 5000
                sheet.col(1).width = 5000
                
                i += 1
                
            book.save('patient_data.xls')
            msg = "Excel file saved in current directory"
            savedMsg = wx.MessageDialog(page, msg, "Patient Data Exported", wx.OK)
            savedMsg.ShowModal()