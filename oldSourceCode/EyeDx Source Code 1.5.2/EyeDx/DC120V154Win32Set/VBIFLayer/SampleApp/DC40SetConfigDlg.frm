VERSION 4.00Begin VB.Form DC40SetConfigDlg    Caption         =   "DCSetConfig(DC40)"   ClientHeight    =   6480   ClientLeft      =   660   ClientTop       =   1770   ClientWidth     =   8400   Height          =   6885   Left            =   600   LinkTopic       =   "DC40SetConfigDlg"   ScaleHeight     =   6480   ScaleWidth      =   8400   Top             =   1425   Width           =   8520   Begin VB.TextBox Text1       Height          =   270      Index           =   16      Left            =   5160      TabIndex        =   57      Text            =   "Text1"      Top             =   5520      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   15      Left            =   5160      TabIndex        =   55      Text            =   "Text1"      Top             =   5160      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   0      Left            =   1920      TabIndex        =   26      Text            =   "Text1"      Top             =   3000      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   1      Left            =   1920      TabIndex        =   25      Text            =   "Text1"      Top             =   3360      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   2      Left            =   1920      TabIndex        =   24      Text            =   "Text1"      Top             =   3720      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   3      Left            =   1920      TabIndex        =   23      Text            =   "Text1"      Top             =   4080      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   4      Left            =   1920      TabIndex        =   22      Text            =   "Text1"      Top             =   4440      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   5      Left            =   1920      TabIndex        =   21      Text            =   "Text1"      Top             =   4800      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   6      Left            =   1920      TabIndex        =   20      Text            =   "Text1"      Top             =   5160      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   7      Left            =   1920      TabIndex        =   19      Text            =   "Text1"      Top             =   5520      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   8      Left            =   1920      TabIndex        =   18      Text            =   "Text1"      Top             =   5880      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   9      Left            =   5160      TabIndex        =   17      Text            =   "Text1"      Top             =   3000      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   10      Left            =   5160      TabIndex        =   16      Text            =   "Text1"      Top             =   3360      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   11      Left            =   5160      TabIndex        =   15      Text            =   "Text1"      Top             =   3720      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   12      Left            =   5160      TabIndex        =   14      Text            =   "Text1"      Top             =   4080      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   13      Left            =   5160      TabIndex        =   13      Text            =   "Text1"      Top             =   4440      Width           =   1335   End   Begin VB.TextBox Text1       Height          =   270      Index           =   14      Left            =   5160      TabIndex        =   12      Text            =   "Text1"      Top             =   4800      Width           =   1335   End   Begin VB.TextBox Text2       Height          =   270      Index           =   0      Left            =   1440      TabIndex        =   11      Text            =   "Text2"      Top             =   840      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   1      Left            =   1440      TabIndex        =   10      Text            =   "Text2"      Top             =   1200      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   2      Left            =   1440      TabIndex        =   9      Text            =   "Text2"      Top             =   1560      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   3      Left            =   3360      TabIndex        =   8      Text            =   "Text2"      Top             =   840      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   4      Left            =   3360      TabIndex        =   7      Text            =   "Text2"      Top             =   1200      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   5      Left            =   3360      TabIndex        =   6      Text            =   "Text2"      Top             =   1560      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   6      Left            =   5280      TabIndex        =   5      Text            =   "Text2"      Top             =   840      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   7      Left            =   5280      TabIndex        =   4      Text            =   "Text2"      Top             =   1200      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   8      Left            =   5280      TabIndex        =   3      Text            =   "Text2"      Top             =   1560      Width           =   855   End   Begin VB.TextBox Text2       Height          =   270      Index           =   9      Left            =   1200      TabIndex        =   2      Text            =   "Text2"      Top             =   2040      Width           =   3615   End   Begin VB.CommandButton OK       Caption         =   "OK"      Default         =   -1  'True      Height          =   375      Left            =   6960      TabIndex        =   1      Top             =   240      Width           =   1095   End   Begin VB.CommandButton Cancel       Caption         =   "Cancel"      Height          =   375      Left            =   6960      TabIndex        =   0      Top             =   720      Width           =   1095   End   Begin VB.Label Label1       Caption         =   "ManualFNumber :"      Height          =   255      Index           =   16      Left            =   3480      TabIndex        =   58      Top             =   5520      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "ManualExpTime :"      Height          =   255      Index           =   15      Left            =   3480      TabIndex        =   56      Top             =   5160      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "SleepTimeout :"      Height          =   255      Index           =   0      Left            =   360      TabIndex        =   54      Top             =   3000      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "AcknowledgeMode :"      Height          =   255      Index           =   1      Left            =   360      TabIndex        =   53      Top             =   3360      Width           =   1575   End   Begin VB.Label Label1       Caption         =   "DefExpMode :"      Height          =   255      Index           =   2      Left            =   360      TabIndex        =   52      Top             =   3720      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "DefTimerMode :"      Height          =   255      Index           =   3      Left            =   360      TabIndex        =   51      Top             =   4080      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "UpDownMode :"      Height          =   255      Index           =   5      Left            =   360      TabIndex        =   50      Top             =   4800      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "ExpMode :"      Height          =   255      Index           =   6      Left            =   360      TabIndex        =   49      Top             =   5160      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "TimerMode :"      Height          =   255      Index           =   7      Left            =   360      TabIndex        =   48      Top             =   5520      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "FlashMode :"      Height          =   255      Index           =   8      Left            =   360      TabIndex        =   47      Top             =   5880      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "BeepButton :"      Height          =   255      Index           =   9      Left            =   3480      TabIndex        =   46      Top             =   3000      Width           =   1695   End   Begin VB.Label Label1       Caption         =   "BeepEvent :"      Height          =   255      Index           =   10      Left            =   3480      TabIndex        =   45      Top             =   3360      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "DeleteLast :"      Height          =   255      Index           =   11      Left            =   3480      TabIndex        =   44      Top             =   3720      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "DeleteAll :"      Height          =   255      Index           =   12      Left            =   3480      TabIndex        =   43      Top             =   4080      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "PictMode :"      Height          =   255      Index           =   13      Left            =   3480      TabIndex        =   42      Top             =   4440      Width           =   1695   End   Begin VB.Label Label1       Caption         =   "ManualExpFlag :"      Height          =   255      Index           =   14      Left            =   3480      TabIndex        =   41      Top             =   4800      Width           =   1455   End   Begin VB.Label Label1       Caption         =   "DefFlashMode :"      Height          =   255      Index           =   4      Left            =   360      TabIndex        =   40      Top             =   4440      Width           =   1455   End   Begin VB.Label Label2       Caption         =   "tm_sec :"      Height          =   255      Index           =   0      Left            =   600      TabIndex        =   39      Top             =   840      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_min :"      Height          =   255      Index           =   1      Left            =   600      TabIndex        =   38      Top             =   1200      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_hour :"      Height          =   255      Index           =   2      Left            =   600      TabIndex        =   37      Top             =   1560      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_mday :"      Height          =   255      Index           =   3      Left            =   2520      TabIndex        =   36      Top             =   840      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_mon :"      Height          =   255      Index           =   4      Left            =   2520      TabIndex        =   35      Top             =   1200      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_year :"      Height          =   255      Index           =   5      Left            =   2520      TabIndex        =   34      Top             =   1560      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_wday :"      Height          =   255      Index           =   6      Left            =   4440      TabIndex        =   33      Top             =   840      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_yday :"      Height          =   255      Index           =   7      Left            =   4440      TabIndex        =   32      Top             =   1200      Width           =   735   End   Begin VB.Label Label2       Caption         =   "tm_isdst :"      Height          =   255      Index           =   8      Left            =   4440      TabIndex        =   31      Top             =   1560      Width           =   735   End   Begin VB.Label Label2       Caption         =   "CamId :"      Height          =   255      Index           =   9      Left            =   360      TabIndex        =   30      Top             =   2040      Width           =   735   End   Begin VB.Label Label3       Caption         =   "GenericConfig"      Height          =   255      Left            =   240      TabIndex        =   29      Top             =   240      Width           =   1095   End   Begin VB.Label Label4       Caption         =   "Time"      Height          =   255      Left            =   360      TabIndex        =   28      Top             =   600      Width           =   855   End   Begin VB.Label Label5       Caption         =   "FullConfig(DC40Config)"      Height          =   255      Left            =   240      TabIndex        =   27      Top             =   2640      Width           =   2055   EndEndAttribute VB_Name = "DC40SetConfigDlg"Attribute VB_Creatable = FalseAttribute VB_Exposed = FalsePrivate Sub Cancel_Click()    Unload DC40SetConfigDlgEnd SubPrivate Sub OK_Click()    Dim Ret As Integer    Dim Cnt As Integer, TempStr As String        Form1.StatusBar1.SimpleText = "Now Calling DCSetConfig..."    Form1.Refresh        GenericConfig.Time.tm_sec = Text2(0).Text    GenericConfig.Time.tm_min = Text2(1).Text    GenericConfig.Time.tm_hour = Text2(2).Text    GenericConfig.Time.tm_mday = Text2(3).Text    GenericConfig.Time.tm_mon = Text2(4).Text    GenericConfig.Time.tm_year = Text2(5).Text    GenericConfig.Time.tm_wday = Text2(6).Text    GenericConfig.Time.tm_yday = Text2(7).Text    GenericConfig.Time.tm_isdst = Text2(8).Text    TempStr = Text2(9).Text    For Cnt = 0 To Len(TempStr) - 1        GenericConfig.CamId(Cnt) = Asc(Mid(TempStr, Cnt + 1, 1))    Next Cnt    GenericConfig.CamId(Cnt) = &H0        FullDC40Config.SleepTimeout = DC40SetConfigDlg.Text1(0).Text    FullDC40Config.AcknowledgeMode = DC40SetConfigDlg.Text1(1).Text    FullDC40Config.DefExpMode = DC40SetConfigDlg.Text1(2).Text    FullDC40Config.DefTimerMode = DC40SetConfigDlg.Text1(3).Text    FullDC40Config.DefFlashMode = DC40SetConfigDlg.Text1(4).Text    FullDC40Config.UpDownMode = DC40SetConfigDlg.Text1(5).Text    FullDC40Config.ExpMode = DC40SetConfigDlg.Text1(6).Text    FullDC40Config.TimerMode = DC40SetConfigDlg.Text1(7).Text    FullDC40Config.FlashMode = DC40SetConfigDlg.Text1(8).Text    FullDC40Config.BeepButton = DC40SetConfigDlg.Text1(9).Text    FullDC40Config.BeepEvent = DC40SetConfigDlg.Text1(10).Text    FullDC40Config.DeleteLast = DC40SetConfigDlg.Text1(11).Text    FullDC40Config.DeleteAll = DC40SetConfigDlg.Text1(12).Text    FullDC40Config.PictMode = DC40SetConfigDlg.Text1(13).Text    FullDC40Config.ManualExpFlag = DC40SetConfigDlg.Text1(14).Text    FullDC40Config.ManualExpTime = DC40SetConfigDlg.Text1(15).Text    FullDC40Config.ManualFNumber = DC40SetConfigDlg.Text1(16).Text    Ret = DCSetConfig(CameraData, GenericConfig, FullDC40Config)    Form1.StatusBar1.SimpleText = "DCSetConfig:" & DCMakeErrorMessage(Ret)    Unload DC40SetConfigDlgEnd Sub