
#include <stdio.h>
#include <math.h>
#include <windows.h>
#include "globals.h"

	/*******************************************************************
	** Takes in a set of circles, with their fitted statistics.
	** Normalizes all statistics, sorts by sum, and returns the
	** indices of the strongest and second strongest circles.
	** The function return-value is the total number of used circles.
	*******************************************************************/

int BestTwoCircles(	int		*points,			/* CRs, coded y*COLS+x */
					int		COLS,
					int     total_circles,		/* total number of (possible) circles */
					double  **red_circles,		/* circle data */
					double  *red_gradients,
					double  *red_spacings,
					double  *red_residuals,
					double  **white_circles,
					double  *white_red_radii,
					double  *white_gradients,
					double  *white_spacings,
					double  *white_residuals,
					int		*one,int *two)		/* outputs:  indices of two best circles */

{
int		i,j,used_circles,*indices;
double	BestUsableScore,a1,b1,c1,a2,b2,c2;
double	*sums,**scores;
//FILE *fpt;

indices=(int *)calloc(MAX_BRIGHTS,sizeof(int));
sums=(double *)calloc(MAX_BRIGHTS,sizeof(double));
scores=(double **)calloc(MAX_BRIGHTS,sizeof(double *));
for (i=0; i<MAX_BRIGHTS; i++)
  scores[i]=(double *)calloc(6,sizeof(double));

//fpt=fopen("models.txt","w");
//for (i=0; i<total_circles; i++)
//  fprintf(fpt,"%d => %lf %lf %lf  |  %lf %lf %lf\n",i,
//		red_residuals[i],red_gradients[i],red_spacings[i],
//		white_residuals[i],white_gradients[i],white_spacings[i]);


	/******************************************************************
	** Normalize all residuals, spacings, and gradients into `scores'
	** array.  residuals and spacings must be inverted,
	** to make higher values mean better for all scores.
	** residuals is normalized from 0...MAX_EYE_RESID.
	** spacings is normalized from 0...MAX_EYE_SPACE.
	** gradients is normalized from 0...MAX_EYE_GRAD.
	** arcs is normalized from 0...2pi.
	** Any values outside these ranges are capped to 0 or 1.
	** Sum scores for each red and white circle, holding higher
	** score in `sums' array.
	******************************************************************/

used_circles=0;
for (i=0; i<total_circles; i++)
  {
  if (red_circles[i][2] > 0.0)
    {
//	if (red_residuals[i] > MAX_EYE_RESID)
//	  scores[used_circles][0]=0.0;
//	else
      scores[used_circles][0]=1.0-(red_residuals[i]/(double)MAX_EYE_RESID);
	if (red_gradients[i] > MAX_EYE_GRAD)
	  scores[used_circles][1]=1.0;
	else
      scores[used_circles][1]=red_gradients[i]/(double)MAX_EYE_GRAD;
//	if (red_spacings[i] > MAX_EYE_SPACE)
//	  scores[used_circles][2]=0.0;
//	else
//	  scores[used_circles][2]=1.0-(red_spacings[i]/(double)MAX_EYE_SPACE);
	scores[used_circles][2]=red_spacings[i]/(2.0*M_PI);
    }
  else
    scores[used_circles][0]=scores[used_circles][1]=scores[used_circles][2]=0.0;
  if (white_circles[i][2] > 0.0)
    {
//	if (white_residuals[i] > MAX_EYE_RESID)
//	  scores[used_circles][3]=0.0;
//	else
      scores[used_circles][3]=1.0-(white_residuals[i]/(double)MAX_EYE_RESID);
	if (white_gradients[i] > MAX_EYE_GRAD)
	  scores[used_circles][4]=1.0;
	else
      scores[used_circles][4]=white_gradients[i]/(double)MAX_EYE_GRAD;
//	if (white_spacings[i] > MAX_EYE_SPACE)
//	  scores[used_circles][5]=0.0;
//	else
//	  scores[used_circles][5]=1.0-(white_spacings[i]/(double)MAX_EYE_SPACE);
	scores[used_circles][5]=white_spacings[i]/(2.0*M_PI);
    }
  else
    scores[used_circles][3]=scores[used_circles][4]=scores[used_circles][5]=0.0;
  if (red_circles[i][2] >= 0.0  ||  white_circles[i][2] >= 0.0)
    {
//    if (scores[used_circles][0]+scores[used_circles][1]+
//		scores[used_circles][2] > scores[used_circles][3]+
//		scores[used_circles][4]+scores[used_circles][5])
//      sums[used_circles]=scores[used_circles][0]+
//		scores[used_circles][1]+scores[used_circles][2];
//    else
//      sums[used_circles]=scores[used_circles][3]+
//		scores[used_circles][4]+scores[used_circles][5];
	sums[used_circles]=scores[used_circles][0]+scores[used_circles][1]+scores[used_circles][2]+
						scores[used_circles][3]+scores[used_circles][4]+scores[used_circles][5];
    indices[used_circles]=i;
    used_circles++;
//fprintf(fpt,"%d => %lf %lf %lf  |  %lf %lf %lf  |  %lf\n",indices[used_circles-1],
//		scores[used_circles-1][0],scores[used_circles-1][1],scores[used_circles-1][2],
//		scores[used_circles-1][3],scores[used_circles-1][4],scores[used_circles-1][5],sums[used_circles-1]);
    }
  }
//fclose(fpt);

	/******************************************************************
	** Search sums array for highest scoring pair, that also passes
	** some criteria:  eye models at least one diameter-average apart,
	** eye models either vertically or horizontally aligned (within
	** HEAD_TILT tolerance).  The indices array is used for matching
	** back into the original circles-data.
	******************************************************************/

BestUsableScore=0.0;
(*one)=(*two)=0;
for (i=0; i<used_circles; i++)
  {
  if (sums[i] < 0.0)
	continue;	/* marked as not good, from below */
  for (j=0; j<used_circles; j++)
	{
	if (i == j)
	  continue;
	if (sums[j] < 0.0)
	  continue;	/* marked as not good, from below */
	if (red_circles[indices[i]][2] > 0.0)
	  {
	  a1=red_circles[indices[i]][0];
	  b1=red_circles[indices[i]][1];
	  c1=white_red_radii[indices[i]];
	  }
	else
	  {
	  a1=white_circles[indices[i]][0];
	  b1=white_circles[indices[i]][1];
	  c1=white_circles[indices[i]][2];
	  }
	if (red_circles[indices[j]][2] > 0.0)
	  {
	  a2=red_circles[indices[j]][0];
	  b2=red_circles[indices[j]][1];
	  c2=white_red_radii[indices[j]];
	  }
	else
	  {
	  a2=white_circles[indices[j]][0];
	  b2=white_circles[indices[j]][1];
	  c2=white_circles[indices[j]][2];
	  }
    if (sqrt(SQR(a1-a2)+SQR(b1-b2)) <= 2.0*(c1+c2))
	  {
	  if (sqrt(SQR(points[indices[i]]/COLS-b1)+SQR(points[indices[i]]%COLS-a1)) >
		  sqrt(SQR(points[indices[j]]/COLS-b2)+SQR(points[indices[j]]%COLS-a2)))
		{
		sums[i]=-1.0;	/* model j better than i for same area */
		(*one)=(*two)=0;/* start over */
		BestUsableScore=0.0;
		i=0;
		break;
		}
	  continue;		/* eye models overlapping -- not possible */
	  }
    if (atan2(fabs(a1-a2),fabs(b1-b2)) > MAX_HEAD_TILT*M_PI/180.0  &&
		atan2(fabs(b1-b2),fabs(a1-a2)) > MAX_HEAD_TILT*M_PI/180.0)
	  continue;		/* eye models not at acceptable angle */
	if (sums[i]+sums[j] > BestUsableScore)
	  {
	  BestUsableScore=sums[i]+sums[j];
	  *one=indices[i];
	  *two=indices[j];
	  }
	}
  }
if (*one == 0  &&  *two == 0)
  return(0);	/* no acceptable pair found */

free(indices);
free(sums);
for (i=0; i<MAX_BRIGHTS; i++)
  free(scores[i]);
free(scores);
return(used_circles);
}
