#include <stdio.h>
#include <windows.h>
#include <winuser.h>
#include "globals.h"
#include "DC120.h"
#include "resource.h"

static int				DISPLAY_ROWS,DISPLAY_COLS;	// display window
static unsigned char	*disp_image;				// display data

static int			CameraOpen=0; // 0 => no, 1=> driver, 2=> camera
static DCDriver		Driver;	// Kodak camera hooks
static DCCamera		Camera;
static int			NumOfPicts,UpPictNum=1,SidePictNum=2;
static DCCamMemType	CamOrCard;

		/*
		** Discovers the current size of the main window.
		** Scales the given image data and copies it into a
		** static image kept here for display. Copy may be
		** made into full image window, or only part of it.
		*/

void MakeDisplayImage(unsigned char *RawImage,
					  int RAW_IMAGE_ROWS,int RAW_IMAGE_COLS,
					  int CopyLocation)		// 0 => full,
											// 1 => left icon
											// 2 => right icon

{
int				r,c,r2,c2,StartRow,StartCol;
RECT			MainRect;
static int		LastRows=0,LastCols=0;

GetClientRect(MainWnd,&MainRect);
DISPLAY_ROWS=MainRect.bottom-MainRect.top;
DISPLAY_COLS=MainRect.right-MainRect.left;
if (DISPLAY_ROWS < 100)
  DISPLAY_ROWS=100;
if (DISPLAY_COLS < 100)
  DISPLAY_COLS=100;
if (DISPLAY_ROWS % 4 != 0)	// Windows pads to 4-byte boundaries
  DISPLAY_ROWS=(DISPLAY_ROWS/4+1)*4;
if (DISPLAY_COLS % 4 != 0)
  DISPLAY_COLS=(DISPLAY_COLS/4+1)*4;
		/* free up memory for last displayed image, get new memory */
if (disp_image != NULL  &&  (LastRows != DISPLAY_ROWS  ||  LastCols != DISPLAY_COLS))
  {
  free(disp_image);
  disp_image=NULL;
  }
if (disp_image == NULL)
  {
  disp_image=(unsigned char *)calloc(DISPLAY_ROWS*DISPLAY_COLS*3,1);
  if (disp_image == NULL)
    {
    MessageBox(MainWnd,"Out of memory","MakeDisplayImage()",MB_APPLMODAL | MB_OK);
    exit(0);
    }
//  sprintf(text,"size %d x %d",DISPLAY_COLS,DISPLAY_ROWS);
//  MessageBox(MainWnd,text,"MakeDisplayImage()",MB_APPLMODAL | MB_OK);
  }

LastRows=DISPLAY_ROWS;
LastCols=DISPLAY_COLS;

if (RawImage == NULL)
  {		/* nothing to display; just make empty (white) image */
  for (r=0; r<DISPLAY_ROWS*DISPLAY_COLS*3; r++)
    disp_image[r]=255;
  return;
  }

if (CopyLocation == 0)
  {		// copies image into full window
  for (r=0; r<DISPLAY_ROWS; r++)
    {
    r2=(int)((double)r/(double)DISPLAY_ROWS*(double)RAW_IMAGE_ROWS);
    for (c=0; c<DISPLAY_COLS; c++)
	  {		/* image enters in RGB order, but windows wants it BGR */
      c2=(int)((double)c/(double)DISPLAY_COLS*(double)RAW_IMAGE_COLS);
      disp_image[(r*DISPLAY_COLS+c)*3+0]=RawImage[(r2*RAW_IMAGE_COLS+c2)*3+2];
      disp_image[(r*DISPLAY_COLS+c)*3+1]=RawImage[(r2*RAW_IMAGE_COLS+c2)*3+1];
      disp_image[(r*DISPLAY_COLS+c)*3+2]=RawImage[(r2*RAW_IMAGE_COLS+c2)*3+0];
	  }
    }
  }
else	// copies image into sub-area of window
  {
  StartRow=30;
  if (CopyLocation == 1)
    StartCol=20;
  else
	StartCol=210;
  for (r=StartRow; r<StartRow+THUMB_HEIGHT*2; r++)
    {
    r2=(int)((double)(r-StartRow)/(double)(THUMB_HEIGHT*2)*(double)RAW_IMAGE_ROWS);
    for (c=StartCol; c<StartCol+THUMB_WIDTH*2; c++)
	  {		/* image enters in RGB order, but windows wants it BGR */
      c2=(int)((double)(c-StartCol)/(double)(THUMB_WIDTH*2)*(double)RAW_IMAGE_COLS);
      disp_image[(r*DISPLAY_COLS+c)*3+0]=RawImage[(r2*RAW_IMAGE_COLS+c2)*3+2];
      disp_image[(r*DISPLAY_COLS+c)*3+1]=RawImage[(r2*RAW_IMAGE_COLS+c2)*3+1];
      disp_image[(r*DISPLAY_COLS+c)*3+2]=RawImage[(r2*RAW_IMAGE_COLS+c2)*3+0];
	  }
    }
  }
}



		/*
		** No ins or outs; simply redraws the static image kept
		** here (file static) in the main window.
		*/

