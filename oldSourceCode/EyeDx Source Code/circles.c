#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <windows.h>
#include "globals.h"

#define	SQR(x) ((x)*(x))
#define M_PI 3.1415927


	/*******************************************************************
	** Fit circles to subsets of points, where each subset is 270
	** degrees of arc.
	*******************************************************************/

void FitSubArcCircle(int	*points,			/* y*COLS+x coords of points to fit */
					int		total_points,		/* number of points in entire arc */
					int		*grad,				/* gradients of points, coded y*COLS+x */
					int		*used,				/* in/out array, telling which points to use */
					int		*total_used_points,	/* number of used points */
					double	best_fit_circle[3],	/* circle equation of subarc fit */
					int		ROWS,int COLS)		/* used to decode points array */

{
int		quadrant,best_quadrant,delta,p,u,i;
double	circle[9][3],std_dev[9],theta_arc[9],avg_grad[9];
double	score,best_score;
int		*x_coords,*y_coords;

x_coords=(int *)calloc(total_points,sizeof(int));
y_coords=(int *)calloc(total_points,sizeof(int));
for (quadrant=0; quadrant<9; quadrant++)
  {
  delta=(int)((double)quadrant/8.0*(double)total_points);
  *total_used_points=0;
  avg_grad[quadrant]=0;
  circle[quadrant][2]=-1.0;
  for (p=0; p<(quadrant == 8 ? total_points : (int)((double)total_points*6.0/8.0) ); p++)
    {
    if (used[(p+delta)%total_points] == 0)
      continue;
    x_coords[*total_used_points]=points[(p+delta)%total_points]%COLS;
    y_coords[*total_used_points]=points[(p+delta)%total_points]/COLS;
    (*total_used_points)++;
    avg_grad[quadrant]+=(double)grad[(p+delta)%total_points];
    }
  if ((double)(*total_used_points)/(double)total_points < 0.2)
    continue;	/* not enough points for circle */
  Fit_Circle_To_Points(*total_used_points,x_coords,y_coords,circle[quadrant]);
  theta_arc[quadrant]=((double)(*total_used_points)/circle[quadrant][2])/(2.0*M_PI);
  std_dev[quadrant]=0.0;	/* stddev of points from circle */
  for (u=0; u<*total_used_points; u++)
    std_dev[quadrant]+=fabs(circle[quadrant][2]-sqrt(SQR((double)x_coords[u]-
          circle[quadrant][0])+SQR((double)y_coords[u]-circle[quadrant][1])));
  std_dev[quadrant]/=(double)(*total_used_points);
  avg_grad[quadrant]/=(double)(*total_used_points);
  }

	/*
	** Calculate each subarc fit's score according to residual,
	** avg gradient, and percent of arc used in fit.
	*/
best_score=0.0;
best_quadrant=-1;
for (i=0; i<9; i++)
  {
  if (circle[i][2] <= 0.0)
	continue;
  if (theta_arc[i] < MIN_EYE_ARC)
	continue;
  score=0.0;
  score+=(1.0-(std_dev[i]/(double)MAX_EYE_RESID)); /* can be negative */
  if (avg_grad[i] > MAX_EYE_GRAD)
	score+=1.0;
  else
	score+=(avg_grad[i]/(double)MAX_EYE_GRAD);
  score+=(theta_arc[i]);
  if (best_quadrant == -1  ||  score > best_score)
	{
	best_quadrant=i;
	best_score=score;
	}
  }
if (best_quadrant != -1)
  {			/* at least one quadrant had enough pixels */
  for (i=0; i<3; i++)
    best_fit_circle[i]=circle[best_quadrant][i];
  delta=(int)((double)best_quadrant/8.0*(double)total_points);
  *total_used_points=0;
  for (p=0; p<total_points; p++)
    {
    if (p >= (int)((double)total_points*6.0/8.0))
      used[(p+delta)%total_points]=0;
    if (used[(p+delta)%total_points])
      (*total_used_points)++;
    }
  }
else			/* no quadrant had enough pixels */
  {
  *total_used_points=0;
  best_fit_circle[0]=best_fit_circle[1]=best_fit_circle[2]=0.0;
  }
free(x_coords);
free(y_coords);
}



	/*******************************************************************
	** Compute a bunch of statistics of a circle and fit points 
	*******************************************************************/

