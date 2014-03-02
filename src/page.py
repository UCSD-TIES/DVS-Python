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


		# set up result page
		self.resultPage = wx.Panel(parent)
		self.resultPageSetup(self.resultPage)
		baseSizer.Add(self.resultPage, 1, wx.EXPAND)
		#self.page1.Hide()
		self.resultPage.Hide()


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
		upload = wx.FlexGridSizer(1, 5, 5, 4)      # Path names and upload buttons

		pic1 = wx.BoxSizer(wx.VERTICAL)
		pic2 = wx.BoxSizer(wx.VERTICAL)

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)            # Images start off as blank images
		self.verImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))  # Creates it as a bitmap
		horImg = wx.EmptyImage(440,440)
		self.horImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Welcome to DVS")   # Static text for the page

		# Displays path of images, uneditable
		horPhotoTxt = wx.TextCtrl(page, size=(360,-1), style=wx.TE_READONLY)
		horPhotoTxt.SetValue("Please upload an image.")
		verPhotoTxt = wx.TextCtrl(page, size=(360,-1), style=wx.TE_READONLY)
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
		menu.AddMany([(title),(640,0),(resetBtn),(nextBtn)])      # Title, large space, reset, next
		pic1.Add(self.horImgCtrl, flag = wx.ALIGN_CENTER)
		pic2.Add(self.verImgCtrl, flag = wx.ALIGN_CENTER)
		pics.AddMany([(pic1),(pic2)])       # The two images
		upload.AddMany([(horPhotoTxt),(horiBtn),(0,0),(verPhotoTxt),(vertBtn)])   # Text boxes and buttons

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
		menu = wx.FlexGridSizer(1, 4, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)

		pic1 = wx.BoxSizer(wx.VERTICAL)
		pic2 = wx.BoxSizer(wx.VERTICAL)

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
		pic1.Add(self.hor2ImgCtrl, flag = wx.ALIGN_RIGHT)
		pic2.Add(self.ver2ImgCtrl, flag = wx.ALIGN_LEFT)
		pics.AddMany([(pic1),(pic2)])

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

		# adding see result button
		resultBtn = wx.Button(page, label="See Result")
		resultBtn.Bind(wx.EVT_BUTTON, lambda event: self.interact.seeResult(self.page3, self.resultPage))
		menu.AddMany([(title), (560, 0), (resultBtn)])

		mainGrid.AddMany([(menu),(pics)])
		pics.AddMany([(self.hor3ImgCtrl),(self.ver3ImgCtrl)])

		### Mouse events, on click, on drag
		# Mouse events for vertical image
		self.ver3ImgCtrl.Bind(wx.EVT_LEFT_DOWN, lambda event: self.interact.mousePress(event, 1))
		self.ver3ImgCtrl.Bind(wx.EVT_MOTION, lambda event: self.interact.mouseDrag(event,self.ver3ImgCtrl))
		self.ver3ImgCtrl.Bind(wx.EVT_LEFT_UP, lambda event: self.interact.mouseRelease(event, self.ver3ImgCtrl, 1))

		# Mouse events for horizontal image
		self.hor3ImgCtrl.Bind(wx.EVT_LEFT_DOWN, lambda event: self.interact.mousePress(event, 0))
		self.hor3ImgCtrl.Bind(wx.EVT_MOTION, lambda event: self.interact.mouseDrag(event, self.hor3ImgCtrl))
		self.hor3ImgCtrl.Bind(wx.EVT_LEFT_UP, lambda event: self.interact.mouseRelease(event, self.hor3ImgCtrl, 0))

		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)

		# setup a result page
	def resultPageSetup(self, page):

		h_path = "/Users/yMac/Desktop/hh.jpg"
		v_path = "/Users/yMac/Desktop/vv.jpg"

		print 'making patient call'
		patients = makePatient(h_path, v_path)
		resetEyes( patients, ((455,572,647,695),(771,537,958,650)) ,((467,596,620,718),(746,614,887,704)) )

		patients.analyzeEyes(0.17)

		all_info = patients.getInfo()
		all_defects = patients.getDefects()

		for line in  all_defects.keys():
			print "[" + line + "]" + " = " + str(all_defects[line])
		print "\n"
		for line in  all_info.keys():
			print "[" + line + "]" + " = " + str(all_info[line])
		print "\n"

		'''
		# print out title on top left corner of the page
		resultText = "This is result page"
		result = wx.StaticText(page, -1, resultText, (0, 40), (1000, -1), wx.ALIGN_CENTER)
		result.SetBackgroundColour('blue')
		result.SetForegroundColour('white')

		picThumbnail = "Picture thumbnail goes here"
		wx.StaticText(page, -1, picThumbnail, (50, 200))

		foundTxt = "Found in (left/right/both/none)"
		found = wx.StaticText(page, -1, foundTxt, (750, 100), (-1, -1), wx.ALIGN_CENTER)
		found.SetBackgroundColour('blue')
		found.SetForegroundColour('white')

		# passing data from backend to here
		disease1 = "Disease Name 1: left eye"
		disease2 = "Disease Name 2: right eye"
		disease3 = "Disease Name 3: both eyes"
		disease4 = "Disease Name 4: NONE"
		disease5 = "Disease Name 5: right eye"
		wx.StaticText(page, -1, disease1, (600, 140))
		wx.StaticText(page, -1, disease2, (600, 180))
		wx.StaticText(page, -1, disease3, (600, 220))
		wx.StaticText(page, -1, disease4, (600, 260))
		wx.StaticText(page, -1, disease5, (600, 300))


		referFont = wx.Font(28, wx.DECORATIVE, wx.DEFAULT, wx.BOLD)
		referTxt = "Refer"
		refer = wx.StaticText(page, -1, referTxt, (800, 450), (-1, -1), wx.ALIGN_CENTER)
		refer.SetBackgroundColour('yellow')
		refer.SetForegroundColour('red')
		refer.SetFont(referFont)


		notReferTxt = "Not Refer"
		notRefer = wx.StaticText(page, -1, notReferTxt, (800, 500), (-1, -1), wx.ALIGN_CENTER)
		notRefer.SetBackgroundColour('maroon')
		notRefer.SetForegroundColour('green')
		notRefer.SetFont(referFont)
		'''