void PaintImage()

{
PAINTSTRUCT			Painter;
HDC					hDC;
BITMAPINFOHEADER	bm_info_header;
BITMAPINFO			bm_info;
RECT				outline;
HBRUSH				DrawBrush;

			/* all this stuff is pure windows code */
BeginPaint(MainWnd,&Painter);
hDC=GetDC(MainWnd);
bm_info_header.biSize=sizeof(BITMAPINFOHEADER); 
bm_info_header.biWidth=DISPLAY_COLS;
bm_info_header.biHeight=-DISPLAY_ROWS; 
bm_info_header.biPlanes=1;
bm_info_header.biBitCount=24; 
bm_info_header.biCompression=BI_RGB; 
bm_info_header.biSizeImage=0; 
bm_info_header.biXPelsPerMeter=0; 
bm_info_header.biYPelsPerMeter=0;
bm_info_header.biClrUsed=0; 
bm_info_header.biClrImportant=0;
// bm_info.bmiColors=NULL;
bm_info.bmiHeader=bm_info_header;
SetDIBitsToDevice(hDC,0,0,DISPLAY_COLS,DISPLAY_ROWS,0,0,
			  0, /* first scan line */
			  DISPLAY_ROWS, /* number of scan lines */
			  disp_image,&bm_info,DIB_RGB_COLORS);
if (RunInProgress == 1  ||  RunInProgress == 2)
  {		// for selection windows; outline icons and other stuff
  outline.top=28; outline.bottom=152;
  outline.left=18; outline.right=182;
  DrawBrush=CreateSolidBrush(RGB(0,0,0));
  FrameRect(hDC,&outline,DrawBrush);
  outline.left=208; outline.right=372;
  FrameRect(hDC,&outline,DrawBrush);
  DeleteObject(DrawBrush);
  TextOut(hDC,45,272,"Report name:",12);
  if (RunInProgress == 1)
	TextOut(hDC,0,0,"Run From Disk",13);
  else
	{
	TextOut(hDC,0,0,"Run From Camera",15);
	TextOut(hDC,92,182,"Up",2);
	TextOut(hDC,276,182,"Side",4);
	}
  if ((RunInProgress == 1  &&  up_image == NULL)  ||
	  (RunInProgress == 2  &&  UpPictNum == 0))
	{
    outline.top=30; outline.bottom=150;
    outline.left=20; outline.right=180;
    DrawBrush=CreateSolidBrush(RGB(255,255,255));
    FillRect(hDC,&outline,DrawBrush);
	TextOut(hDC,75,80,"[NONE]",6);
    DeleteObject(DrawBrush);
	}
  if ((RunInProgress == 1  &&  side_image == NULL)  ||
	  (RunInProgress == 2  &&  SidePictNum == 0))
	{
    outline.top=30; outline.bottom=150;
    outline.left=210; outline.right=370;
    DrawBrush=CreateSolidBrush(RGB(255,255,255));
    FillRect(hDC,&outline,DrawBrush);
	TextOut(hDC,265,80,"[NONE]",6);
    DeleteObject(DrawBrush);
	}
  }
ReleaseDC(MainWnd,hDC);
EndPaint(MainWnd,&Painter);
}






			/* Opens a dialog box which scrolls through the file
			** hierarchy and allows the user to select a file. */

