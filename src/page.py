import wx, os
from interaction import *

'''
TODO:
- Change pageSetUp to handle ALL pages. This will reduce repeated code.
'''

class page(wx.Panel):

	def __init__(self, parent, baseSizer):

		self.interact = interaction()   # for button functionality, also holds some data
		self.verImgCtrl = None          # There's 2 different imgCtrl's in each page
		self.horImgCtrl = None          # These 2 are just the first page's.
										# They don't even need to be initialized here

		#page setups
		self.page0 = wx.Panel(parent)   # Creates the page, which is a panel
		self.pageSetUp0(self.page0)      # Each page is set up differently
		baseSizer.Add(self.page0, 1, wx.EXPAND)   # Add the page to the frame's sizer
		self.page1 = wx.Panel(parent)   # Creates the page, which is a panel
		self.pageSetUp1(self.page1)      # Each page is set up differently
		baseSizer.Add(self.page1, 1, wx.EXPAND)   # Add the page to the frame's sizer
		self.page2 = wx.Panel(parent)
		self.pageSetUp2(self.page2)
		baseSizer.Add(self.page2, 1, wx.EXPAND)
		self.page3 = wx.Panel(parent)
		self.pageSetUp3(self.page3)
		baseSizer.Add(self.page3, 1, wx.EXPAND)
		self.page4 = wx.Panel(parent)
		self.pageSetUp4(self.page4)
		baseSizer.Add(self.page4, 1, wx.EXPAND)
		self.page5 = wx.Panel(parent)
		self.pageSetUp5(self.page5)
		baseSizer.Add(self.page5, 1, wx.EXPAND)
		self.page1.Hide()
		self.page2.Hide()               # Pages that aren't page 1 start off hidden
		self.page3.Hide()
		self.page4.Hide()
		self.page5.Hide()

		
		# set up result page
		self.resultPage = wx.Panel(parent)
		self.resultPageSetup(self.resultPage)
		baseSizer.Add(self.resultPage, 1, wx.EXPAND)

		# to only test result page, reverse comment the following line
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
	def pageSetUp0(self, page):
                # instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		##############SIZERS#####################
                mainGrid = wx.FlexGridSizer(10, 2, 5, 5)

		###############STATIC TEXT################
                name = wx.StaticText(page, label="Name: ")  
                birth = wx.StaticText(page, label="Date of Birth: ")  
                gender = wx.StaticText(page, label="Gender: ")  
                ethnicity = wx.StaticText(page, label="Ethnicity: ")  
                language = wx.StaticText(page, label="Language: ")  
                roomNumber = wx.StaticText(page, label="Room Number: ")  
                school = wx.StaticText(page, label="School: ")  
                screeningComment = wx.StaticText(page, label="Screening Comment: ")  
                referral = wx.StaticText(page, label="Referral: ")  
                
		###################INPUTS####################
		nameInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		birthInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		genderInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		ethnicityInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		languageInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		roomNumberInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		schoolInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		screeningCommentInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		referralInput = wx.TextCtrl(page, -1, "", size=(175, -1))
		# Passes in path names for both photos, current page, page 2, creates page 2's imgCtrl's		

                ###################Buttons####################
		nextBtn0 = wx.Button(page, label='Next')          # Button for moving onto next page
		nextBtn0.Bind(wx.EVT_BUTTON, lambda event: 
		              self.interact.next0(self.page0, self.page1, 
		                                  nameInput.GetValue(), 
		                                  birthInput.GetValue(), 
		                                  genderInput.GetValue(),
		                                  ethnicityInput.GetValue(),
		                                  languageInput.GetValue(),
		                                  roomNumberInput.GetValue(),
		                                  schoolInput.GetValue(),
		                                  screeningCommentInput.GetValue(),
		                                  referralInput.GetValue()))

		###################ADDING_STUFF#################
	        mainGrid.AddMany([(name),(nameInput)])
	        mainGrid.AddMany([(birth),(birthInput)])
	        mainGrid.AddMany([(gender),(genderInput)])
	        mainGrid.AddMany([(ethnicity),(ethnicityInput)])	        
	        mainGrid.AddMany([(language),(languageInput)])
	        mainGrid.AddMany([(roomNumber),(roomNumberInput)])
	        mainGrid.AddMany([(school),(schoolInput)])
	        mainGrid.AddMany([(screeningComment),(screeningCommentInput)])
	        mainGrid.AddMany([(referral),(referralInput)])
	        mainGrid.AddMany([(nextBtn0)])
	        
	        vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)   # Adds everything to real main sizer
		page.SetSizer(vbox)                                # Sets the main sizer as the page's sizer
	
	def pageSetUp1(self, page):
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
		nextBtn1 = wx.Button(page, label='Next')          # Button for moving onto next page
		nextBtn1.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.next1(horPhotoTxt.GetValue(),
				verPhotoTxt.GetValue(), self.page1, self.page2, self.hor2ImgCtrl, self.ver2ImgCtrl))
		# Passes in path names for both photos, current page, page 2, creates page 2's imgCtrl's

		# Button to clear pictures and paths
		resetBtn = wx.Button(page, label='Reset')
		resetBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.reset(page, self.horImgCtrl,
				self.verImgCtrl, horPhotoTxt, verPhotoTxt, 1))
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
		menu.AddMany([(title),(640,0),(resetBtn),(nextBtn1)])      # Title, large space, reset, next
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

		hRightImg = wx.EmptyImage(1,1)
		self.hRightImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(hRightImg))
		hLeftImg = wx.EmptyImage(1,1)
		self.hLeftImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(hLeftImg))
		vRightImg = wx.EmptyImage(1,1)
		self.vRightImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(vRightImg))
		vLeftImg = wx.EmptyImage(1,1)
		self.vLeftImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(vLeftImg))

		title = wx.StaticText(page, label="Do the boxes frame the eyes?")   # Different title from page 1's

		yesBtn = wx.Button(page, label='Yes')  
		yesBtn.Bind(wx.EVT_BUTTON,         # Button to go to 4th page
			lambda event: self.interact.Yes2(self.page2, self.page4, self.hRightImgCtrl, 
				self.hLeftImgCtrl, self.vRightImgCtrl, self.vLeftImgCtrl))
		# Passes in path names for both photos, current page, page 4, creates page 4's imgCtrl's
			
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

		pic1 = wx.BoxSizer(wx.VERTICAL)
		pic2 = wx.BoxSizer(wx.VERTICAL)

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)
		self.ver3ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		self.hor3ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Please correct the eye detection.")
		# Button to clear pictures and paths
		resetBtn = wx.Button(page, label='Reset')
		resetBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.reset(page, self.hor3ImgCtrl, 
				self.ver3ImgCtrl, None, None, 3))

		# adding see result button
		resultBtn = wx.Button(page, label="See Result")
		resultBtn.Bind(wx.EVT_BUTTON, lambda event: self.interact.seeResult(self.page3, self.resultPage, 1))

		### Mouse events, on click, on drag
		# Mouse events for vertical image
		self.ver3ImgCtrl.Bind(wx.EVT_LEFT_DOWN, lambda event: self.interact.mousePress(event, 1))
		self.ver3ImgCtrl.Bind(wx.EVT_MOTION, lambda event: self.interact.mouseDrag(event,self.ver3ImgCtrl))
		self.ver3ImgCtrl.Bind(wx.EVT_LEFT_UP, lambda event: self.interact.mouseRelease(event, self.ver3ImgCtrl, 1))

		# Mouse events for horizontal image
		self.hor3ImgCtrl.Bind(wx.EVT_LEFT_DOWN, lambda event: self.interact.mousePress(event, 0))
		self.hor3ImgCtrl.Bind(wx.EVT_MOTION, lambda event: self.interact.mouseDrag(event, self.hor3ImgCtrl))
		self.hor3ImgCtrl.Bind(wx.EVT_LEFT_UP, lambda event: self.interact.mouseRelease(event, self.hor3ImgCtrl, 0))

		mainGrid.AddMany([(menu),(pics)])
		menu.AddMany([(title),(560,0),(resetBtn),(resultBtn)])
		pic1.Add(self.hor3ImgCtrl, flag = wx.ALIGN_CENTER)
		pic2.Add(self.ver3ImgCtrl, flag = wx.ALIGN_CENTER)
		pics.AddMany([(pic1),(pic2)])

		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)

	# Set up for page 4 - Page for pupil detection
	def pageSetUp4(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)

		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(3, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 4, 5, 5)
		pics = wx.FlexGridSizer(1, 4, 5, 5)

		pic1 = wx.BoxSizer(wx.VERTICAL)
		pic2 = wx.BoxSizer(wx.VERTICAL)
		pic3 = wx.BoxSizer(wx.VERTICAL)
		pic4 = wx.BoxSizer(wx.VERTICAL)

		###############COMPONENTS################
		hRightImg = wx.EmptyImage(100,100)
		self.hRightImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(hRightImg))
		hLeftImg = wx.EmptyImage(100,100)
		self.hLeftImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(hLeftImg))
		vRightImg = wx.EmptyImage(100,100)
		self.vRightImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(vRightImg))
		vLeftImg = wx.EmptyImage(100,100)
		self.vLeftImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(vLeftImg))

		title = wx.StaticText(page, label="Do the boxes frame the pupils?")   # Different title from page 1's

		yesBtn = wx.Button(page, label='Yes')     # Button to go to result page
		yesBtn.Bind(wx.EVT_BUTTON,
				lambda event: self.interact.seeResult(self.page4, self.resultPage, 1))
			
		noBtn = wx.Button(page, label='No')       # Button to go to 5th page
		noBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.No4(self.page4, self.page5, self.hRightImgCtrl, 
				self.hLeftImgCtrl, self.vRightImgCtrl, self.vLeftImgCtrl))
		# Will pass in image controls of 4th page

		#################ADDING STUFF#################
		# See page 1's set up
		mainGrid.AddMany([(menu),(pics)])
		menu.AddMany([(title),(560,0),(yesBtn),(noBtn)])
		pic1.Add(self.hLeftImgCtrl, flag = wx.ALIGN_RIGHT)
		pic2.Add(self.hRightImgCtrl, flag = wx.ALIGN_RIGHT)
		pic3.Add(self.vLeftImgCtrl, flag = wx.ALIGN_LEFT)
		pic4.Add(self.vRightImgCtrl, flag = wx.ALIGN_LEFT)
		pics.AddMany([(pic1),(pic2),(pic3),(pic4)])

		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)
		
	# Set up for page 5 - Nothing special about this page yet, 
	# This is the user input pupil detection correction page
	def pageSetUp5(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)

		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(2, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 5, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)

		pic1 = wx.BoxSizer(wx.VERTICAL)
		pic2 = wx.BoxSizer(wx.VERTICAL)

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)
		self.ver5ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		self.hor5ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Please correct the pupil detection.")
		# Button to clear pictures and paths
		resetBtn = wx.Button(page, label='Reset')
		resetBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.reset(page, self.hor5ImgCtrl, 
				self.ver5ImgCtrl, None, None, 3))

		# adding see result button
		resultBtn = wx.Button(page, label="See Result")
		resultBtn.Bind(wx.EVT_BUTTON, lambda event: self.interact.seeResult(self.page5, self.resultPage, 1))

		### Mouse events, on click, on drag
		# Mouse events for vertical image
		self.ver5ImgCtrl.Bind(wx.EVT_LEFT_DOWN, lambda event: self.interact.mousePress(event, 1))
		self.ver5ImgCtrl.Bind(wx.EVT_MOTION, lambda event: self.interact.mouseDrag(event,self.ver5ImgCtrl))
		self.ver5ImgCtrl.Bind(wx.EVT_LEFT_UP, lambda event: self.interact.mouseRelease(event, self.ver5ImgCtrl, 1))

		# Mouse events for horizontal image
		self.hor5ImgCtrl.Bind(wx.EVT_LEFT_DOWN, lambda event: self.interact.mousePress(event, 0))
		self.hor5ImgCtrl.Bind(wx.EVT_MOTION, lambda event: self.interact.mouseDrag(event, self.hor5ImgCtrl))
		self.hor5ImgCtrl.Bind(wx.EVT_LEFT_UP, lambda event: self.interact.mouseRelease(event, self.hor5ImgCtrl, 0))

		mainGrid.AddMany([(menu),(pics)])
		menu.AddMany([(title),(560,0),(resetBtn),(resultBtn)])
		pic1.Add(self.hor5ImgCtrl, flag = wx.ALIGN_CENTER)
		pic2.Add(self.ver5ImgCtrl, flag = wx.ALIGN_CENTER)
		pics.AddMany([(pic1),(pic2)])

		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)

	# setup a result page
	def resultPageSetup(self, page):

		# print out title on top left corner of the page
		resultText = "This is result page"
		result = wx.StaticText(page, -1, resultText, (0, 40), (1000, -1), wx.ALIGN_CENTER)
		result.SetBackgroundColour('blue')
		result.SetForegroundColour('white')


		horPhotoTxt = wx.TextCtrl(page, size=(360,-1), style=wx.TE_READONLY)
		verPhotoTxt = wx.TextCtrl(page, size=(360,-1), style=wx.TE_READONLY)

		horPhotoTxt.SetValue("Please upload an image.")
		verPhotoTxt.SetValue("Please upload an image.")

		horPhotoTxt.Hide()
		verPhotoTxt.Hide()


		restartBtn = wx.Button(page, label="Start Over", pos=(840, 520))

		restartBtn.Bind(wx.EVT_BUTTON,
		            lambda event: self.interact.startOver(self.resultPage,
		                                                  self.page1,
		                                                  self.horImgCtrl,
		                                                  self.verImgCtrl,
		                                                  horPhotoTxt,
		                                                  verPhotoTxt,
		                                                  1))
