import wx, os
from interaction import *

class page(wx.Panel):

	def __init__(self, parent, baseSizer):
		self.page1 = wx.Panel(parent)
		self.pageSetUp(self.page1)
		baseSizer.Add(self.page1, 1, wx.EXPAND)
		self.page2 = wx.Panel(parent)
		self.pageSetUp2(self.page2)
		baseSizer.Add(self.page2, 1, wx.EXPAND)
		self.page2.Hide()

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

	def pageSetUp(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)
		# instantiate the class for interactivity
		interact = interaction()

		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(3, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 5, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)
		upload = wx.FlexGridSizer(1, 4, 5, 5)

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)
		verImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		horImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Welcome to DVS")

		# Displays path of horizontal image, uneditable
		horPhotoTxt = wx.TextCtrl(page, size=(350,-1), style=wx.TE_READONLY)
		horPhotoTxt.SetValue("Please upload an image.")
		verPhotoTxt = wx.TextCtrl(page, size=(350,-1), style=wx.TE_READONLY)
		verPhotoTxt.SetValue("Please upload an image.")


		###################BUTTONS####################
		nextBtn = wx.Button(page, label='Next')
		#btnNext.Bind(wx.EVT_BUTTON, lambda event:
				#self.onNext(event, self.horPhotoTxt.GetValue(),
				#self.vertPhotoTxt.GetValue()))
		nextBtn.Bind(wx.EVT_BUTTON,
			lambda event: interact.next1(horPhotoTxt.GetValue(), verPhotoTxt.GetValue(), self.page1, self.page2))

		# Button to clear pictures and paths
		resetBtn = wx.Button(page, label='Reset')
		resetBtn.Bind(wx.EVT_BUTTON,
			lambda event: interact.reset(page, horImgCtrl, verImgCtrl, horPhotoTxt, verPhotoTxt))
				
		# Button to upload a horizontal photo
		horiBtn = wx.Button(page, label='Horizontal')
		horiBtn.Bind(wx.EVT_BUTTON,
			lambda event: interact.upload(page, horImgCtrl, horPhotoTxt))

		# Button to upload a vertical photo
		vertBtn = wx.Button(page, label='Vertical')
		vertBtn.Bind(wx.EVT_BUTTON, 
			lambda event: interact.upload(page, verImgCtrl, verPhotoTxt))

		###################ADDING_STUFF#################
		# Adding items into the grids
		mainGrid.AddMany([(menu),(upload),(pics)])

		menu.AddMany([(title),(315,0),(resetBtn), (275,0),(nextBtn)])
		pics.AddMany([(horImgCtrl),(verImgCtrl)])
		upload.AddMany([(horPhotoTxt),(horiBtn),(verPhotoTxt),(vertBtn)])

		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)

	def pageSetUp2(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)
		# instantiate the class for interactivity
		interact = interaction()

		##############SIZERS#####################
		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(3, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 5, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)

		###############COMPONENTS################
		verImg = wx.EmptyImage(440,440)
		verImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(verImg))
		horImg = wx.EmptyImage(440,440)
		horImgCtrl = wx.StaticBitmap(page, -1, wx.BitmapFromImage(horImg))

		title = wx.StaticText(page, label="Are these the eyes?")

		yesBtn = wx.Button(page, label='Yes')

		noBtn = wx.Button(page, label='No')

		mainGrid.AddMany([(menu),(pics)])
		menu.AddMany([(title),(560,0),(yesBtn),(noBtn)])
		pics.AddMany([(horImgCtrl),(verImgCtrl)])


		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)