char	ReturnFilename[MAX_FILENAME_CHARS];
char	Suffix[5];

BOOL SetFilename(HINSTANCE hInst,
				 HWND hParentWnd,
				 char *Extension,	/* type of file to look for */
				 char *Filename)	/* returned name of file selected */

{
char	*FileOnly;

strcpy(Suffix,Extension);	/* file-global access to suffix */
DialogBox(hInst,"ID_FILE_MENU",hParentWnd,(DLGPROC)OpenFileProc);
if (strlen(ReturnFilename) > 1)
  {		/* set current path to whatever was used to select filename */
  GetFullPathName(ReturnFilename,MAX_FILENAME_CHARS,ImagesPath,&FileOnly);
  *FileOnly='\0';
		/* copy return filename to calling filename */
  strcpy(Filename,ReturnFilename);
  return(TRUE);
  }
return(FALSE);
}



LRESULT CALLBACK OpenFileProc(HWND hDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)

{
char	*FileOnly,CurrentList[MAX_FILENAME_CHARS];

switch(uMsg)
  {
  case WM_INITDIALOG:
	sprintf(ReturnFilename,"%s*.%s",ImagesPath,Suffix);
    DlgDirList(hDlg,ReturnFilename,IDC_LIST,IDC_DIRECTORY,DDL_DIRECTORY | DDL_DRIVES);
	GetFullPathName(ReturnFilename,MAX_FILENAME_CHARS,CurrentList,&FileOnly);
	SetDlgItemText(hDlg,IDC_DIRECTORY,CurrentList);
	break;
  case WM_COMMAND:
	switch(LOWORD(wParam))
	  {
	  case IDC_LIST:
        if (HIWORD(wParam) == LBN_DBLCLK)
		  {
		  if (DlgDirSelectEx(hDlg,ReturnFilename,sizeof(ReturnFilename),IDC_LIST))
			{
			if (strlen(ReturnFilename) == 2  &&  ReturnFilename[1] == ':')
			  lstrcat(ReturnFilename,"\\");
			lstrcat(ReturnFilename,"*.");
			lstrcat(ReturnFilename,Suffix);
			DlgDirList(hDlg,ReturnFilename,IDC_LIST,IDC_DIRECTORY,DDL_DIRECTORY | DDL_DRIVES);
			GetFullPathName(ReturnFilename,MAX_FILENAME_CHARS,CurrentList,&FileOnly);
			SetDlgItemText(hDlg,IDC_DIRECTORY,CurrentList);
		    }
		  else
			{
			EndDialog(hDlg,IDOK);
		    }
		  }
		break;
	  case IDCANCEL:
		strcpy(ReturnFilename,"");
		EndDialog(hDlg,IDCANCEL);
		break;
	  case IDOK:
		GetDlgItemText(hDlg,IDC_DIRECTORY,ReturnFilename,MAX_FILENAME_CHARS);
		if (strlen(ReturnFilename) > 5  &&
			ReturnFilename[strlen(ReturnFilename)-5] == '*')
		  {		/* wildcards in edit box */
		  strcpy(ReturnFilename,"none?");
		  if (DlgDirSelectEx(hDlg,ReturnFilename,sizeof(ReturnFilename),IDC_LIST))
			{	/* user selected directory/drive */
		    MessageBox(hDlg,"Cannot select a directory\n(Try double-clicking.)",
					"Error",MB_OK | MB_APPLMODAL);
			}
		  else if (strcmp(ReturnFilename,"none?") == 0)
			{	/* nothing selected; user clicked ok */
		    strcpy(ReturnFilename,"");
		    EndDialog(hDlg,IDCANCEL);
		    }
		  else	/* something selected, user clicked ok */
			EndDialog(hDlg,IDOK);
		  break;
		  }
		else	/* user typed something in edit box */
		  EndDialog(hDlg,IDOK);
		break;
	  }
	break;
  default:
	return(FALSE);
  }
return(TRUE);
}




			/*
			** To ask the user if it is okay to continue.
			** Used to ask about replacing a file, and used to
			** ask about loading an image of unexpected size.
			*/

