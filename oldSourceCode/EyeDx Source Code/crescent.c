
#include <stdio.h>
#include <math.h>
#include <windows.h>
#include "globals.h"


void ClassifyPupilInterior(unsigned char	*raw,		/* image data, RGB order */
							unsigned char	*threshimage,	/* used to mark CR and ARR */
							unsigned char	*dispimage,	/* for displaying what's going on */
							int		ROWS,int COLS,
							double	pupil_circle[4],	/* pupil-iris border */
							int		corneal_point,		/* input: a point inside corneal reflex */
							int		*corneal_reflex_indices, /* output: indices of CR */
							int		*total_cr,			/* output: count of pixels in CR */
							int		*abnormal_red_reflex_indices,	/* output: indices of ARR */
							int		*total_arr,			/* output: count of ARR */
							int		red_reflex_avg[3],	/* output: avg red reflex luminensce */
							int		*red_reflex_class,	/* output: classif. of blob */
							int		*red_reflex_col,	/* output: X-centroid of blob */
							int		*red_reflex_row)	/* output: Y-centroid of blob */

{
int		EYE_ROWS,EYE_COLS,r,c,r2,c2,pass,x,y,center_row,center_col;
int		AvgShade[3],DevShade[3],count,diff,size,touching_count;
int		perim_count,perim_pixel,r3,c3;
double	area;
int		*circle_points,total_circle_points,i,Zoom;
//char	text[100];

if (DisplayGraphics == 1)
  {
  if (pupil_circle[3] >= 1.0)
	Zoom=(int)(pupil_circle[3]*3.0);
  else if (pupil_circle[2] >= 1.0)
	Zoom=(int)(pupil_circle[2]*3.0);
  else
	Zoom=MaxIrisRad*2;
  ZoomDisplay(dispimage,ROWS,COLS,corneal_point/COLS,corneal_point%COLS,Zoom,Zoom,ZoomSteps);
  circle_points=(int *)calloc(MaxIrisRad*8,sizeof(int));
  Sleep(FramePause/4);
  if (pupil_circle[2] >= 0.0)
    {
	MakeCircleIndices(pupil_circle[0],pupil_circle[1],pupil_circle[2],
						ROWS,COLS,circle_points,&total_circle_points);
	for (i=0; i<total_circle_points; i++)
	  dispimage[circle_points[i]*3+1]=255;
    }
  if (pupil_circle[3] >= 0.0)
    {
	MakeCircleIndices(pupil_circle[0],pupil_circle[1],pupil_circle[3],
						ROWS,COLS,circle_points,&total_circle_points);
	for (i=0; i<total_circle_points; i++)
	  dispimage[circle_points[i]*3+1]=dispimage[circle_points[i]*3+0]=255;
    }
  free(circle_points);
  ZoomDisplay(dispimage,ROWS,COLS,corneal_point/COLS,corneal_point%COLS,Zoom,Zoom,0);
  Sleep(FramePause/4);
  }

	/*****************************************************************
	** threshimage keeps track of pixel labels.  First, label the
	** corneal reflex with a distinctive label, so the CR pixels will
	** be ignored in further processing.
	*****************************************************************/

size=RegionFill(threshimage,ROWS,COLS,corneal_point/COLS,corneal_point%COLS,
		POSS_REFLEX,CORN_REFLEX);

	/*****************************************************************
	** if there is no red circle, then fill cr_indices array and exit
	*****************************************************************/

(*total_arr)=(*total_cr)=0;
(*red_reflex_col)=(*red_reflex_row)=0;
red_reflex_avg[0]=red_reflex_avg[1]=red_reflex_avg[2]=0;
if (pupil_circle[2] <= 0.0)
  {
  for (r=corneal_point/COLS-size; r<corneal_point/COLS+size; r++)
    for (c=corneal_point%COLS-size; c<corneal_point%COLS+size; c++)
      if (r >= 0  &&  r < ROWS  &&  c >= 0  &&  c < COLS  &&
				threshimage[r*COLS+c] == CORN_REFLEX)
        {
        corneal_reflex_indices[*total_cr]=r*COLS+c;
        (*total_cr)++;
		if (DisplayGraphics == 1)
		  {
          dispimage[(r*COLS+c)*3+0]/=8;
          dispimage[(r*COLS+c)*3+1]/=8;
          dispimage[(r*COLS+c)*3+2]=255;
		  }
        }
  if (DisplayGraphics == 1)
    {
    ZoomDisplay(dispimage,ROWS,COLS,corneal_point/COLS,corneal_point%COLS,Zoom,Zoom,0);
    Sleep(FramePause/4);
	}
  return;
  }
(*red_reflex_class)=NORMAL;

	/*****************************************************************
	** Four passes through the image data:
	** 	pass 0: find the average intensity inside the pupil
	**	pass 1: find the stddev intensity inside the pupil
	** 	pass 2: label abnormal pixels inside the pupil
	**	pass 3: paint-fill abnormal areas and classify
	*****************************************************************/

EYE_ROWS=EYE_COLS=(int)(pupil_circle[2]*2.0+2.0);	/* inside of pupil */
y=(int)pupil_circle[1]-EYE_ROWS/2;	/* local image bounds to check */
x=(int)pupil_circle[0]-EYE_COLS/2;

AvgShade[0]=AvgShade[1]=AvgShade[2]=count=0;
DevShade[0]=DevShade[1]=DevShade[2]=0;
for (pass=0; pass<4; pass++)
  {
  for (r=y; r<=y+EYE_ROWS; r++)
    for (c=x; c<=x+EYE_COLS; c++)
      {
      if (r < 0  ||  r >= ROWS  ||  c < 0  ||  c >= COLS)
        continue;	/* outside image bounds */
      if (sqrt(SQR((double)r-pupil_circle[1])+SQR((double)c-pupil_circle[0])) > pupil_circle[2])
		{
		threshimage[r*COLS+c]=OTHER;	/* so paint-fill stops at circle */
		continue;	/* outside pupil circle */
		}
      if (threshimage[r*COLS+c] == CORN_REFLEX)
        {
        if (pass == 0)
          {
          corneal_reflex_indices[*total_cr]=r*COLS+c;
          (*total_cr)++;
          }
        continue;	/* don't want to include CR */
        }
      for (r2=-2; r2<=2; r2++)	/* search for 2-deep border of CR */
        {
        for (c2=-2; c2<=2; c2++)
          if (threshimage[(r+r2)*COLS+c+c2] == CORN_REFLEX)
		    break;
        if (c2 <=2) break;
		}
      if (r2 <= 2)
		{
		threshimage[r*COLS+c]=OTHER;
        continue;	/* don't want to include area just around CR */
		}
      if (pass == 0)
        {
		AvgShade[0]+=raw[(r*COLS+c)*3+0];	/* red */
		AvgShade[1]+=raw[(r*COLS+c)*3+1];	/* green */
		AvgShade[2]+=raw[(r*COLS+c)*3+2];	/* blue */
		count++;
        }
      else if (pass == 1)
        {
		DevShade[0]+=SQR(raw[(r*COLS+c)*3+0]-AvgShade[0]);
		DevShade[1]+=SQR(raw[(r*COLS+c)*3+1]-AvgShade[1]);
		DevShade[2]+=SQR(raw[(r*COLS+c)*3+2]-AvgShade[2]);
        }
      else if (pass == 2)
        {
        diff=(raw[(r*COLS+c)*3+0]-AvgShade[0])+
		(raw[(r*COLS+c)*3+1]-AvgShade[1])+
		(raw[(r*COLS+c)*3+2]-AvgShade[2]);
		if (diff > 70  &&  (AvgShade[0] > 200  ||
						raw[(r*COLS+c)*3+0]-AvgShade[0] > 30))
		  threshimage[r*COLS+c]=ABNORMAL;
		else
		  threshimage[r*COLS+c]=OTHER;
        }
      else	/* pass == 3 */
		{
        if (threshimage[r*COLS+c] == ABNORMAL)
          size=RegionFill(threshimage,ROWS,COLS,r,c,ABNORMAL,BRIGHT_CHECKING);
        else
          continue;
        area=(double)size/(M_PI*SQR(pupil_circle[2]));
//sprintf(text,"ARR size %d area %lf (limits %lf %lf)",size,area,MIN_2R_AREA,MAX_2R_AREA);
//MessageBox(NULL,text,"ARR analysis",MB_OK | MB_APPLMODAL);
        if (area < MIN_2R_AREA  ||  area > MAX_2R_AREA)
          {
          size=RegionFill(threshimage,ROWS,COLS,r,c,BRIGHT_CHECKING,OTHER);
          continue;
          }
                /* big enough area -- find centroid and circle-border count */
        center_row=center_col=touching_count=perim_count=0;
        for (r2=r-size; r2<r+size; r2++)
          for (c2=c-size; c2<c+size; c2++)
            if (r2 >= 0  &&  r2 < ROWS  &&  c2 >= 0  &&  c2 < COLS  &&
					threshimage[r2*COLS+c2] == BRIGHT_CHECKING)
              {
              center_row+=r2;
              center_col+=c2;
		      perim_pixel=0;	/* is pixel on perimter of ARR-blob? */
		      for (r3=r2-1; r3<=r2+1; r3++)
				for (c3=c2-1; c3<=c2+1; c3++)
				  {
				  if (r3 >= 0  &&  r3 < ROWS  &&  c3 >= 0  &&  c3 < COLS  &&
						threshimage[r3*COLS+c3] != BRIGHT_CHECKING)
				    perim_pixel=1;
				  }
		      if (perim_pixel == 1)
		        {
		        perim_count++;
                if (fabs(pupil_circle[2]-sqrt(SQR((double)r2-pupil_circle[1])+
						SQR((double)c2-pupil_circle[0])) ) <= 2.5)
		          touching_count++;
                }
		      }
		*red_reflex_col=(int)((double)center_col/(double)size);
		*red_reflex_row=(int)((double)center_row/(double)size);
        if (sqrt(SQR((double)(*red_reflex_row)-pupil_circle[1])+
                 SQR((double)(*red_reflex_col)-pupil_circle[0]))
                < pupil_circle[2])	/* centroid inside pupil */
          {
		  if ((double)touching_count/(double)perim_count > MIN_CRESC)
		    *red_reflex_class=CRESCENT;
          else
		    *red_reflex_class=OTHER_BLOB;
          for (r2=r-size; r2<r+size; r2++)
            for (c2=c-size; c2<c+size; c2++)
              if (r2 >= 0  &&  r2 < ROWS  &&  c2 >= 0  &&  c2 < COLS  &&
                        threshimage[r2*COLS+c2] == BRIGHT_CHECKING)
                {
                abnormal_red_reflex_indices[*total_arr]=r2*COLS+c2;
                (*total_arr)++;
                }
          }
        size=RegionFill(threshimage,ROWS,COLS,r,c,BRIGHT_CHECKING,OTHER);
		}
      }
  if (pass == 0)
    {
    red_reflex_avg[0]=AvgShade[0]=AvgShade[0]/count;
    red_reflex_avg[1]=AvgShade[1]=AvgShade[1]/count;
    red_reflex_avg[2]=AvgShade[2]=AvgShade[2]/count;
//sprintf(text,"RR avg inten %d %d %d",AvgShade[0],AvgShade[1],AvgShade[2]);
//MessageBox(NULL,text,"ARR analysis",MB_OK | MB_APPLMODAL);
    }
  else if (pass == 1)
    {
    DevShade[0]=(int)sqrt((double)DevShade[0]/(double)count);
    DevShade[1]=(int)sqrt((double)DevShade[1]/(double)count);
    DevShade[2]=(int)sqrt((double)DevShade[2]/(double)count);
    }
  if (pass == 0  &&  DisplayGraphics == 1)
    {
    for (i=0; i<(*total_cr); i++)
	  {
      dispimage[corneal_reflex_indices[i]*3+0]/=8;
      dispimage[corneal_reflex_indices[i]*3+1]/=8;
      dispimage[corneal_reflex_indices[i]*3+2]=255;
	  }
    ZoomDisplay(dispimage,ROWS,COLS,corneal_point/COLS,corneal_point%COLS,Zoom,Zoom,0);
    Sleep(FramePause/4);
    }
  }

if (DisplayGraphics == 1)
  {
  for (i=0; i<(*total_arr); i++)
	{
    dispimage[abnormal_red_reflex_indices[i]*3+2]=255;
	if ((*red_reflex_class) == CRESCENT)
	  {
	  dispimage[abnormal_red_reflex_indices[i]*3+1]=255;
	  dispimage[abnormal_red_reflex_indices[i]*3+0]/=8;
	  }
	else
	  {
	  dispimage[abnormal_red_reflex_indices[i]*3+1]/=8;
	  dispimage[abnormal_red_reflex_indices[i]*3+0]=175;
	  }
	}
  ZoomDisplay(dispimage,ROWS,COLS,corneal_point/COLS,corneal_point%COLS,Zoom,Zoom,0);
  Sleep(FramePause);
  }
}



