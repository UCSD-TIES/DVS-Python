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
		page1inst = page(base, 1)
		#page2inst = page(base, 2)

		page1obj = page1inst.getPage()
		#page2obj = page2inst.getPage()
		#page2obj.Hide()
		#page2inst.ShowYourself()


		pageSizer.Add(page1obj, 1, wx.EXPAND)
		pageSizer.Add(page2obj, 1, wx.EXPAND)

		#page3.GetParent().GetSizer().Show(page2)
		#page3.GetParent().GetSizer().Layout()


		#setup base frame
		base.Centre()
		#base.Maximize()
		base.Show()