LRESULT CALLBACK ContinueDlgProc(HWND hDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)

{
switch(uMsg)
  {
  case WM_COMMAND:
	switch(LOWORD(wParam))
	  {
	  case IDOK:
		EndDialog(hDlg,IDOK);
		break;
	  case IDCANCEL:
		EndDialog(hDlg,IDCANCEL);
		break;
	  }
	break;
  default:
	return(FALSE);
  }
return(TRUE);
}



			/*
			** To ask the user a yes or no question.
			** Used to ask about age of child if crescent is only
			** abnormality detected.
			*/

LRESULT CALLBACK YesNoDlgProc(HWND hDlg, UINT uMsg, WPARAM wParam, LPARAM lParam)

{
switch(uMsg)
  {
  case WM_COMMAND:
	switch(LOWORD(wParam))
	  {
	  case IDYES:
		EndDialog(hDlg,IDYES);
		break;
	  case IDNO:
		EndDialog(hDlg,IDNO);
		break;
	  }
	break;
  default:
	return(FALSE);
  }
return(TRUE);
}



			/*
			** During animation, used to flash located eyes.
			*/

void FlashCircles(unsigned char *Background,
				  int ROWS,int COLS,
				  double circle1[3],
				  double circle2[3])

{
int		i,j,thick,circ,*circle_points,total_circle_points;

circle_points=(int *)calloc(MaxIrisRad*8,sizeof(int));
for (i=0; i<Flashes; i++)
  {
  for (circ=0; circ<2; circ++)
	{
	for (thick=-CircleThickness; thick<=CircleThickness; thick++)
	  {
	  if (circ == 0)
        MakeCircleIndices(circle1[0],circle1[1],circle1[2]+(double)thick,
					ROWS,COLS,circle_points,&total_circle_points);
	  else
        MakeCircleIndices(circle2[0],circle2[1],circle2[2]+(double)thick,
					ROWS,COLS,circle_points,&total_circle_points);
      for (j=0; j<total_circle_points; j++)
	    {
	    if (circle_points[j]/COLS < 0  ||  circle_points[j]/COLS >= ROWS  ||
		    circle_points[j]%COLS < 0  ||  circle_points[j]%COLS >= COLS)
		continue;
        Background[circle_points[j]*3+((i+0)%3)]=255;
        Background[circle_points[j]*3+((i+1)%3)]=128;
        Background[circle_points[j]*3+((i+2)%3)]=0;
		}
	  }
    }
  MakeDisplayImage(Background,ROWS,COLS,0);
  PaintImage();
  }
free(circle_points);
}


			/*
			** During animation, used to zoom in on subimage area.
			*/

void ZoomDisplay(unsigned char *Image,
				int ROWS,int COLS,
				int zy, int zx,
				int ZoomRows,int ZoomCols,
				int ZoomSteps)