void ClassifyPupilAlignment(double	lefteye_circles[4],	/* input:  left eye model */
							int	*lefteye_cr_indices,	/* input:  indices (y*COLS+x) of left CR */
							int	total_left_cr,			/* input:  count of left CR pixels */
							double	righteye_circles[4],/* input:  right eye model */
							int	*righteye_cr_indices,	/* input:  indices (y*COLS+x) of right CR */
							int	total_right_cr,			/* input:  count of right CR pixels */
							int	COLS,					/* input:  used to decode indices arrays */
							int	a,					/* input:  image-ori (0 up, 1 left, 2 right) */
							int	*strabismus)		/* output:  classif. of strabismus (0-5) */

{
double	left_cr_col,left_cr_row,right_cr_col,right_cr_row;
int	i,left_align,right_align;
double	pup_to_pup_dist,cr_to_cr_dist;

	/*****************************************************************
	** Compute corneal reflex centroids for both eyes, in xy coord sys
	*****************************************************************/

left_cr_col=left_cr_row=0.0;
for (i=0; i<total_left_cr; i++)
  {
  left_cr_col+=(double)(lefteye_cr_indices[i]%COLS);
  left_cr_row+=(double)(lefteye_cr_indices[i]/COLS);
  }
left_cr_col/=(double)total_left_cr;
left_cr_row/=(double)total_left_cr;
right_cr_col=right_cr_row=0.0;
for (i=0; i<total_right_cr; i++)
  {
  right_cr_col+=(double)(righteye_cr_indices[i]%COLS);
  right_cr_row+=(double)(righteye_cr_indices[i]/COLS);
  }
right_cr_col/=(double)total_right_cr;
right_cr_row/=(double)total_right_cr;

	/*****************************************************************
	** Compute alignments of CRs to eye models
	*****************************************************************/

pup_to_pup_dist=sqrt(SQR(lefteye_circles[0]-righteye_circles[0])+
	SQR(lefteye_circles[1]-righteye_circles[1]));
cr_to_cr_dist=sqrt(SQR(left_cr_col-right_cr_col)+
	SQR(left_cr_row-right_cr_row));
if (sqrt(SQR(lefteye_circles[0]-left_cr_col)+
	SQR(lefteye_circles[1]-left_cr_row))
		>= lefteye_circles[3]*MAX_CR_PUP_DIST)
  {			/* left eye not aligned */
  if (fabs(lefteye_circles[0]-left_cr_col) >
	fabs(lefteye_circles[1]-left_cr_row))
    left_align=1;	/* worse horizontal misalign then vertical */
  else
    left_align=2;	/* worse vertical misalign then horizontal */
  }
else
  left_align=0;		/* left eye ok */
if (sqrt(SQR(righteye_circles[0]-right_cr_col)+
	SQR(righteye_circles[1]-right_cr_row))
		>= righteye_circles[3]*MAX_CR_PUP_DIST)
  {			/* right eye not aligned */
  if (fabs(righteye_circles[0]-right_cr_col) >
	fabs(righteye_circles[1]-right_cr_row))
    right_align=1;	/* worse horizontal misalign then vertical */
  else
    right_align=2;	/* worse vertical misalign then horizontal */
  }
else
  right_align=0;	/* right eye ok */
if (left_align  &&  right_align)
  (*strabismus)=NOT_LOOKING;
else if (left_align == 0  &&  right_align == 0)
  (*strabismus)=NORMAL;
else if (((left_align == 1  ||  right_align == 1)  &&  a != 0)  ||
	 ((left_align == 2  ||  right_align == 2)  &&  a == 0))
  (*strabismus)=HYPERTROPIA;
else if (pup_to_pup_dist > cr_to_cr_dist)
  (*strabismus)=ESOTROPIA;
else
  (*strabismus)=EXOTROPIA;

}