void ComputeCircleFitStatistics(double circle[3],			/* equation of circle */
								int	*points,				/* points, coded y*COLS+x */
								int	total_points,
								int	*used,					/* which points were used in fit */
								int	total_used_points,		/* total points used in fit */
								int	*point_grad,			/* gradients of points */
								int	ROWS,int COLS,			/* used to decode points[] array */
								double *stddev,double *avg_grad,double *avg_spac)	/* outputs */

{
int	p,p2,x,y,x2,y2;

*stddev=0.0;		/* stddev of points from circle */
*avg_grad=0.0;		/* avg gradient of points on circle */
*avg_spac=0.0;		/* average spacing of points on circle */
for (p=0; p<total_points; p++)
  {
  if (used[p])
    {
    x=points[p]%COLS;
    y=points[p]/COLS;
    for (p2=1; p2<total_points; p2++)
      if (used[(p+p2)%total_points])
	break;
    x2=points[(p+p2)%total_points]%COLS;
    y2=points[(p+p2)%total_points]/COLS;
    (*stddev)+=fabs(circle[2]-sqrt(SQR((double)x-circle[0])+
			SQR((double)y-circle[1])) );
    (*avg_grad)+=(double)point_grad[p];
    //(*avg_spac)+=sqrt((double)(SQR(x2-x)+SQR(y2-y)));
	(*avg_spac)++;
    }
  }
(*avg_grad)/=(double)total_used_points;
//(*avg_spac)/=(double)total_used_points;
(*avg_spac)=((*avg_spac)/circle[2]);
(*stddev)/=(double)total_used_points;
}



	/*******************************************************************
	** Traverse string of points, marking as unusable any point which
	** does not belong to (at least) a 5-pixel contiguous chain.
	*******************************************************************/

void DontUseIsolatedPoints(int	*points,		/* indices of points, coded r*COLS+c */
						int	total_points,		/* count */
						int	*used,				/* boolean, which points are used */
						int	*total_used_points,	/* count */
						int	COLS)				/* used to decode points[] array */

{
int	p[9],i,j,t,r1,c1,r2,c2;

t=total_points;
for (p[4]=0; p[4]<t; p[4]++)
  {
  if (!(used[p[4]]))	/* middle point */
    continue;	/* already not used */
  p[0]=p[1]=-1;	/* find indices of next four used points previous in list */
  p[2]=p[3]=-1;
  i=(p[4]-1+t)%t;
  while (p[0] == -1  &&  i != p[4])
    {
    if (used[i])
      {
      if (p[3] == -1) p[3]=i;
      else if (p[2] == -1) p[2]=i;
      else if (p[1] == -1) p[1]=i;
	  else p[0]=i;
      }
    i=(i-1+t)%t;
    }
  p[5]=p[6]=-1;	/* find indices of next four used points following in list */
  p[7]=p[8]=-1;
  i=(p[4]+1)%t;
  while (p[8] == -1  &&  i != p[4])
    {
    if (used[i])
      {
      if (p[5] == -1) p[5]=i;
      else if (p[6] == -1) p[6]=i;
      else if (p[7] == -1) p[7]=i;
      else p[8]=i;
      }
    i=(i+1)%t;
    }
  if (p[0] == -1  ||  p[8] == -1)
    {
    used[p[4]]=0;
    (*total_used_points)--;
    continue;
    }
  for (i=2; i<=6; i++)
    {	/* check 5 5-pixel subchains, with p[i] as middle pixel each time */
	for (j=-2; j<=1; j++)
	  {
      r1=points[p[i+j]]/COLS;
      c1=points[p[i+j]]%COLS;
      r2=points[p[i+j+1]]/COLS;
      c2=points[p[i+j+1]]%COLS;
      if (sqrt((double)(SQR(r1-r2)+SQR(c1-c2))) > 2.5)
		break;	/* this subchain not ok */
	  }
	if (j > 1)	/* this subchain ok */
      break;
    }
  if (i > 6)	/* no ok subchain */
    {
    used[p[4]]=0;
    (*total_used_points)--;
    }
  }
}