{
int	EYE_ROWS,EYE_COLS,EyeX,EyeY,i,dROWS,dCOLS,dx,dy,r,c,r2,c2;

EYE_ROWS=ZoomRows;
EYE_COLS=ZoomCols;
EyeX=zx-EYE_COLS/2;
EyeY=zy-EYE_ROWS/2;
if (EyeX < 0) EyeX=0;
if (EyeY < 0) EyeY=0;
for (i=ZoomSteps; i>=0; i--)
  {
  dROWS=EYE_ROWS+(int)((double)(ROWS-EYE_ROWS)*(double)i/(double)ZoomSteps);
  dCOLS=EYE_COLS+(int)((double)(COLS-EYE_COLS)*(double)i/(double)ZoomSteps);
  dx=EyeX-(int)((double)(EyeX-0)*(double)i/(double)ZoomSteps);
  dy=EyeY-(int)((double)(EyeY-0)*(double)i/(double)ZoomSteps);
  for (r=0; r<DISPLAY_ROWS; r++)
	{
    r2=(int)((double)r/(double)DISPLAY_ROWS*(double)dROWS)+dy;
	for (c=0; c<DISPLAY_COLS; c++)
	  {
      c2=(int)((double)c/(double)DISPLAY_COLS*(double)dCOLS)+dx;
	  if (r2 < 0  ||  r2 >= ROWS  ||  c2 < 0  ||  c2 >= COLS)
		{
		disp_image[(r*DISPLAY_COLS+c)*3+0]=0;
		disp_image[(r*DISPLAY_COLS+c)*3+1]=0;
		disp_image[(r*DISPLAY_COLS+c)*3+2]=0;
		}
	  else
		{
	    disp_image[(r*DISPLAY_COLS+c)*3+0]=Image[(r2*COLS+c2)*3+2];
	    disp_image[(r*DISPLAY_COLS+c)*3+1]=Image[(r2*COLS+c2)*3+1];
	    disp_image[(r*DISPLAY_COLS+c)*3+2]=Image[(r2*COLS+c2)*3+0];
		}
	  }
	}
  PaintImage();
  }
}



int DownloadSide;	/* 0 or 1 meaning up or side image currently being downloaded */

BOOL pascal  DownloadProgress(DCProgressStatus		Status,
								short				PercentComplete,
								DCProgressType		Type,
								long				RefCon)

{
HDC		hDC;
char	report[80];
RECT	outline;
HBRUSH	DrawBrush;

hDC=GetDC(MainWnd);
SetBkMode(hDC,OPAQUE);
SetBkColor(hDC,RGB(255,255,255));
if (PercentComplete == 0)
  {
  DrawBrush=CreateSolidBrush(RGB(255,255,255));
  outline.left=0; outline.right=385;
  outline.top=0; outline.bottom=25;
  FillRect(hDC,&outline,DrawBrush);
  DeleteObject(DrawBrush);
  }
outline.top=26;
outline.bottom=154;
if (DownloadSide == 0)
  { outline.left=16; outline.right=184; }
else
  { outline.left=206; outline.right=374; }
if (PercentComplete%5 == 0)
  {
  if ((Type == DCImageProcess  &&  PercentComplete%20 == 0)  ||
	  (Type == DCTransferImage  &&  PercentComplete%10 == 0))
    DrawBrush=CreateSolidBrush(RGB(0,0,0));
  else
    DrawBrush=CreateSolidBrush(RGB(255,255,255));
  FrameRect(hDC,&outline,DrawBrush);
  DeleteObject(DrawBrush);
  }
if (Type == DCTransferImage)
  sprintf(report,"Downloading   %3d%%",PercentComplete);
else /* Type == DCImageProcess */
  sprintf(report,"Decompressing %3d%%",PercentComplete);
TextOut(hDC,0,0,report,strlen(report));
ReleaseDC(MainWnd,hDC);
return(TRUE);
}



			/*
			** Opens the driver and camera (static variables kept here)
			** and downloads the first two icons.
			** Returns 1 (success) or 0 (failure).
			*/

int ConnectToCamera()

