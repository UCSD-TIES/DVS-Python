; CLW file contains information for the MFC ClassWizard

[General Info]
Version=1
LastClass=CPage2
LastTemplate=CPropertyPage
NewFileInclude1=#include "stdafx.h"
NewFileInclude2=#include "Resize.h"

ClassCount=5
Class1=CResizeApp
Class2=CResizeDlg

ResourceCount=6
Resource2=IDD_RESIZE_DIALOG
Resource1=IDR_MAINFRAME
Resource3=IDD_PAGE1 (English (U.S.))
Resource4=IDD_RESIZE_DIALOG (English (U.S.))
Resource5=IDD_PAGE3 (English (U.S.))
Class3=CResizablePropertySheet
Class4=CPage1
Class5=CPage2
Resource6=IDD_PAGE2 (English (U.S.))

[CLS:CResizeApp]
Type=0
HeaderFile=Resize.h
ImplementationFile=Resize.cpp
Filter=N

[CLS:CResizeDlg]
Type=0
HeaderFile=ResizeDlg.h
ImplementationFile=ResizeDlg.cpp
Filter=D
BaseClass=CDialog
VirtualFilter=dWC



[DLG:IDD_RESIZE_DIALOG]
Type=1
ControlCount=3
Control1=IDOK,button,1342242817
Control2=IDCANCEL,button,1342242816
Control3=IDC_STATIC,static,1342308352
Class=CResizeDlg

[DLG:IDD_RESIZE_DIALOG (English (U.S.))]
Type=1
Class=CResizeDlg
ControlCount=2
Control1=IDC_WIZARD,button,1342242816
Control2=IDC_PROPSHEET,button,1342242816

[CLS:CResizablePropertySheet]
Type=0
HeaderFile=ResizablePropertySheet.h
ImplementationFile=ResizablePropertySheet.cpp
BaseClass=CPropertySheet
LastObject=CResizablePropertySheet

[DLG:IDD_PAGE1 (English (U.S.))]
Type=1
Class=CPage1
ControlCount=9
Control1=IDC_NAMELABEL,static,1342308352
Control2=IDC_NAME,edit,1350631552
Control3=IDC_FRAME,button,1342177287
Control4=IDC_PHONELABEL,static,1342308352
Control5=IDC_PHONE,edit,1350631552
Control6=IDC_NOTESLABEL,static,1342308352
Control7=IDC_NOTES,edit,1352732804
Control8=IDC_FAXLABEL,static,1342308352
Control9=IDC_FAX,edit,1350631552

[DLG:IDD_PAGE2 (English (U.S.))]
Type=1
Class=CPage2
ControlCount=2
Control1=IDC_FILESLABEL,static,1342308352
Control2=IDC_FILES,listbox,1352728835

[DLG:IDD_PAGE3 (English (U.S.))]
Type=1
Class=?
ControlCount=1
Control1=IDC_STATIC,static,1342308352

[CLS:CPage1]
Type=0
HeaderFile=Page1.h
ImplementationFile=Page1.cpp
BaseClass=CPropertyPage
Filter=D
VirtualFilter=idWC
LastObject=CPage1

[CLS:CPage2]
Type=0
HeaderFile=Page2.h
ImplementationFile=Page2.cpp
BaseClass=CPropertyPage
Filter=D
VirtualFilter=idWC
LastObject=IDC_FILES

