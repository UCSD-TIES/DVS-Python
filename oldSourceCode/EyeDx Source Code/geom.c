
	/*******************************************************************
	** Routines in this file convert geometric shapes (lines and circles)
	** into sets of pixel coordinates.
	*******************************************************************/

#include <stdio.h>
#include <math.h>
#include <windows.h>
#include "globals.h"

	/*******************************************************************
	** Given two endpoints of a line segment (integers), this routine
	** computes the indices of the integer points of the segment.
	*******************************************************************/

void MakeLineIndices(int x1,int y1,int x2,int y2,	/* inputs -- endpoints of line segment */
					 int ROWS,int COLS,				/* inputs -- clipping width & height */
					 int *indices,					/* output -- indices of pixels on line */
					 int *tp)						/* output -- total pixels in line segment */

{
float   x,y;
int     temp,swap,i;

if (x1 > x2)
  { temp=x1; x1=x2; x2=temp; temp=y1; y1=y2; y2=temp; swap=1; }
else
  swap=0;
x=(float)x1; y=(float)y1;
*tp=0;
do
  {
  if ((int)x >= 0  &&  (int)x < COLS  &&  (int)y >= 0  &&  (int)y < ROWS)
    {
    indices[*tp]=(int)y*COLS+(int)x;
    (*tp)++;
    }
  if (x1 == x2  &&  y1 == y2)
    break;
  if (abs(x2-x1) > abs(y2-y1))
    {
    x+=1.0;
    y+=(float)(y2-y1)/(float)(x2-x1);
    }
  else
    {
    if (y2 > y1)
      y+=1.0;
    else
      y-=1.0;
    x+=(float)(x2-x1)/(float)fabs((double)(y2-y1));
    }
  }
while (fabs((double)x-(double)x2) > 0.5  ||  fabs((double)y-(double)y2) > 0.5);
if (swap)
  for (i=0; i<(*tp)/2; i++)
    { temp=indices[i]; indices[i]=indices[(*tp)-1-i]; indices[(*tp)-1-i]=temp; }
}








	/*******************************************************************
	** Given the center and radius of a circle (real #s), this routine
	** computes the indices of the integer points on the circle.
	*******************************************************************/

void MakeCircleIndices(double cx,double cy,double ra, /* inputs -- center and radius of circle */
					   int ROWS,int COLS,				/* inputs -- clipping width & height */
					   int *indices,				/* output -- indices of points on circle */
					   int *tp)					/* output -- total points in circle */

{
double	x,y;
int	pass;	/* 1 => building top half of circle; 2 => bottom half */

if (ra < 1.0)
  {
  *tp=0;
  return;
  }
x=0.0-ra; y=0.0;
pass=1;			/* build top half of circle left->right */
*tp=0;
while (pass < 3)
  {
  if ((int)(cx+x) >= 0  &&  (int)(cx+x) < COLS  &&
	(int)(cy-y) >= 0  &&  (int)(cy-y) < ROWS)
    {
    indices[*tp]=(int)(cy-y)*COLS+(int)(cx+x);
    (*tp)++;
    }
  if (atan2(fabs(y),fabs(x)) > M_PI/4.0)
    {
    if (pass == 1)
      {
      x+=1.0;
      y=sqrt(ra*ra-x*x);
      }
    else
      {
      x-=1.0;
      y=-sqrt(ra*ra-x*x);
      }
    }
  else if (x < 0.0)
    {
    y+=1.0;
    x=-sqrt(ra*ra-y*y);
    }
  else
    {
    y-=1.0;
    x=sqrt(ra*ra-y*y);
    }
  if (pass == 1  &&  y <= 0.0)
    pass=2;		/*build bottom half of circle right->left */
  else if (pass == 2  &&  y >= 0.0)
    pass=3;
  }
(*tp)--;	/* last point is duplicate of first point */
}

