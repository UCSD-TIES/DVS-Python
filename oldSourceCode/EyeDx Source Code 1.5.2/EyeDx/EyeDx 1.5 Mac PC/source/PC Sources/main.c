
#include <stdio.h>

#include <windows.h>

#include <wingdi.h>
#include <winbase.h>
#include <winuser.h>

#include <process.h>
#include "resource.h"
#include "globals.h"


#if defined (WIN32)
	#define IS_WIN32	TRUE
#else
	#define IS_WIN32	FALSE
#endif

#define IS_NT	IS_WIN32 && (BOOL)(GetVersion() < 0x80000000)
#define IS_WIN32S	IS_WIN32 && (BOOL)(!(IS_NT) && \
					(LOBYTE(LOWORD(GetVersion()))<4))
#define IS_WIN95	(BOOL)(!(IS_NT) && !(IS_WIN32S)) && IS_WIN32


		// labels for buttons for main window

#define IDB_RUN_CAM		100

#define IDB_RUN_DISK	101

#define IDB_QUIT		102

#define IDB_VERSION		103

#define IDB_REPORTS		104

#define IDB_UP_SELECT	105

#define IDB_UP_PREV		106

#define IDB_UP_NEXT		107

#define IDB_SIDE_SELECT	108

#define IDB_SIDE_PREV	109

#define IDB_SIDE_NEXT	110

#define IDB_RUN_OK		120

#define IDB_RUN_CANCEL	121

#define IDE_REPORT_NAME	130

#define IDB_ANIMATE		131

		// functions for displaying/removing buttons only called here

void MakeMainMenuButtons(),DeleteMainMenuButtons();

void MakeRunMenuButtons(int),DeleteRunMenuButtons(int);

			// window handles for buttons

HWND	CamRunWnd,DiskRunWnd,QuitWnd,VersionWnd,ReportsWnd;

HWND	UpSelectWnd,SideSelectWnd,RunOKWnd,RunCancelWnd;

HWND	UpNextWnd,UpPrevWnd,SideNextWnd,SidePrevWnd;

HWND	ReportNameWnd,AnimateWnd;



		// a background image is loaded at startup and kept here
static int				BACK_ROWS,BACK_COLS;		// background

static unsigned char	*back_image;				// backg data


LPCTSTR lpszTitle="EyeDx Photoscreener";

BOOL RegisterWin95(CONST WNDCLASS* lpwc);





int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
				LPTSTR lpCmdLine, int nCmdShow)

{
MSG			msg;
HWND		hWnd;
WNDCLASS	wc;


// In Windows 95 or Windows NT the hPrevInstance will always be NULL.

wc.style=CS_HREDRAW | CS_VREDRAW;
wc.lpfnWndProc=(WNDPROC)WndProc;
wc.cbClsExtra=0;
wc.cbWndExtra=0;
wc.hInstance=hInstance;
wc.hIcon=LoadIcon(hInstance,"ID_EYEDX_ICON");
wc.hCursor=LoadCursor(NULL,IDC_ARROW);
wc.hbrBackground=(HBRUSH)(COLOR_WINDOW+1);
wc.lpszMenuName=NULL /* "ID_MAIN_MENU" */;
wc.lpszClassName="EyeDx";

if (IS_WIN95)
  {
  if (!RegisterWin95(&wc))
    return(FALSE);
  }
else if (!RegisterClass(&wc))
  return(FALSE);

hInst=hInstance;

hWnd=CreateWindow("EyeDx",lpszTitle,WS_OVERLAPPEDWINDOW | WS_CLIPCHILDREN,
		CW_USEDEFAULT,0,400,400,NULL,NULL,hInstance,NULL);
if (!hWnd)
  return(FALSE);


ShowWindow(hWnd,nCmdShow);
UpdateWindow(hWnd);

MainWnd=hWnd;


MakeMainMenuButtons();



strcpy(ImagesPath,"C:\\EyeDx\\");

strcpy(DataPath,"C:\\EyeDx\\");

strcpy(report_filename,"No Name");

strcpy(up_filename,"");

strcpy(side_filename,"");

up_image=side_image=NULL;

UP_ROWS=UP_COLS=SIDE_ROWS=SIDE_COLS=0;

RunInProgress=0;

		// user interface used to be able to change all these values

		// while we were researching this, but now they are fixed

DisplayGraphics=1;

SideWhichWay=0;	/* left */

MinIrisRad=MIN_IRIS_RAD;

MaxIrisRad=MAX_IRIS_RAD;

MinPupilRad=MIN_PUPIL_RAD;

MaxPupilRad=MAX_PUPIL_RAD;

MinCRArea=MIN_CR_AREA;

MaxCRArea=MAX_CR_AREA;

BrightThresh=BRIGHT_THRESH;

ZoomSteps=20;

FramePause=2000;

CircleThickness=1;

Flashes=20;



if (ReadImage("EyeDxBg.jpg",&back_image,&BACK_ROWS,&BACK_COLS) == 0)

  {

  MessageBox(MainWnd,"No background set","Warning",MB_APPLMODAL | MB_OK);

  back_image=NULL;

  BACK_ROWS=BACK_COLS=0;

  }

MakeDisplayImage(back_image,BACK_ROWS,BACK_COLS,0);

InvalidateRect(hWnd,NULL,TRUE);

UpdateWindow(hWnd);


while (GetMessage(&msg,NULL,0,0))
  {
  TranslateMessage(&msg);
  DispatchMessage(&msg);
  }
return(msg.wParam);
}



