import wx
from page import *

class pageact:
	def __init__(self, base, sizer, pageNum):
		addPage(base, sizer, pageNum)

	def addPage(self, base, sizer, pageNum):
		pageInst = page(self.base, pageNum)
		pageObj = pageInst.getPage()
		self.pageSizer.Add(pageObj, 1, wx.EXPAND)
		if pageNum > 1:
			pageObj.Hide()

	#def hidePage(self):