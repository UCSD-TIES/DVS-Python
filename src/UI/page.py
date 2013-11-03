import wx, os
from interaction import *

class page(wx.Panel):
	def __init__(self, parent, pageNum):
		if pageNum == 1:
			page = wx.Panel(parent)
			self.pageSetUp(page)
		elif pageNum == 2:
			page = wx.Panel(parent)
			self.pageSetUp(page)

	def pageSetUp(self, page):
		# instantiate the most outer sizer
		vbox = wx.BoxSizer(wx.VERTICAL)
		# instantiate the class for interactivity
		interact = interaction()

		# mainGrid has three FlexGrids inside it
		# wx.FlexGridSizer(rows, cols, vgap, hgap)
		mainGrid = wx.FlexGridSizer(3, 1, 5, 5)
		menu = wx.FlexGridSizer(1, 3, 5, 5)
		pics = wx.FlexGridSizer(1, 2, 5, 5)
		upload = wx.FlexGridSizer(1, 4, 5, 5)

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

		nextBtn = wx.Button(page, label='Next')
		#btnNext.Bind(wx.EVT_BUTTON, lambda event:
     	#self.onNext(event, self.horPhotoTxt.GetValue(),
        #			self.vertPhotoTxt.GetValue()))

		# Button to upload a horizontal photo
		horiBtn = wx.Button(page, label='Horizontal')
		horiBtn.Bind(wx.EVT_BUTTON,
					lambda event: interact.upload(page,verImgCtrl, horPhotoTxt))

		# Button to upload a vertical photo
		vertBtn = wx.Button(page, label='Vertical')
		vertBtn.Bind(wx.EVT_BUTTON, 
					lambda event: interact.upload(page,horImgCtrl, verPhotoTxt))

		# Adding items into the grids
		mainGrid.AddMany([(menu),(pics),(upload)])

		menu.AddMany([(title),(680,0),(nextBtn)])
		pics.AddMany([(verImgCtrl),(horImgCtrl)])
		upload.AddMany([(horPhotoTxt),(horiBtn),(verPhotoTxt),(vertBtn)])


		vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=40)
		page.SetSizer(vbox)
		