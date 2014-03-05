
#include <stdio.h>
#include <math.h>
#include <windows.h>
#include "globals.h"

#define ANGLE_INC	2.0	/* units are degrees */

#define MIN_GRADIENT	100
#define MIN_RED_GRAD	100

#define MIN_POINTS	0.2	/* units are percentage of total points */

#define DEBUG_GRADS	0
#define DEBUG_FITS	0

	/*******************************************************************
	** For each given point, find the strongest surrounding
	** red-bordering-black circle and the strongest surrounding
	** white-bordering-black circle.  Circle points are taken along
	** ANGLE_INC degree increments radially from the given point,
	** at whichever radii have the largest red/white-black gradient.
	** The points are then fit using a least-squares approach.
	**
	** Statistics on the circle fits are also returned.
	*******************************************************************/

void FindCircles(unsigned char	*raw,	/* raw image data (RGB0,RGB1,RGB2, ...) order */
				int		ROWS,int COLS,
				unsigned char	*disp,	/* image data to display in GUI */
				int		*centers,		/* indices, coded y*COLS+x */
				int		total_centers,	/* number of points to fit circles around */
				double	**red_circles,	/* outputs */
				double	*red_gradients,
				double	*red_spacings,
				double	*red_residuals,
				double	**white_circles,
				double	*white_red_radii,
				double	*white_gradients,
				double	*white_spacings,
				double	*white_residuals)

