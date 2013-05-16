#!/user/bin/env python
import wx, os
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, pos=(0,0), size=wx.DisplaySize())
        self.panel = wx.Panel(self)

        self.CreateStatusBar()
        
        self.PhotoMaxSize = 440
        
        # Setting up the menu.
        filemenu = wx.Menu()

        #wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidget
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.createWidgets()


        self.panel.Show(True)        
        self.Show(True)

    def createWidgets(self):
        # Welcome message
        welcome = "Welcome to DVS!"
        welcomeFont = wx.Font(13, wx.NORMAL, wx.NORMAL, wx.BOLD)
        welcomemsg = wx.StaticText(self.panel, -1, welcome)
        welcomemsg.SetFont(welcomeFont)

        # Horizontal Image
        img = wx.EmptyImage(440,440)
        self.imgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                  wx.BitmapFromImage(img))

        self.photoTxt = wx.TextCtrl(self.panel, size=(350,-1))

        horiBtn = wx.Button(self.panel, label='Horizontal')
        horiBtn.Bind(wx.EVT_BUTTON, self.openFile)


        # Vertical Image
        # I did this the dumb way because I don't know how to use parameters
        # in Python :/ So I made an exact replica of a method.. haha. Might
        # be helpful to differentiate, however.
        img2 = wx.EmptyImage(440,440)
        self.imgCtrl2 = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                        wx.BitmapFromImage(img2))

        self.photoTxt2 = wx.TextCtrl(self.panel, size=(350,-1))
        
        vertiBtn = wx.Button(self.panel, label='Vertical')
        vertiBtn.Bind(wx.EVT_BUTTON, self.openFile2)


        # Resolve Layout Issues
        self.height = wx.BoxSizer(wx.VERTICAL)
        self.header = wx.BoxSizer(wx.HORIZONTAL)
        self.sizzle = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.height.Add(self.header, 0, wx.ALL | wx.CENTER, 5)
        self.height.Add(self.sizzle, 0, wx.ALL | wx.CENTER, 5)

        self.header.Add(welcomemsg, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        self.sizzle.Add(self.leftSizer, 0, wx.LEFT | wx.EXPAND, 5)

        self.leftSizer.Add(self.imgCtrl, 0, wx.ALL | wx.LEFT, 5)
        self.leftSizer.Add(self.sizer, 0, wx.ALL | wx.LEFT |
                           wx.EXPAND, 5)

        self.sizer.Add(self.photoTxt, 0, wx.ALL | wx.LEFT, 5)
        self.sizer.Add(horiBtn, 0, wx.ALL | wx.LEFT, 5)

        self.sizzle.Add(self.rightSizer, 0, wx.RIGHT | wx.EXPAND, 5)

        self.rightSizer.Add(self.imgCtrl2, 0, wx.ALL | wx.RIGHT, 5)
        self.rightSizer.Add(self.sizer2, 0, wx.ALL | wx.RIGHT |
                            wx.EXPAND, 5)
        self.sizer2.Add(self.photoTxt2, 0, wx.ALL | wx.RIGHT, 5)
        self.sizer2.Add(vertiBtn, 0, wx.ALL | wx.RIGHT, 5)

        self.panel.SetSizer(self.height)
        self.panel.Layout()
        

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK )
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True) # Close the frame.
 
    def openFile(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*",
                            wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.photoTxt.SetValue(path)

        dlg.Destroy()
        self.OnPaint()

    def OnPaint(self):
        filepath = self.photoTxt.GetValue()
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()

        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW,NewH)

        self.imgCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()


    def openFile2(self, event):
        dlg2 = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*",
                            wx.OPEN)
        if dlg2.ShowModal() == wx.ID_OK:
            path2 = dlg2.GetPath()
            self.photoTxt2.SetValue(path2)

        dlg2.Destroy()
        self.OnPaint2()

    def OnPaint2(self):
        filepath2 = self.photoTxt2.GetValue()
        img2 = wx.Image(filepath2, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        W2 = img2.GetWidth()
        H2 = img2.GetHeight()

        if W2 > H2:
            NewW2 = self.PhotoMaxSize
            NewH2 = self.PhotoMaxSize * H2 / W2
        else:
            NewH2 = self.PhotoMaxSize
            NewW2 = self.PhotoMaxSize * W2 / H2
        img2 = img2.Scale(NewW2,NewH2)

        self.imgCtrl2.SetBitmap(wx.BitmapFromImage(img2))
        self.panel.Refresh()

        
if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, 'Digital Vision Screening')
    app.MainLoop()


#old stuff
"""
import wx, os
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, pos = (0, 0), size=wx.DisplaySize())
        panel = wx.Panel(self)

        IMGMASK = "JPEG Files |*.jpg|" \
                  ".BMP Files |*.bmp|" \
                  "All Files |*.*"

        # frame size = (width, length)
        horizontal = wx.Button(panel, 1, 'Horizontal', (50, 130), (110, -1))
        vertical = wx.Button(panel, 2, 'Vertical', (400, 130), (110, -1))

        self.Bind(wx.EVT_BUTTON, self.openFile, horizontal)
        self.Bind(wx.EVT_BUTTON, self.openFile, vertical)

        #Welcome message
        welcome = 'Welcome to DVS!'
        # SetPointSize(self, 20)
        wx.StaticText(panel, -1, welcome, pos=(250,10))

        # Setting up the menu.
        filemenu = wx.Menu()

        #wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWIdget
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    	#Button to close
        xButton=wx.Button(panel,label="Close", pos=(500,600))
        xButton.Bind(wx.EVT_BUTTON, self.OnExit)
        
        self.Show(True)

    #add image in screens

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK )
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True) # Close the frame.


    def openFile(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            mypath = os.path.basename(path)
        dlg.Destroy()

app = wx.App(False)
frame = MyFrame(None, 'Digital Vision Screening')
app.MainLoop()
"""
