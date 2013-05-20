#!/user/bin/env python
import wx, os

# file filter for pictures: bitmap and jpeg files
IMGMASK = "JPEG Files(*.jpg;*.jpeg;*.jpe;*.jfif) " \
          "|*.jpg; *.jpeg; *.jpe; *.jfif|" \
          "Raw Files |*.cr2; *crw|" \
          "All Files |*.*"

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

        # Passes to createWidgets method definition
        self.createWidgets()

        self.panel.Show(True)        
        self.Show(True)

#----------------------------------------------------------------------------

    def createWidgets(self):
        # Welcome message
        welcome = "Welcome to DVS!"
        welcomeFont = wx.Font(13, wx.NORMAL, wx.NORMAL, wx.BOLD)
        welcomemsg = wx.StaticText(self.panel, -1, welcome)
        welcomemsg.SetFont(welcomeFont)

        # Horizontal Image
        horImg = wx.EmptyImage(440,440)
        self.horImgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                  wx.BitmapFromImage(horImg))

        # Displays path of horizontal image
        self.horPhotoTxt = wx.TextCtrl(self.panel, size=(350,-1))

        horiBtn = wx.Button(self.panel, label='Horizontal')
        horiBtn.Bind(wx.EVT_BUTTON, self.horOpenFile)


        # Vertical Image
        # I did this the dumb way because I don't know how to use parameters
        # in Python :/ So I made an exact replica of a method.. haha. Might
        # be helpful to differentiate, however.
        vertImg = wx.EmptyImage(440,440)
        self.vertImgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                        wx.BitmapFromImage(vertImg))

        # Displays path of vertical image
        self.vertPhotoTxt = wx.TextCtrl(self.panel, size=(350,-1))
        
        vertiBtn = wx.Button(self.panel, label='Vertical')
        vertiBtn.Bind(wx.EVT_BUTTON, self.vertOpenFile)

#------------------------------------------------------------------------------

        # Resolve Layout Issues
        self.full = wx.BoxSizer(wx.VERTICAL)
        
        self.header = wx.BoxSizer(wx.HORIZONTAL)
        self.body = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.horBrowseAndText = wx.BoxSizer(wx.HORIZONTAL)
        self.vertBrowseAndText = wx.BoxSizer(wx.HORIZONTAL)

        # This aligns the whole layout vertically, including header, body,
        # and bottom line (staticLine).
        self.full.Add(self.header, 0, wx.ALL | wx.CENTER, 5)
        self.full.Add(self.body, 0, wx.ALL | wx.CENTER, 5)
        self.full.Add(wx.StaticLine(self.panel, wx.ID_ANY),
                        0, wx.ALL|wx.EXPAND, 5)

        # This centers the welcome message ("Welcome to DVS!") and puts
        # it at the top.
        self.header.Add(welcomemsg, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)

        # This portions the left side of the layout, including left
        # image, left browse button (horizontal button), and left text
        # control box, which contains the path of the horizontal image.
        self.body.Add(self.leftSizer, 0, wx.LEFT | wx.EXPAND, 5)
        self.leftSizer.Add(self.horImgCtrl, 0, wx.ALL | wx.LEFT, 5)

        # Within the leftSizer container, we have a miniature sizer, called
        # horBrowseAndText, which allows us to format the text control box
        # and the horizontal browse button. 
        self.leftSizer.Add(self.horBrowseAndText, 0, wx.ALL | wx.LEFT |
                           wx.EXPAND, 5)

        self.horBrowseAndText.Add(self.horPhotoTxt, 0, wx.ALL | wx.LEFT, 5)
        self.horBrowseAndText.Add(horiBtn, 0, wx.ALL | wx.LEFT, 5)


        # This portions the right side of the layout, including right image,
        # right browse button (vertical button), and right text control box,
        # which contains the path of the horizontal image.
        self.body.Add(self.rightSizer, 0, wx.RIGHT | wx.EXPAND, 5)
        self.rightSizer.Add(self.vertImgCtrl, 0, wx.ALL | wx.RIGHT, 5)

        # Within the rightSizer container, we have a miniature sizer called
        # vertBrowseAndText, which allows us to format the text control box
        # and the vertical browse button.
        self.rightSizer.Add(self.vertBrowseAndText, 0, wx.ALL | wx.RIGHT |
                            wx.EXPAND, 5)
        self.vertBrowseAndText.Add(self.vertPhotoTxt, 0, wx.ALL | wx.RIGHT, 5)
        self.vertBrowseAndText.Add(vertiBtn, 0, wx.ALL | wx.RIGHT, 5)

        self.panel.SetSizer(self.full)
        self.panel.Layout()
        

#---------------------------------------------------------------------------
        
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        aboutText = "Eye Diagnostic Program: Please Enter a Vertical and Horizontal Photo"
        dlg = wx.MessageDialog( self, aboutText, "About Sample Editor", wx.OK )
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True) # Close the frame.
 
    def horOpenFile(self, event):
        horDlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", IMGMASK,
                            wx.OPEN)
        if horDlg.ShowModal() == wx.ID_OK:
            horPath = horDlg.GetPath()
            self.horPhotoTxt.SetValue(horPath)
            self.horOnPaint()                  # moved to make code more stable
        # Can't load image from file '': file does not exist

        horDlg.Destroy()

    def horOnPaint(self):
        horFilepath = self.horPhotoTxt.GetValue()
        horImg = wx.Image(horFilepath, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        horW = horImg.GetWidth()
        horH = horImg.GetHeight()

        if horW > horH:
            NewhorW = self.PhotoMaxSize
            NewhorH = self.PhotoMaxSize * horH / horW
        else:
            NewhorH = self.PhotoMaxSize
            NewhorW = self.PhotoMaxSize * horW / horH
        horImg = horImg.Scale(NewhorW,NewhorH)

        self.horImgCtrl.SetBitmap(wx.BitmapFromImage(horImg))
        self.panel.Refresh()


    def vertOpenFile(self, event):
        vertDlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", IMGMASK,
                            wx.OPEN)
        if vertDlg.ShowModal() == wx.ID_OK:
            vertPath = vertDlg.GetPath()
            self.vertPhotoTxt.SetValue(vertPath)
            self.vertOnPaint()             # moved to make code more stable

        vertDlg.Destroy()
        #self.OnPaint2()

    def vertOnPaint(self):
        vertFilepath = self.vertPhotoTxt.GetValue()
        vertImg = wx.Image(vertFilepath, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        vertW = vertImg.GetWidth()
        vertH = vertImg.GetHeight()

        if vertW > vertH:
            NewvertW = self.PhotoMaxSize
            NewvertH = self.PhotoMaxSize * vertH / vertW
        else:
            NewvertH = self.PhotoMaxSize
            NewvertW = self.PhotoMaxSize * vertW / vertH
        vertImg = vertImg.Scale(NewvertW,NewvertH)

        self.vertImgCtrl.SetBitmap(wx.BitmapFromImage(vertImg))
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