{
int		r,c,i,j,p;

int		*line_points,*line_grad,*line_red,total_line_points;
int		*white_points,*white_grad,*white_used,total_white_points;
int		*red_points,*red_grad,*red_used,total_red_points;
int		total_used_red_points,total_used_white_points;
int		x_max,x_min,y_max,y_min,sharpest,reddest;

double	theta,white_circle_fit[3],red_circle_fit[3];
double	stddev,avg_grad,avg_spac,dist;
int		*radii_count,largest;
int		*circle_points;

char	text[200];
int	*gi1,*gi2;
unsigned char *giout;
int		x,y,z,smallestG,largestG,smallestR,largestR;
FILE	*fpt;

giout=(unsigned char *)calloc(200*200*3,1);
gi1=(int *)calloc(200*200,sizeof(int));
gi2=(int *)calloc(200*200,sizeof(int));


	/*******************************************************************
	** Everything is allocated twice as big as it needs to be,
	** to give extra protection from memory leaks.
	** All these arrays are pretty small anyway.
	*******************************************************************/

line_points=(int *)calloc(MaxIrisRad*2,sizeof(int));
line_grad=(int *)calloc(MaxIrisRad*2,sizeof(int));
line_red=(int *)calloc(MaxIrisRad*2,sizeof(int));
radii_count=(int *)calloc(MaxIrisRad*2,sizeof(int));
white_points=(int *)calloc((int)(360.0/ANGLE_INC*2.0),sizeof(int));
white_grad=(int *)calloc((int)(360.0/ANGLE_INC*2.0),sizeof(int));
white_used=(int *)calloc((int)(360.0/ANGLE_INC*2.0),sizeof(int));
red_points=(int *)calloc((int)(360.0/ANGLE_INC*2.0),sizeof(int));
red_grad=(int *)calloc((int)(360.0/ANGLE_INC*2.0),sizeof(int));
red_used=(int *)calloc((int)(360.0/ANGLE_INC*2.0),sizeof(int));
circle_points=(int *)calloc(MaxIrisRad*8,sizeof(int));
for (i=0; i<total_centers; i++)
  {
  r=centers[i]/COLS; c=centers[i]%COLS;

	/*******************************************************************
	** find highest (total) gradient and red gradient (both signed)
	** points in all directions
	*******************************************************************/

  total_white_points=total_red_points=0;
  total_used_white_points=total_used_red_points=0;
if (DEBUG_GRADS) {
smallestG=99999; largestG=-99999;
smallestR=99999; largestR=-99999; }
if (DEBUG_FITS) {
for (x=0; x<200; x++)
  for (y=0; y<200; y++)
	if ((y+centers[i]/COLS-100) >= 0  &&  (y+centers[i]/COLS-100) < ROWS  &&
		(x+centers[i]%COLS-100) >= 0  &&  (x+centers[i]%COLS-100) < COLS)
	  for (z=0; z<3; z++)
		giout[(y*200+x)*3+z]=raw[((y+centers[i]/COLS-100)*COLS+(x+centers[i]%COLS-100))*3+z];
	else
	  for (z=0; z<3; z++)
		giout[(y*200+x)*3+z]=0;
}
  for (theta=0.0; theta<2.0*M_PI; theta+=(ANGLE_INC*M_PI/180.0))
    {
		/* find indices of pixels along radial line segment */
    x_min=centers[i]%COLS+(int)((double)MinPupilRad*cos(theta));
    y_min=centers[i]/COLS+(int)((double)MinPupilRad*sin(theta));
    x_max=centers[i]%COLS+(int)((double)MaxIrisRad*cos(theta));
    y_max=centers[i]/COLS+(int)((double)MaxIrisRad*sin(theta));
    MakeLineIndices(x_min,y_min,x_max,y_max,ROWS,COLS,
					line_points,&total_line_points);
		/* compute total gradient, and red-only gradient, along line */
    for (p=3; p<total_line_points-3; p++)
      {		/* gradient is computed in 7x1 window, along ray */
	  if (sqrt(SQR(line_points[p]%COLS-centers[i]%COLS)+
		  SQR(line_points[p]/COLS-centers[i]/COLS)) < (double)MinIrisRad)
		line_grad[p]=0;
	  else
        line_grad[p]=(raw[line_points[p+1]*3+2]-raw[line_points[p-1]*3+2])+
			(raw[line_points[p+1]*3+1]-raw[line_points[p-1]*3+1])+
			(raw[line_points[p+1]*3+0]-raw[line_points[p-1]*3+0])+
			1*(raw[line_points[p+2]*3+2]-raw[line_points[p-2]*3+2])+
			1*(raw[line_points[p+2]*3+1]-raw[line_points[p-2]*3+1])+
			1*(raw[line_points[p+2]*3+0]-raw[line_points[p-2]*3+0])+
			1*(raw[line_points[p+3]*3+2]-raw[line_points[p-3]*3+2])+
			1*(raw[line_points[p+3]*3+1]-raw[line_points[p-3]*3+1])+
			1*(raw[line_points[p+3]*3+0]-raw[line_points[p-3]*3+0]);
	  if (sqrt(SQR(line_points[p]%COLS-centers[i]%COLS)+
		  SQR(line_points[p]/COLS-centers[i]/COLS)) > (double)MaxPupilRad)
		line_red[p]=0;
	  else
        line_red[p]=( (raw[line_points[p-1]*3+0]-raw[line_points[p+1]*3+0])+
			1*(raw[line_points[p-2]*3+0]-raw[line_points[p+2]*3+0])+
			1*(raw[line_points[p-3]*3+0]-raw[line_points[p+3]*3+0]) )*3;
if (DEBUG_GRADS) {
x=line_points[p]%COLS; y=line_points[p]/COLS;
if (line_grad[p] > largestG) largestG=line_grad[p];
if (line_grad[p] < smallestG) smallestG=line_grad[p];
if (line_red[p] > largestR) largestR=line_red[p];
if (line_red[p] < smallestR) smallestR=line_red[p];
gi1[(y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100)]=line_grad[p];
gi2[(y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100)]=line_red[p];
}
      }
		/* find sharpest black->white and red->not_red spots on line */
    sharpest=reddest=1;
    for (p=2; p<total_line_points-2; p++)
      {
      if (line_grad[p] > line_grad[sharpest])
		sharpest=p;
      if (p < MaxPupilRad  &&  line_red[p] > line_red[reddest])
		reddest=p;
      }
if (DEBUG_FITS) {
x=line_points[reddest]%COLS; y=line_points[reddest]/COLS;
giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+0]=0;
giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+1]=255;
giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+2]=0;
x=line_points[sharpest]%COLS; y=line_points[sharpest]/COLS;
giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+0]=255;
giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+1]=255;
giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+2]=0;
}
		/* check if best red-gradient-pt is new or not */
    for (j=0; j<total_red_points; j++)
      if (red_points[j] == line_points[reddest])
        break;
    if (j == total_red_points)
      {
      red_points[total_red_points]=line_points[reddest];
      red_grad[total_red_points]=line_red[reddest];
		/* check if red-gradient-pt is strong enough for fitting */
      if (line_red[reddest] > MIN_RED_GRAD  &&  reddest < sharpest-3)
	    {
        red_used[total_red_points]=1;
		total_used_red_points++;
		}
      else
        red_used[total_red_points]=0;
      total_red_points++;
      }
		/* check if best gradient-pt is new or not */
    for (j=0; j<total_white_points; j++)
      if (line_points[sharpest] == white_points[j])
        break;
    if (j == total_white_points)
      {
      white_points[total_white_points]=line_points[sharpest];
      white_grad[total_white_points]=line_grad[sharpest];
		/* check if gradient-pt is strong enough for fitting */
      if (line_grad[sharpest] > MIN_GRADIENT)
        {
        white_used[total_white_points]=1;
        total_used_white_points++;
        }
      else
        white_used[total_white_points]=0;
      total_white_points++;
      }
    }
