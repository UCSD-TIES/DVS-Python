import wx, os
#from Controller import *
from interaction import *
from page import *

app = wx.App()

#main frame setup, holds everything
#wx.Frame(parent, id=-1, title=EmptyString, pos=DefaultPosition,
#	size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
base = wx.Frame(None, -1, 'Digital Vision Screening',
	pos = wx.DefaultPosition,
	size = (1000,600),
	style = wx.DEFAULT_FRAME_STYLE)

#add things to panel, then add to the sizers

#initialize pages from page class
#see page.py constructor for parameter usage
page1 = page(base, 1)

#setup base frame
base.Centre()
#base.Maximize()
base.Show()

# The mainloop is an endless cycle. It catches and dispatches all events 
# that exist during the life of our application.
app.MainLoop()
