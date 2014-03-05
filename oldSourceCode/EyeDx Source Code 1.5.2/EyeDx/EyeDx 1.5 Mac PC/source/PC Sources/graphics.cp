
#include <stdio.h>
#include <windows.h>
#include <wingdi.h>
#include "resource.h"
#include "globals.h"


int DrawScaledImage(HWND Window,
				unsigned char *Image,
				int	ROWS,int COLS,
				int BYTES,
				int x,int y,
				int WindowROWS,int WindowCOLS)

{
unsigned char		*disp_image;
BITMAPINFO			bm_info;
BITMAPINFOHEADER	bm_info_header;
HDC					hDC;
RECT				main_rect;
int					r2,c2,r,c;

hDC=GetDC(hWnd);
GetClientRect(hWnd,&main_rect);
WindowCOLS=main_rect.right-main_rect.left;
WindowROWS=main_rect.bottom-main_rect.top;
disp_image=(unsigned char *)calloc(1,WindowROWS*WindowCOLS*3);
for (r=0; r<WindowROWS; r++)
  for (c=0; c<WindowCOLS; c++)
	{
	r2=(int)((double)r/(double)WindowROWS*(double)ROWS);
	c2=(int)((double)c/(double)WindowCOLS*(double)COLS);
	if (BYTES == 3)
	  {
	  disp_image[(r*WindowCOLS+c)*3+0]=Image[(r2*COLS+c2)*3+0];
	  disp_image[(r*WindowCOLS+c)*3+1]=Image[(r2*COLS+c2)*3+1];
	  disp_image[(r*WindowCOLS+c)*3+2]=Image[(r2*COLS+c2)*3+2];
	  }
	else
	  {
	  disp_image[(r*WindowCOLS+c)*3+0]=Image[r2*COLS+c2];
	  disp_image[(r*WindowCOLS+c)*3+1]=Image[r2*COLS+c2];
	  disp_image[(r*WindowCOLS+c)*3+2]=Image[r2*COLS+c2];
	  }
	}
bm_info_header.biSize=sizeof(BITMAPINFOHEADER); 
bm_info_header.biWidth=WindowCOLS;
bm_info_header.biHeight=-WindowROWS; 
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
SetDIBitsToDevice(hDC,x,y,WindowCOLS,WindowROWS,0,0,
				  0 /* first scan line */,
				  WindowROWS /* number of scan lines */,
				  disp_image,&bm_info,DIB_RGB_COLORS);
// StretchDIBits(hDC,0,0,WindowCOLS,WindowROWS,0,0,COLS,ROWS,
//			image,&bm_info,DIB_RGB_COLORS,SRCCOPY | COLORONCOLOR);
free(disp_image);
}