if (DEBUG_GRADS) {
for (x=0; x<200*200; x++)
  giout[x]=(unsigned char)((double)(gi1[x]-smallestG)/(double)(largestG-smallestG)*255.0);
sprintf(text,"grad%d.pgm",i);
fpt=fopen(text,"wb");
fprintf(fpt,"P5 200 200 255\n");
fwrite(giout,200*200,1,fpt);
fclose(fpt);
for (x=0; x<200*200; x++)
  giout[x]=(unsigned char)((double)(gi2[x]-smallestR)/(double)(largestR-smallestR)*255.0);
sprintf(text,"red%d.pgm",i);
fpt=fopen(text,"wb");
fprintf(fpt,"P5 200 200 255\n");
fwrite(giout,200*200,1,fpt);
fclose(fpt);
sprintf(text,"%d...%d %d...%d",smallestG,largestG,smallestR,largestR);
MessageBox(NULL,text,"stats",MB_OK | MB_APPLMODAL);
}
if (DEBUG_FITS) {
sprintf(text,"allpts%d.ppm",i);
fpt=fopen(text,"wb");
fprintf(fpt,"P6 200 200 255\n");
fwrite(giout,200*200*3,1,fpt);
fclose(fpt);
}

	/*******************************************************************
	** Try to fit circle to red points
	*******************************************************************/

  DontUseIsolatedPoints(red_points,total_red_points,red_used,
		&total_used_red_points,COLS);
  red_circles[i][2]=-1.0;	/* means don't have circle (yet) */
  if ((double)total_used_red_points/(double)total_red_points > MIN_POINTS)
    {
if (DEBUG_FITS) {
for (x=0; x<200; x++)
  for (y=0; y<200; y++)
	if ((y+centers[i]/COLS-100) >= 0  &&  (y+centers[i]/COLS-100) < ROWS  &&
		(x+centers[i]%COLS-100) >= 0  &&  (x+centers[i]%COLS-100) < COLS)
	  for (z=0; z<3; z++)
		giout[(y*200+x)*3+z]=raw[((y+centers[i]/COLS-100)*COLS+(x+centers[i]%COLS-100))*3+z];
	else
	  for (z=0; z<3; z++)
		giout[(y*200+x)*3+z]=0;
for (z=0; z<total_red_points; z++)
  if (red_used[z])
  { x=red_points[z]%COLS; y=red_points[z]/COLS;
    giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+0]=255;
    giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+1]=0;
    giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+2]=0;
  }
sprintf(text,"strand%d.ppm",i);
fpt=fopen(text,"wb");
fprintf(fpt,"P6 200 200 255\n");
fwrite(giout,200*200*3,1,fpt);
fclose(fpt);
if (i == 1) red_used[230]=-1; else red_used[230]=0;
}
    FitSubArcCircle(red_points,total_red_points,red_grad,red_used,
		&total_used_red_points,red_circle_fit,ROWS,COLS);
    if (total_used_red_points > 0  &&  red_circle_fit[2] <= (double)MAX_PUPIL_RAD)
      {
      ComputeCircleFitStatistics(red_circle_fit,red_points,
		total_red_points,red_used,total_used_red_points,
		red_grad,ROWS,COLS,&stddev,&avg_grad,&avg_spac);

      red_circles[i][0]=red_circle_fit[0];	/* circle column */
      red_circles[i][1]=red_circle_fit[1];	/* circle row */
      red_circles[i][2]=red_circle_fit[2];	/* circle radius */
      red_residuals[i]=stddev;
      red_gradients[i]=avg_grad;
      red_spacings[i]=avg_spac;
if (DEBUG_FITS) {
for (x=0; x<200; x++)
  for (y=0; y<200; y++)
	if ((y+centers[i]/COLS-100) >= 0  &&  (y+centers[i]/COLS-100) < ROWS  &&
		(x+centers[i]%COLS-100) >= 0  &&  (x+centers[i]%COLS-100) < COLS)
	  for (z=0; z<3; z++)
		giout[(y*200+x)*3+z]=raw[((y+centers[i]/COLS-100)*COLS+(x+centers[i]%COLS-100))*3+z];
	else
	  for (z=0; z<3; z++)
		giout[(y*200+x)*3+z]=0;
for (z=0; z<total_red_points; z++)
  if (red_used[z])
  { x=red_points[z]%COLS; y=red_points[z]/COLS;
    giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+0]=255;
    giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+1]=0;
    giout[((y-centers[i]/COLS+100)*200+(x-centers[i]%COLS+100))*3+2]=0;
  }
