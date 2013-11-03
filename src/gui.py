import wx, os
#from Controller import *

app = wx.App()

#main frame setup, holds everything
#wx.Frame(parent, id=-1, title=EmptyString, pos=DefaultPosition,
#	size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)

base = wx.Frame(None, -1, 'DVS', pos = wx.DefaultPosition, 
	size = wx.DefaultSize, style = wx.DEFAULT_FRAME_STYLE)

#add things to panel, then add to the sizers
panel = wx.Panel(base)

vbox = wx.BoxSizer(wx.VERTICAL)

#wx.FlexGridSizer(rows, cols, vgap, hgap)
mainGrid = wx.FlexGridSizer(3, 1, 5, 5)
menu = wx.FlexGridSizer(1, 3, 5, 5)
pics = wx.FlexGridSizer(1, 2, 5, 5)
upload = wx.FlexGridSizer(1, 4, 5, 5)

verImg = wx.EmptyImage(440,440)
verImgCtrl = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(verImg))
horImg = wx.EmptyImage(440,440)
horImgCtrl = wx.StaticBitmap(panel, -1, wx.BitmapFromImage(horImg))

title = wx.StaticText(panel, label="Welcome to DVS")
#empty = wx.StaticText(panel, label="empty")

# Displays path of horizontal image, uneditable
horPhotoTxt = wx.TextCtrl(panel, size=(350,-1), style=wx.TE_READONLY)
verPhotoTxt = wx.TextCtrl(panel, size=(350,-1), style=wx.TE_READONLY)


submitBtn = wx.Button(panel, label='Submit')
# Button to upload a horizontal photo
horiBtn = wx.Button(panel, label='Horizontal')
# horiBtn.Bind(wx.EVT_BUTTON, self.horOpenFile)
# Button to upload a vertical photo
vertBtn = wx.Button(panel, label='Vertical')
# vertBtn.Bind(wx.EVT_BUTTON, self.horOpenFile)

mainGrid.AddMany([(menu),(pics),(upload)])

menu.AddMany([(title),(680,3),(submitBtn)])
pics.AddMany([(verImgCtrl),(horImgCtrl)])
upload.AddMany([(horPhotoTxt),(horiBtn),(verPhotoTxt),(vertBtn)])

#menu.AddGrowableCol(3, 1)
#menu.AddGrowableCol(1, 1)


vbox.Add(mainGrid, proportion=1, flag=wx.ALIGN_CENTER|wx.TOP, border=20)

panel.SetSizer(vbox)

base.Centre()
base.Maximize()
base.Show()

# The mainloop is an endless cycle. It catches and dispatches all events 
# that exist during the life of our application.
app.MainLoop()