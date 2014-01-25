import wx, os
from interaction import *

class page(wx.Panel):

	def __init__(self, parent, baseSizer):

		#Image controls and interaction object
		self.interact = interaction()
		self.verImgCtrl = None
		self.horImgCtrl = None

		#page setups
		self.page1 = wx.Panel(parent)
		self.pageSetUp(self.page1)
		baseSizer.Add(self.page1, 1, wx.EXPAND)
		self.page2 = wx.Panel(parent)
		self.pageSetUp2(self.page2)
		baseSizer.Add(self.page2, 1, wx.EXPAND)
		self.page3 = wx.Panel(parent)
		self.pageSetUp3(self.page3)
		baseSizer.Add(self.page3, 1, wx.EXPAND)
		self.page2.Hide()
		self.page3.Hide()

	def getPage(self, pageNum):
		if pageNum == 1:
			return self.page1
		elif pageNum == 2:
			return self.page2

	def ShowYourself(self, page):
		page.Raise()
		page.SetPosition((0,0))
		page.Fit()
		page.GetParent().GetSizer().Show(page)
		page.GetParent().GetSizer().Layout()

	# Set up for page 1
	def pageSetUp(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)
		# instantiate the class for interactivity


		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(3, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 5, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)
		upload = wx.FlexGridSizer(1, 4, 5, 5)

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)
		self.verImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		self.horImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Welcome to DVS")

		# Displays path of horizontal image, uneditable
		horPhotoTxt = wx.TextCtrl(page, size=(350,-1), style=wx.TE_READONLY)
		horPhotoTxt.SetValue("Please upload an image.")
		verPhotoTxt = wx.TextCtrl(page, size=(350,-1), style=wx.TE_READONLY)
		verPhotoTxt.SetValue("Please upload an image.")


		###################BUTTONS####################
		nextBtn = wx.Button(page, label='Next')
		nextBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.next1(horPhotoTxt.GetValue(), 
				verPhotoTxt.GetValue(), self.page1, self.page2, self.hor2ImgCtrl, self.ver2ImgCtrl))

		# Button to clear pictures and paths
		resetBtn = wx.Button(page, label='Reset')
		resetBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.reset(page, self.horImgCtrl, 
				self.verImgCtrl, horPhotoTxt, verPhotoTxt))
				
		# Button to upload a horizontal photo
		horiBtn = wx.Button(page, label='Horizontal')
		horiBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.upload(page, self.horImgCtrl, horPhotoTxt, 0))

		# Button to upload a vertical photo
		vertBtn = wx.Button(page, label='Vertical')
		vertBtn.Bind(wx.EVT_BUTTON, 
			lambda event: self.interact.upload(page, self.verImgCtrl, verPhotoTxt, 1))

		###################ADDING_STUFF#################
		# Adding items into the grids
		mainGrid.AddMany([(menu),(upload),(pics)])

		menu.AddMany([(title),(595,0),(resetBtn),(nextBtn)])
		pics.AddMany([(self.horImgCtrl),(self.verImgCtrl)])
		upload.AddMany([(horPhotoTxt),(horiBtn),(verPhotoTxt),(vertBtn)])

		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)

	# Set up for page 2
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
		verImg = wx.EmptyImage(440,440)
		self.ver2ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		self.hor2ImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Do the boxes frame the eyes?")

		yesBtn = wx.Button(page, label='Yes')

		noBtn = wx.Button(page, label='No')
		noBtn.Bind(wx.EVT_BUTTON,
			lambda event: self.interact.No2(self.page2, self.page3, self.hor3ImgCtrl, self.ver3ImgCtrl))

		mainGrid.AddMany([(menu),(pics)])
		menu.AddMany([(title),(560,0),(yesBtn),(noBtn)])
		pics.AddMany([(self.hor2ImgCtrl),(self.ver2ImgCtrl)])


		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)

	# Set up for page 3
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