BOOL RegisterWin95(CONST WNDCLASS* lpwc)

{
WNDCLASSEX wcex;

wcex.style=lpwc->style;
wcex.lpfnWndProc=lpwc->lpfnWndProc;
wcex.cbClsExtra=lpwc->cbClsExtra;
wcex.cbWndExtra=lpwc->cbWndExtra;
wcex.hInstance=lpwc->hInstance;
wcex.hIcon=lpwc->hIcon;
wcex.hCursor=lpwc->hCursor;
wcex.hbrBackground=lpwc->hbrBackground;
wcex.lpszMenuName=lpwc->lpszMenuName;
wcex.lpszClassName=lpwc->lpszClassName;
		// Added elements for Windows 95:
wcex.cbSize=sizeof(WNDCLASSEX);
wcex.hIconSm=LoadIcon(wcex.hInstance,"ID_EYEDX_ICON_SM");
return (RegisterClassEx(&wcex));
}



LRESULT CALLBACK WndProc (HWND hWnd, UINT uMsg,
		WPARAM wParam, LPARAM lParam)

{

HDC				hDC;

RECT			MainRect;

HBRUSH			DrawBrush;

char			ExplorerPath[300],ReportsPath[300];

HANDLE			hFind;

WIN32_FIND_DATA	fd;
STARTUPINFO si;
PROCESS_INFORMATION pi;
		

switch (uMsg)
  {
  case WM_COMMAND:
    switch (LOWORD(wParam))
      {

	  case IDB_RUN_DISK:

		DeleteMainMenuButtons();

		MakeRunMenuButtons(1);

		RunInProgress=1;

		DisplayGraphics=0;

		SetWindowText(ReportNameWnd,report_filename);

		MakeDisplayImage(NULL,0,0,0);

		InvalidateRect(hWnd,NULL,TRUE);

	    UpdateWindow(hWnd);

		break;

	  case IDB_RUN_CAM:

		DeleteMainMenuButtons();

		hDC=GetDC(MainWnd);

		TextOut(hDC,0,0,"Connecting to camera...",23);

		ReleaseDC(MainWnd,hDC);

		if (ConnectToCamera() == 0)

		  {

		  CloseCamera();

		  MakeMainMenuButtons();

		  }

		else

		  {

		  RunInProgress=2;

		  MakeRunMenuButtons(0);

		  DisplayGraphics=0;

		  SetWindowText(ReportNameWnd,report_filename);

		  }

		InvalidateRect(hWnd,NULL,TRUE);

	    UpdateWindow(hWnd);

		break;

	  case IDB_RUN_CANCEL:

		if (RunInProgress == 2)

		  DeleteRunMenuButtons(0);

		else

		  DeleteRunMenuButtons(1);

		MakeMainMenuButtons();

		if (RunInProgress == 2)

		  CloseCamera();

		if (side_image != NULL)

		  {

		  free(side_image);

		  side_image=NULL;

		  SIDE_ROWS=SIDE_COLS=0;

		  }

		if (up_image != NULL)

		  {

		  free(up_image);

		  up_image=NULL;

		  UP_ROWS=UP_COLS=0;

		  }

		strcpy(up_filename,"");

		strcpy(side_filename,"");

		MakeDisplayImage(back_image,BACK_ROWS,BACK_COLS,0);

		RunInProgress=0;

		break;

	  case IDB_REPORTS:

		GetWindowsDirectory(ExplorerPath,300);

		if (ExplorerPath[strlen(ExplorerPath)-1] != '\\')

		  strcat(ExplorerPath,"\\");

		strcat(ExplorerPath,"explorer.exe");

		strcpy(ReportsPath,DataPath);

		if (ReportsPath[strlen(ReportsPath)-1] != '\\')

		  strcat(ReportsPath,"\\");

		strcat(ReportsPath,"reports");
		
		// Now tack the reports path onto the explorer path so that it is on
		// the explorer's command line. Note that the reports path must be in
		// double quotes to allow it to contain long file names
		
		strcat(ExplorerPath, " \"");
		strcat(ExplorerPath, ReportsPath);
		strcat(ExplorerPath, "\"");

		ZeroMemory(&si, sizeof(STARTUPINFO));
		si.cb = sizeof(si);
		si.dwFlags = STARTF_FORCEONFEEDBACK;
				
		printf("ExplorerPath = %s\n", ExplorerPath);
		
	   if (CreateProcess(NULL, ExplorerPath, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi) == FALSE)
		  MessageBox(MainWnd,"Unable to start explorer.\n Please look manually.",
						"Reports",MB_OK | MB_APPLMODAL);
		else
		{
			// Get rid of the handles since we don't care about the forked process
			CloseHandle(pi.hProcess);
			CloseHandle(pi.hThread);
		}

		break;
      case IDB_UP_SELECT:

		if (!(SetFilename(hInst,hWnd,"JPG",up_filename)))

		  break;

		if (up_image != NULL)

		  {

		  free(up_image);

		  up_image=NULL;

		  UP_ROWS=UP_COLS=0;

		  }

		if (ReadImage(up_filename,&up_image,&UP_ROWS,&UP_COLS) == 0)

		  strcpy(up_filename,"");

		else

		  MakeDisplayImage(up_image,UP_ROWS,UP_COLS,1);

	    InvalidateRect(hWnd,NULL,TRUE);

	    UpdateWindow(hWnd);

		break;

	  case IDB_UP_NEXT:

		GetIconFromCamera(-1,1);

	    InvalidateRect(hWnd,NULL,TRUE);

	    UpdateWindow(hWnd);

		break;
	  case IDB_UP_PREV:

		GetIconFromCamera(-2,1);

	    InvalidateRect(hWnd,NULL,TRUE);

	    UpdateWindow(hWnd);

		break;

	  case IDB_SIDE_SELECT:

		if (!(SetFilename(hInst,hWnd,"JPG",side_filename)))

		  break;

		if (side_image != NULL)

		  {

		  free(side_image);

		  side_image=NULL;

		  SIDE_ROWS=SIDE_COLS=0;

		  }

		if (ReadImage(side_filename,&side_image,&SIDE_ROWS,&SIDE_COLS) == 0)

		  strcpy(side_filename,"");

		else

		  MakeDisplayImage(side_image,SIDE_ROWS,SIDE_COLS,2);

		InvalidateRect(hWnd,NULL,TRUE);

		UpdateWindow(hWnd);

		break;

	  case IDB_SIDE_NEXT:

		GetIconFromCamera(-1,2);

		InvalidateRect(hWnd,NULL,TRUE);

		UpdateWindow(hWnd);

		break;

	  case IDB_SIDE_PREV:

		GetIconFromCamera(-2,2);

		InvalidateRect(hWnd,NULL,TRUE);

		UpdateWindow(hWnd);

		break;

	  case IDB_RUN_OK:

		GetWindowText(ReportNameWnd,report_filename,MAX_FILENAME_CHARS);

		if (strcmp(up_filename,"") != 0  ||  strcmp(side_filename,"") != 0)

		  {

		  if (strlen(report_filename) == 0)

		    {

		    MessageBox(MainWnd,"You must specify a report name.","No name",

					MB_OK | MB_APPLMODAL);

		    break;

		    }

		  sprintf(ReportsPath,"%s%sreports\\%s.htm",DataPath,

				(DataPath[strlen(DataPath)-1] == '\\' ? "" : "\\"),report_filename);

		  hFind=FindFirstFile(ReportsPath,&fd);

		  FindClose(hFind);

		  if (hFind != INVALID_HANDLE_VALUE)

		    {

		    if (DialogBox(hInst,"ID_REPLACE_DIALOG",MainWnd,(DLGPROC)ContinueDlgProc) == ID_CANCEL)

			  break;

		    }

		  }

		if (RunInProgress == 2)

		  DeleteRunMenuButtons(0);

		else

		  DeleteRunMenuButtons(1);

		hDC=GetDC(MainWnd);

		DrawBrush=CreateSolidBrush(RGB(255,255,255));

		MainRect.top=175; MainRect.bottom=385;

		MainRect.left=5; MainRect.right=385;

		FillRect(hDC,&MainRect,DrawBrush);

		ReleaseDC(MainWnd,hDC);

		DeleteObject(DrawBrush);

		if (RunInProgress == 2)

		  {

		  DownloadImageFromCamera(1,&up_image,&UP_ROWS,&UP_COLS,up_filename);

		  DownloadImageFromCamera(2,&side_image,&SIDE_ROWS,&SIDE_COLS,side_filename);

		  }

		if (up_image != NULL  ||  side_image != NULL)

		  {

		  RunInProgress=3;

		  EyeDx(up_filename,side_filename,SideWhichWay,0);

		  }

		if (side_image != NULL)

		  {

		  free(side_image);

		  side_image=NULL;

		  SIDE_ROWS=SIDE_COLS=0;

		  }

		if (up_image != NULL)

		  {

		  free(up_image);

		  up_image=NULL;

		  UP_ROWS=UP_COLS=0;

		  }

		strcpy(up_filename,"");

		strcpy(side_filename,"");

		RunInProgress=0;

		MakeDisplayImage(back_image,BACK_ROWS,BACK_COLS,0);

		MakeMainMenuButtons();

		InvalidateRect(hWnd,NULL,TRUE);

	    UpdateWindow(hWnd);

		break;

	  case IDB_ANIMATE:

		DisplayGraphics=(DisplayGraphics+1)%2;

		break;

	  case IDB_VERSION:

		DialogBox(hInst,"ID_ABOUT_DIALOG",hWnd,(DLGPROC)ContinueDlgProc);

		MakeDisplayImage(back_image,BACK_ROWS,BACK_COLS,0);

		InvalidateRect(hWnd,NULL,TRUE);

		UpdateWindow(hWnd);

		break;

      case ID_EXIT:case ID_QUIT:case IDB_QUIT:

		if (up_image != NULL)

		  free(up_image);

		if (side_image != NULL)

		  free(side_image);

        DestroyWindow(hWnd);
        break;
      }
    break;

  case WM_SIZE:

	if (hWnd != MainWnd  ||  GetUpdateRect(hWnd,NULL,FALSE) == 0  ||  RunInProgress == 3)

	  {

      return(DefWindowProc(hWnd,uMsg,wParam,lParam));

	  break;

	  }

	if (RunInProgress == 0)

	  MakeDisplayImage(back_image,BACK_ROWS,BACK_COLS,0);

	else if (RunInProgress == 1)

	  {

	  MakeDisplayImage(NULL,0,0,0);	// for white background

	  if (up_image != NULL)

	    MakeDisplayImage(up_image,UP_ROWS,UP_COLS,1);

	  if (side_image != NULL)

	    MakeDisplayImage(side_image,SIDE_ROWS,SIDE_COLS,2);

	  }

	else	// RunInProgress == 2

	  {

	  MakeDisplayImage(NULL,0,0,0);	// for white background

	  GetIconFromCamera(-3,1);

	  GetIconFromCamera(-3,2);

	  }

	InvalidateRect(hWnd,NULL,TRUE);

	UpdateWindow(hWnd);

	break;

  case WM_PAINT:

	if (hWnd != MainWnd  ||  GetUpdateRect(hWnd,NULL,FALSE) == 0)

	  {

      return(DefWindowProc(hWnd,uMsg,wParam,lParam));

	  break;

	  }

	PaintImage();

	if (RunInProgress == 1  ||  RunInProgress == 2)

	  {

	  hDC=GetDC(MainWnd);

	  if (strcmp(up_filename,"") != 0)

	    TextOut(hDC,20,155,up_filename,strlen(up_filename));

	  if (strcmp(side_filename,"") != 0)

	    TextOut(hDC,210,155,side_filename,strlen(side_filename));

	  ReleaseDC(MainWnd,hDC);

	  }

    return(DefWindowProc(hWnd,uMsg,wParam,lParam));

	break;
  case WM_DESTROY:
    PostQuitMessage(0);
    break;
  default:
    return(DefWindowProc(hWnd,uMsg,wParam,lParam));
    break;
  }
return(0L);
}







