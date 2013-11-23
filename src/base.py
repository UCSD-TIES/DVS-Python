import wx
from page import *

class base(wx.Frame):
	def __init__(self, parent, id, title, pos, size, style):
		#main frame setup, holds everything
		#wx.Frame(parent, id=-1, title=EmptyString, pos=DefaultPosition,
		#		size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
		base = wx.Frame(parent, id, title, pos, size, style)
		pageSizer = wx.BoxSizer(wx.VERTICAL)
		base.SetSizer(pageSizer)
		#add things to panel, then add to the sizers

		#initialize pages from page class
		#see page.py constructor for parameter usage

		page(base, pageSizer)
		#put pages into a vector so all pages can modified at once
		#setup base frame
		base.Centre()
		#base.Maximize()
		base.Show()