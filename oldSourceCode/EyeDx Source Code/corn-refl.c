
	/*******************************************************************
	** Routines to find possible corneal reflexes
	*******************************************************************/

#include <stdio.h>
#include <math.h>
#include <windows.h>
#include "globals.h"

#define SAVE_THRESH_IMAGE	0   /* flags to save intermediate results */
#define SAVE_BRIGHTS_IMAGE	0	/* for debugging purposes only */


int FindBrightSpots(unsigned char	*raw,						/* input */
					int				ROWS,int COLS,				/* input */
					unsigned char	*threshimage,				/* output */
					int				*total_brights,int *brights)/* output */

{
unsigned char	*saveimage;
int				r,c,r2,c2;
int				size,center_row,center_col;
// FILE			*fpt;

	/*******************************************************************
	** Threshold raw image to find candidate bright pixels
	*******************************************************************/

for (r=0; r<ROWS; r++)
  for (c=0; c<COLS; c++)
    {		/* raw image in BGR0,BGR1,BGR2,BGR3,... order */
    if (raw[(r*COLS+c)*3+0] > BrightThresh  &&
		raw[(r*COLS+c)*3+1] > BrightThresh  &&
		raw[(r*COLS+c)*3+2] > BrightThresh)
	  threshimage[r*COLS+c]=BRIGHT;
    else
	  threshimage[r*COLS+c]=OTHER;
    }

if (SAVE_THRESH_IMAGE)
  {
  saveimage=(unsigned char *)calloc(1,ROWS*COLS*3);
  for (r=0; r<ROWS*COLS; r++)
	saveimage[r*3+0]=saveimage[r*3+1]=saveimage[r*3+2]=threshimage[r];
  SaveImage("thresh.jpg",saveimage,ROWS,COLS,1);
  free(saveimage);
/*
  fpt=fopen("thresh.ppm","wb");
  fprintf(fpt,"P5 %d %d 255\n",COLS,ROWS);
  fwrite(threshimage,1,ROWS*COLS,fpt);
  fclose(fpt);
*/
  }


	/*******************************************************************
	** find `pinpricks' of white -- possible corneal reflexes
	*******************************************************************/

printf("Finding bright spots..."); fflush(stdout);
*total_brights=0;
for (r=25; r<ROWS-25; r++)
  for (c=25; c<COLS-25; c++)
    {
    if (threshimage[r*COLS+c] != BRIGHT)
      continue;
    size=RegionFill(threshimage,ROWS,COLS,r,c,BRIGHT,BRIGHT_CHECKING);
    if (size >= MinCRArea  &&  size <= MaxCRArea)
      {
      if (*total_brights >= MAX_BRIGHTS)
        {
        MessageBox(MainWnd,"MAX_BRIGHTS exceeded in FindBrightSpots()","Error",MB_OK | MB_APPLMODAL);
        return(0);
        }
      center_row=center_col=0;
      for (r2=r-size; r2<r+size; r2++)
	for (c2=c-size; c2<c+size; c2++)
	  if (r2 >= 0  &&  r2 < ROWS  &&  c2 >= 0  &&  c2 < COLS  &&
		threshimage[r2*COLS+c2] == BRIGHT_CHECKING)
	    {
	    center_row+=r2;
	    center_col+=c2;
	    }
      brights[*total_brights]=(center_row/size)*COLS+(center_col/size);
      (*total_brights)++;
      RegionFill(threshimage,ROWS,COLS,r,c,BRIGHT_CHECKING,POSS_REFLEX);
      }
    else
      RegionFill(threshimage,ROWS,COLS,r,c,BRIGHT_CHECKING,BRIGHT_OTHER);
    }

if (SAVE_BRIGHTS_IMAGE)
  {
	for (r=0; r<ROWS*COLS; r++)
		if (threshimage[r] == BRIGHT_OTHER)
			threshimage[r]=175;
		else if (threshimage[r] != POSS_REFLEX)
		{ threshimage[r]=(raw[r*3+0]+raw[r*3+1]+raw[r*3+2])/8; }
  saveimage=(unsigned char *)calloc(1,ROWS*COLS*3);
  for (r=0; r<ROWS*COLS; r++)
	saveimage[r*3+0]=saveimage[r*3+1]=saveimage[r*3+2]=threshimage[r];
  SaveImage("brights.jpg",saveimage,ROWS,COLS,1);
  free(saveimage);
/*
  fpt=fopen("brights.ppm","wb");
  fprintf(fpt,"P5 %d %d 255\n",COLS,ROWS);
  fwrite(threshimage,1,ROWS*COLS,fpt);
  fclose(fpt);
*/
  }
return(1);
}





	/*******************************************************************
	** A queue-based paint-fill routine.
	*******************************************************************/

#define MAX_QUEUE 10000

int RegionFill(unsigned char	*image,
				int	ROWS,int COLS,int r,int c,
				int	paint_over_label,int new_paint_label)

{
int	queue[MAX_QUEUE],qh,qt,count;

if (image[r*COLS+c] != paint_over_label)
  return(0);
image[r*COLS+c]=new_paint_label;
queue[0]=r*COLS+c;
qh=1;
qt=0;
count=1;
while (qt != qh)
  {
  if (queue[qt]/COLS > 0  &&  image[queue[qt]-COLS] == paint_over_label)
    {
    image[queue[qt]-COLS]=new_paint_label;
    count++;
    queue[qh]=queue[qt]-COLS;
    qh=(qh+1)%MAX_QUEUE;
    if (qh == qt)
      {
	  MessageBox(NULL,"MAX_QUEUE exceeded!","RegionFill()",MB_APPLMODAL | MB_OK);
      exit(0);
      }
    }
  if (queue[qt]/COLS < ROWS-1  &&  image[queue[qt]+COLS] == paint_over_label)
    {
    image[queue[qt]+COLS]=new_paint_label;
    count++;
    queue[qh]=queue[qt]+COLS;
    qh=(qh+1)%MAX_QUEUE;
    if (qh == qt)
      {
	  MessageBox(NULL,"MAX_QUEUE exceeded!","RegionFill()",MB_APPLMODAL | MB_OK);
      exit(0);
      }
    }
  if (queue[qt]%COLS > 0  &&  image[queue[qt]-1] == paint_over_label)
    {
    image[queue[qt]-1]=new_paint_label;
    count++;
    queue[qh]=queue[qt]-1;
    qh=(qh+1)%MAX_QUEUE;
    if (qh == qt)
      {
	  MessageBox(NULL,"MAX_QUEUE exceeded!","RegionFill()",MB_APPLMODAL | MB_OK);
      exit(0);
      }
    }
  if (queue[qt]%COLS < COLS-1  &&  image[queue[qt]+1] == paint_over_label)
    {
    image[queue[qt]+1]=new_paint_label;
    count++;
    queue[qh]=queue[qt]+1;
    qh=(qh+1)%MAX_QUEUE;
    if (qh == qt)
      {
	  MessageBox(NULL,"MAX_QUEUE exceeded!","RegionFill()",MB_APPLMODAL | MB_OK);
      exit(0);
      }
    }
  qt=(qt+1)%MAX_QUEUE;
  }
return(count);
}