{
SHORT				Version=DCSDKVersion;
DCPortNum			PortNum;
DCStatus			GenericStatus;

NumOfPicts=0;
if (CameraOpen == 0)
  {
  memset(&Driver,0,sizeof(DCDriver));
  if (DCOpenDriver(&Version,&Driver) != DC_NoErr)
    {
    MessageBox(NULL,"Unable to open camera driver.","Error",MB_OK | MB_APPLMODAL);
    UpPictNum=SidePictNum=0;
    return(0);
    }
  CameraOpen=1;
  Camera.Driver=&Driver;
  Camera.CamType=DC120;
  Camera.BitRate=DCBitRate115200;
  for (PortNum=DCPortNum1; PortNum<=DCPortNum4; PortNum++)
    {
    Camera.PortNum=PortNum;
    if (DCOpenCamera(&Camera) == DC_NoErr)
	  break;
    }
  if (PortNum > DCPortNum4)
    {
    MessageBox(NULL,"Unable to open camera.  Power on?  Cable connected?","Error",MB_OK | MB_APPLMODAL);
    UpPictNum=SidePictNum=0;
    return(0);
    }
  CameraOpen=2;
  }
if (DCGetStatus(&Camera,&GenericStatus,(VOIDPTR)NULL) != DC_NoErr)
  {
  MessageBox(NULL,"Unable to determine picture taken.","Error",MB_OK | MB_APPLMODAL);
  UpPictNum=SidePictNum=0;
  return(0);
  }
NumOfPicts=GenericStatus.MemPictTaken;
CamOrCard=DCCameraMemory;
if (NumOfPicts == 0)
  {
  NumOfPicts=GenericStatus.CardPictTaken;
  CamOrCard=DCPCCard;
  }
if (NumOfPicts < 1)
  {
  MessageBox(NULL,"No pictures stored in camera.","Error",MB_OK | MB_APPLMODAL);
  UpPictNum=SidePictNum=0;
  return(0);
  }
if (UpPictNum > NumOfPicts)
  UpPictNum=0;
if (SidePictNum > NumOfPicts)
  SidePictNum=0;
MakeDisplayImage(NULL,0,0,0);
GetIconFromCamera(UpPictNum,1);
GetIconFromCamera(SidePictNum,2);
return(1);
}



		/*
		** Grabs an icon image from the camera and puts
		** it in the left or right subwindow
		*/

void GetIconFromCamera(int	NewPictNum,	// 1...NumOfPicts from camera
										// 0 make empty (white) image
										// -1 increment and get
										// -2 decrement and get
										// -3 just redraw
					   int	Location)	// 1 => left, 2 => right

{
unsigned char	*ReorderImage;
int				r,c;
DCPictInfo		NewPictInfo;
DC120PictInfo	NewPictFullInfo;

if (NewPictNum < 0)
  {
  if (Location == 1)
	{
	if (NewPictNum == -1)
	  UpPictNum++;
	else if (NewPictNum == -2)
	  UpPictNum--;
	if (UpPictNum > NumOfPicts)
	  UpPictNum=0;
	if (UpPictNum < 0)
	  UpPictNum=NumOfPicts;
	NewPictNum=UpPictNum;
    }
  else
	{
	if (NewPictNum == -1)
	  SidePictNum++;
	else if (NewPictNum == -2)
	  SidePictNum--;
	if (SidePictNum > NumOfPicts)
	  SidePictNum=0;
	if (SidePictNum < 0)
	  SidePictNum=NumOfPicts;
	NewPictNum=SidePictNum;
	}
  }
NewPictInfo.ThumbPtr=malloc(THUMB_WIDTH*THUMB_HEIGHT*3);
if (NewPictNum > 0)
  {
  DCGetCameraPictInfo(&Camera,CamOrCard,DCNoAlbum,(short)NewPictNum,
			TRUE,&NewPictInfo,&NewPictFullInfo);
  if (Location == 1)
	sprintf(up_filename,"%s.jpg",NewPictFullInfo.ImageName);
  else
	sprintf(side_filename,"%s.jpg",NewPictFullInfo.ImageName);
  }
else
  {
  for (r=0; r<THUMB_WIDTH*THUMB_HEIGHT*3; r++)
	NewPictInfo.ThumbPtr[r]=(char)255;
  if (Location == 1)
	strcpy(up_filename,"");
  else
	strcpy(side_filename,"");
  }
ReorderImage=malloc(THUMB_WIDTH*THUMB_HEIGHT*3);
for (r=0; r<THUMB_HEIGHT; r++)
  for (c=0; c<THUMB_WIDTH; c++)
    {
    ReorderImage[(r*THUMB_WIDTH+c)*3+2]=NewPictInfo.ThumbPtr[((THUMB_HEIGHT-1-r)*THUMB_WIDTH+c)*3+0];
    ReorderImage[(r*THUMB_WIDTH+c)*3+1]=NewPictInfo.ThumbPtr[((THUMB_HEIGHT-1-r)*THUMB_WIDTH+c)*3+1];
    ReorderImage[(r*THUMB_WIDTH+c)*3+0]=NewPictInfo.ThumbPtr[((THUMB_HEIGHT-1-r)*THUMB_WIDTH+c)*3+2];
    }
MakeDisplayImage(ReorderImage,THUMB_HEIGHT,THUMB_WIDTH,Location);
free(ReorderImage);
free(NewPictInfo.ThumbPtr);
}