void MakeMainMenuButtons()



{

CamRunWnd=CreateWindow("BUTTON","Run From Camera",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		10,30,150,32,MainWnd,(HMENU)IDB_RUN_CAM,hInst,NULL);

DiskRunWnd=CreateWindow("BUTTON","Run From Disk",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		10,86,150,32,MainWnd,(HMENU)IDB_RUN_DISK,hInst,NULL);

ReportsWnd=CreateWindow("BUTTON","View Stored Reports",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		10,142,150,32,MainWnd,(HMENU)IDB_REPORTS,hInst,NULL);

VersionWnd=CreateWindow("BUTTON","About EyeDx",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		10,198,150,32,MainWnd,(HMENU)IDB_VERSION,hInst,NULL);

QuitWnd=CreateWindow("BUTTON","Exit Program",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		10,254,150,32,MainWnd,(HMENU)IDB_QUIT,hInst,NULL);

}





void DeleteMainMenuButtons()



{

DestroyWindow(CamRunWnd);

DestroyWindow(DiskRunWnd);

DestroyWindow(ReportsWnd);

DestroyWindow(VersionWnd);

DestroyWindow(QuitWnd);

}





void MakeRunMenuButtons(int Device /* 0 => camera, 1 => disk */)



{

if (Device == 0)

  {

  UpPrevWnd=CreateWindow("BUTTON","Prev",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		25,175,50,32,MainWnd,(HMENU)IDB_UP_PREV,hInst,NULL);

  UpNextWnd=CreateWindow("BUTTON","Next",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		125,175,50,32,MainWnd,(HMENU)IDB_UP_NEXT,hInst,NULL);

  SidePrevWnd=CreateWindow("BUTTON","Prev",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		215,175,50,32,MainWnd,(HMENU)IDB_SIDE_PREV,hInst,NULL);

  SideNextWnd=CreateWindow("BUTTON","Next",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		315,175,50,32,MainWnd,(HMENU)IDB_SIDE_NEXT,hInst,NULL);

  }

else

  {

  UpSelectWnd=CreateWindow("BUTTON","Select Up Image",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		25,175,150,32,MainWnd,(HMENU)IDB_UP_SELECT,hInst,NULL);

  SideSelectWnd=CreateWindow("BUTTON","Select Side Image",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		215,175,150,32,MainWnd,(HMENU)IDB_SIDE_SELECT,hInst,NULL);

  }

RunCancelWnd=CreateWindow("BUTTON","Cancel",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		30,320,150,32,MainWnd,(HMENU)IDB_RUN_CANCEL,hInst,NULL);

RunOKWnd=CreateWindow("BUTTON","OK",

		WS_CHILD | WS_VISIBLE | BS_MULTILINE | BS_CENTER | BS_PUSHBUTTON | BS_TEXT,

		210,320,150,32,MainWnd,(HMENU)IDB_RUN_OK,hInst,NULL);

ReportNameWnd=CreateWindow("EDIT",report_filename,

		WS_CHILD | WS_VISIBLE | WS_BORDER | ES_AUTOHSCROLL,

		95,270,255,22,MainWnd,(HMENU)IDE_REPORT_NAME,hInst,NULL);

AnimateWnd=CreateWindow("BUTTON","Show animation during processing",

		WS_CHILD | WS_VISIBLE | BS_AUTOCHECKBOX | BS_CENTER | BS_TEXT,

		70,235,250,22,MainWnd,(HMENU)IDB_ANIMATE,hInst,NULL);

}





void DeleteRunMenuButtons(int Device /* 0 => camera, 1 => disk */)



{

if (Device == 0)

  {

  DestroyWindow(UpNextWnd);

  DestroyWindow(UpPrevWnd);

  DestroyWindow(SideNextWnd);

  DestroyWindow(SidePrevWnd);

  }

else

  {

  DestroyWindow(UpSelectWnd);

  DestroyWindow(SideSelectWnd);

  }

DestroyWindow(RunOKWnd);

DestroyWindow(RunCancelWnd);

DestroyWindow(ReportNameWnd);

DestroyWindow(AnimateWnd);

}