sprintf(text,"used%d.ppm",i);
fpt=fopen(text,"wb");
fprintf(fpt,"P6 200 200 255\n");
fwrite(giout,200*200*3,1,fpt);
fclose(fpt);
}
      }
    }

	/*******************************************************************
	** Try to fit circle to white points.  Keep circle if it fits a
	** minimum amount of subarc, AND if the bright point lies within the
	** fitted circle (it must lie at least within the iris, if not pupil).
	*******************************************************************/

  DontUseIsolatedPoints(white_points,total_white_points,white_used,
		&total_used_white_points,COLS);
  white_circles[i][2]=-1.0;	/* means don't have circle (yet) */
  if ((double)total_used_white_points/(double)total_white_points > MIN_POINTS)
    {
    FitSubArcCircle(white_points,total_white_points,white_grad,white_used,
		&total_used_white_points,white_circle_fit,ROWS,COLS);
    if (total_used_white_points > 0  &&  sqrt(SQR(white_circle_fit[0]-c)
					+SQR(white_circle_fit[1]-r)) < white_circle_fit[2]  &&
		white_circle_fit[2] <= (double)MAX_IRIS_RAD)
      {
      ComputeCircleFitStatistics(white_circle_fit,white_points,
		total_white_points,white_used,total_used_white_points,
		white_grad,ROWS,COLS,&stddev,&avg_grad,&avg_spac);

      white_circles[i][0]=white_circle_fit[0];	/* circle column */
      white_circles[i][1]=white_circle_fit[1];	/* circle row */
      white_circles[i][2]=white_circle_fit[2];	/* circle radius */
      white_residuals[i]=stddev;
      white_gradients[i]=avg_grad;
      white_spacings[i]=avg_spac;

	/*******************************************************************
	** If a red circle was fit, compute mode radius of white points
	** from center of red circle (better fit?).
	*******************************************************************/

      if (red_circles[i][2] >= 0.0)
		{
        for (j=MinIrisRad; j<=MaxIrisRad; j++)
		  radii_count[j]=0;
		for (p=0; p<total_white_points; p++)
		  {
          dist=sqrt((double)(
				SQR((white_points[p]%COLS)-red_circles[i][0])+
				SQR((white_points[p]/COLS)-red_circles[i][1]) ));
		  if ((int)dist >= MinIrisRad  &&  (int)dist <= MaxIrisRad)
		    radii_count[(int)dist]++;
		  }
		largest=MinIrisRad;
		for (j=MinIrisRad+1; j<=MaxIrisRad; j++)
		  if (radii_count[j] > radii_count[largest])
		    largest=j;
		white_red_radii[i]=(double)largest;  /* white radius from red center */
		}
      }
    }
  if (DisplayGraphics == 1)
	{
	for (r=-CircleThickness; r<=CircleThickness; r++)
	  {
      if (red_circles[i][2] >= 0.0)
	    {
	    MakeCircleIndices(red_circles[i][0],red_circles[i][1],red_circles[i][2]+(double)r,
				ROWS,COLS,circle_points,&total_red_points);
        for (j=0; j<total_red_points; j++)
	      disp[circle_points[j]*3+1]=255;
	    MakeCircleIndices(red_circles[i][0],red_circles[i][1],white_red_radii[i]+(double)r,
				ROWS,COLS,circle_points,&total_white_points);
        for (j=0; j<total_white_points; j++)
	      disp[circle_points[j]*3+0]=255;
	    }
      else if (white_circles[i][2] >= 0.0)
	    {
	    MakeCircleIndices(white_circles[i][0],white_circles[i][1],white_circles[i][2]+(double)r,
				ROWS,COLS,circle_points,&total_white_points);
        for (j=0; j<total_white_points; j++)
	      disp[circle_points[j]*3+0]=255;
	    }
	  }
	MakeDisplayImage(disp,ROWS,COLS,0);
    PaintImage();
/*
sprintf(text,"resid/grad/spac %lf %lf %lf | %lf %lf %lf",
		red_residuals[i],red_gradients[i],red_spacings[i],
		white_residuals[i],white_gradients[i],white_spacings[i]);
MessageBox(NULL,text,"stats",MB_OK | MB_APPLMODAL);
/**/
    }
  }

free(line_points);
free(line_grad);
free(line_red);
free(radii_count);
free(white_points);
free(white_grad);
free(white_used);
free(red_points);
free(red_grad);
free(red_used);
free(circle_points);
}