int DownloadImageFromCamera(int				Location,
							unsigned char	**new_image,
							int				*NEW_ROWS,
							int				*NEW_COLS,
							char			*new_filename)

{
int				r,c,NewPictNum;
DCPictInfo		NewPictInfo;
DC120PictInfo	NewPictFullInfo;
DCImageIOCB		Input,Output;
DCProgressCB	Progress;

if (Location == 1)
  {
  NewPictNum=UpPictNum;
  DownloadSide=0;
  }
else
  {
  NewPictNum=SidePictNum;
  DownloadSide=1;
  }
if (NewPictNum == 0)
  return(0);
DCGetCameraPictInfo(&Camera,CamOrCard,DCNoAlbum,(short)NewPictNum,
			FALSE,&NewPictInfo,&NewPictFullInfo);
*NEW_ROWS=NewPictInfo.PictHeight;
*NEW_COLS=NewPictInfo.PictWidth;
if ((*new_image=(unsigned char *)calloc((*NEW_ROWS)*(*NEW_COLS)*3,1)) == NULL)
  {
  MessageBox(MainWnd,"Unable to allocate memory","DownloadFromCamera()",MB_APPLMODAL | MB_OK);
  return(0);
  }
Input.BufferSize=NewPictInfo.PictMinBufIn;
Input.Buffer=malloc(Input.BufferSize);
Input.IOFunc=NULL;
Input.RefCon=0L;
Output.BufferSize=(*NEW_ROWS)*(*NEW_COLS)*3;
if ((Output.Buffer=calloc(Output.BufferSize,1)) == NULL)
  {
  MessageBox(MainWnd,"Unable to allocate download memory","Download()",MB_APPLMODAL | MB_OK);
  return(0);
  }
Output.IOFunc=NULL;
Output.RefCon=0L;
Progress.ProgFunc=(DCProgressProc)DownloadProgress;
if (DCGetCameraPicture(&Camera,CamOrCard,DCNoAlbum,
					&NewPictInfo,&Input,&Output,&Progress) != DC_NoErr)
  {
  MessageBox(NULL,"Error downloading image","Download()",MB_APPLMODAL | MB_OK);
  free(*new_image);
  *new_image=NULL;
  (*NEW_ROWS)=(*NEW_COLS)=0;
  return(0);
  }
else
  {
  sprintf(new_filename,"%s.jpg",NewPictFullInfo.ImageName);
  for (r=0; r<*NEW_ROWS; r++)
    for (c=0; c<*NEW_COLS; c++)
	  {
	  (*new_image)[(r*(*NEW_COLS)+c)*3+0]=Output.Buffer[(((*NEW_ROWS)-1-r)*(*NEW_COLS)+c)*3+2];
	  (*new_image)[(r*(*NEW_COLS)+c)*3+1]=Output.Buffer[(((*NEW_ROWS)-1-r)*(*NEW_COLS)+c)*3+1];
	  (*new_image)[(r*(*NEW_COLS)+c)*3+2]=Output.Buffer[(((*NEW_ROWS)-1-r)*(*NEW_COLS)+c)*3+0];
	  }
  }
free(Input.Buffer);
free(Output.Buffer);
return(1);
}


void CloseCamera()

{
if (CameraOpen >= 2)
  if (DCCloseCamera(&Camera) != DC_NoErr)
    MessageBox(NULL,"Unable to close camera.","Error",MB_OK | MB_APPLMODAL);
if (CameraOpen >= 1)
  if (DCCloseDriver(&Driver) != DC_NoErr)
    MessageBox(NULL,"Unable to close camera driver.","Error",MB_OK | MB_APPLMODAL);
CameraOpen=0;
}

