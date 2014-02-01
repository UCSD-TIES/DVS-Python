import wx, os
from interaction import *

class page(wx.Panel):

	def __init__(self, parent, baseSizer):

		self.interact = interaction()   # for button functionality, also holds some data
		self.verImgCtrl = None          # There's 2 different imgCtrl's in each page
		self.horImgCtrl = None          # These 2 are just the first page's.
										# They don't even need to be initialized here

		#page setups
		self.page1 = wx.Panel(parent)   # Creates the page, which is a panel
		self.pageSetUp(self.page1)      # Each page is set up differently
		baseSizer.Add(self.page1, 1, wx.EXPAND)   # Add the page to the frame's sizer
		self.page2 = wx.Panel(parent)
		self.pageSetUp2(self.page2)
		baseSizer.Add(self.page2, 1, wx.EXPAND)
		self.page3 = wx.Panel(parent)
		self.pageSetUp3(self.page3)
		baseSizer.Add(self.page3, 1, wx.EXPAND)
		self.page2.Hide()               # Pages that aren't page 1 start off hidden
		self.page3.Hide()

	''' Unused
	def getPage(self, pageNum):
		if pageNum == 1:
			return self.page1
		elif pageNum == 2:
			return self.page2
	'''

	''' Moved to interaction.py
	def ShowYourself(self, page):
		page.Raise()
		page.SetPosition((0,0))
		page.Fit()
		page.GetParent().GetSizer().Show(page)
		page.GetParent().GetSizer().Layout()
	'''
	def pageSetUp(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)

		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(3, 1, 5, 5)    # A column that holds the rest of the sizers
		menu = wx.FlexGridSizer(1, 5, 5, 5)        # Title, reset, next button
		pics = wx.FlexGridSizer(1, 2, 5, 5)        # Uploaded photos
		upload = wx.FlexGridSizer(1, 4, 5, 5)      # Path names and upload buttons

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)            # Images start off as blank images
		self.verImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))  # Creates it as a bitmap
		horImg = wx.EmptyImage(440,440)
		self.horImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Welcome to DVS")   # Static text for the page

		# Displays path of images, uneditable
		horPhotoTxt = wx.TextCtrl(page, size=(350,-1), style=wx.TE_READONLY)
		horPhotoTxt.SetValue("Please upload an image.")
		verPhotoTxt = wx.TextCtrl(page, size=(350,-1), style=wx.TE_READONLY)
		verPhotoTxt.SetValue("Please upload an image.")


		###################BUTTONS####################
		nextBtn = wx.Button(page, label='Next')          # Button for moving onto next page
		nextBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.next1(horPhotoTxt.GetValue(), 
				verPhotoTxt.GetValue(), self.page1, self.page2, self.hor2ImgCtrl, self.ver2ImgCtrl))
		# Passes in path names for both photos, current page, page 2, creates page 2's imgCtrl's

		# Button to clear pictures and paths
		resetBtn = wx.Button(page, label='Reset')
		resetBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.reset(page, self.horImgCtrl, 
				self.verImgCtrl, horPhotoTxt, verPhotoTxt))
		# Passes in current page's imgCtrl's and text controls to delete
				
		# Button to upload a horizontal photo
		horiBtn = wx.Button(page, label='Horizontal')
		horiBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.upload(page, self.horImgCtrl, horPhotoTxt, 0))
		# Passes in the imgCtrl and text control that corresponds to the horizontal image

		# Button to upload a vertical photo
		vertBtn = wx.Button(page, label='Vertical')
		vertBtn.Bind(wx.EVT_BUTTON, 
			lambda event: self.interact.upload(page, self.verImgCtrl, verPhotoTxt, 1))

		###################ADDING_STUFF#################
		# Adding items into the grids
		mainGrid.AddMany([(menu),(upload),(pics)])         # Adds the three sizers to the main sizer

		# Adds the components to the layout sizers
		menu.AddMany([(title),(595,0),(resetBtn),(nextBtn)])      # Title, large space, reset, next
		pics.AddMany([(self.horImgCtrl),(self.verImgCtrl)])       # The two images
		upload.AddMany([(horPhotoTxt),(horiBtn),(verPhotoTxt),(vertBtn)])   # Text boxes and buttons

		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)   # Adds everything to real main sizer
		page.SetSizer(vbox)                                # Sets the main sizer as the page's sizer

	# Set up for page 2 - Most of it is the same as page 1
	def pageSetUp2(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)

		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(3, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 5, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)

		###############COMPONENTS################
		# Note that the imgCtrl's here were made in page 1's next button
		verImg = wx.EmptyImage(440,440)
		self.ver2ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		self.hor2ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

 
		title = wx.StaticText(page, label="Do the boxes frame the eyes?")   # Different title from page 1's

		yesBtn = wx.Button(page, label='Yes')     # Button to go to 4th page - FUNCTIONALITY NOT ADDED YET

		noBtn = wx.Button(page, label='No')       # Button to go to 3rd page
		noBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.No2(self.page2, self.page3, self.hor3ImgCtrl, self.ver3ImgCtrl))
		# Will pass in image controls of 3rd page

		#################ADDING STUFF#################
		# See page 1's set up
		mainGrid.AddMany([(menu),(pics)])
		menu.AddMany([(title),(560,0),(yesBtn),(noBtn)])
		pics.AddMany([(self.hor2ImgCtrl),(self.ver2ImgCtrl)])


		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)

	# Set up for page 3 - Nothing special about this page yet, 
	# This is the user input eye detection correction page
	def pageSetUp3(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)

		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(2, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 5, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)
		self.ver3ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		self.hor3ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Please correct the eye detection.")

		mainGrid.AddMany([(menu),(pics)])
		menu.AddMany([(title),(560,0)])
		pics.AddMany([(self.hor3ImgCtrl),(self.ver3ImgCtrl)])


		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)
