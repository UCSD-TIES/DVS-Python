
#include <stdio.h>
#include <math.h>

#define SQR(x) ((x)*(x))

/*
**	This routine calculates and returns the equation of a circle (2D),
**	the variables a, b and r in (X-a)^2 + (Y-b)^2 = r^2).
**	It takes as inputs the x and y coordinates of a set of points
**	(contained in "X_Coord" and "Y_Coord") and an integer "Points_Total"
**	indicating the total number of points.  It returns the three
**	variables a,b and r in "Circle_Eq" indicating the equation of
**	the least-squares-fit circle to the set of points.
*/


void Fit_Circle_To_Points(int		Points_Total,
						  int		X_Coord[],int Y_Coord[],
						  double	Circle_Eq[3])

{
double	**dmatrix(),*dvector(),**A,**At,**b,**Ata,**Inv,*col,d;
int	i,j,*indx,*ivector();
void free_dmatrix(),free_ivector(),free_dvector(),ludcmp(),lubksb();

/*
**	This method works by solving the normal equations Ax=b, for the
**	merit function chi^2(a,b,r)=sum(i=1...N)(r^2-(x_i-a)^2-(y_i-b)^2)^2,
**	where x_i,y_i (i=1...N) are the samples (points to fit).
**	The solution is x=(((A^T A)^-1)A^T)b, where A^T is A transpose and
**	the superscript ^-1 stands for matrix inverse.  Each row of matrix
**	A is [2x_i 2y_i -1], where there are i=1...N samples.  Each row
**	of matrix b is [(x_i)^2+(y_i)^2].  The x matrix is 3x1 and will
**	contain the solution [a b gamma], where gamma=a^2+b^2-r^2 and so
**	may be used to solve for r.
**
**	To weight the points, create a diagonal matrix W which holds the
**	weights as 1/sigma^2, where larger sigma means better points.
**	Then solve the normal equations as X=(((A^T W A)^-1)A^T)Wb.
*/

	/* Create the A, A^T (A transpose) and b matrices.  An Ata matrix is
	** also used, to hold (A^T)A for inversing (result will be in Inv). */

A=dmatrix(1,Points_Total,1,3);
At=dmatrix(1,3,1,Points_Total);
b=dmatrix(1,Points_Total,1,1);
Ata=dmatrix(1,3,1,3);
Inv=dmatrix(1,3,1,3);
indx=ivector(1,3);
col=dvector(1,3);
Ata[1][1]=Ata[1][2]=Ata[1][3]=0.0;
Ata[2][1]=Ata[2][2]=Ata[2][3]=0.0;
Ata[3][1]=Ata[3][2]=Ata[3][3]=0.0;
for (i=1; i<=Points_Total; i++)
  {
  A[i][1]=At[1][i]=2.0*(double)X_Coord[i-1];
  A[i][2]=At[2][i]=2.0*(double)Y_Coord[i-1];
  A[i][3]=At[3][i]=-1.0;
  b[i][1]=(double)(SQR(X_Coord[i-1])+SQR(Y_Coord[i-1]));
  Ata[1][1]+=SQR(A[i][1]);
  Ata[2][2]+=SQR(A[i][2]);
  Ata[3][3]+=SQR(A[i][3]);
  Ata[1][2]+=(A[i][1]*At[2][i]);
  Ata[1][3]+=(A[i][1]*At[3][i]);
  Ata[2][3]+=(A[i][2]*At[3][i]);
  }
Ata[2][1]=Ata[1][2];	/* matrix is symmetrical */
Ata[3][1]=Ata[1][3];
Ata[3][2]=Ata[2][3];

	/* Inverse Ata matrix */

ludcmp(Ata,3,indx,&d);
for (j=1;j<=3;j++)
  {
  for(i=1;i<=3;i++)
    col[i]=0.0;
  col[j]=1.0;
  lubksb(Ata,3,indx,col);
  for(i=1;i<=3;i++) Inv[i][j]=col[i];
  }

	/* Matrix multiply Inv by A^t by b to get x matrix (Circle_Eq). */

Circle_Eq[0]=Circle_Eq[1]=Circle_Eq[2]=0.0;
for (i=1; i<=Points_Total; i++)
  {
  Circle_Eq[0]+=(Inv[1][1]*At[1][i]+Inv[1][2]*At[2][i]+Inv[1][3]*At[3][i])*
	b[i][1];
  Circle_Eq[1]+=(Inv[2][1]*At[1][i]+Inv[2][2]*At[2][i]+Inv[2][3]*At[3][i])*
	b[i][1];
  Circle_Eq[2]+=(Inv[3][1]*At[1][i]+Inv[3][2]*At[2][i]+Inv[3][3]*At[3][i])*
	b[i][1];
  }

	/* Solve for last entry of Circle_Eq (r) using gamma = a^2+b^2-r^2. */

Circle_Eq[2]=sqrt(SQR(Circle_Eq[0])+SQR(Circle_Eq[1])-Circle_Eq[2]);


free_dmatrix(A,1,Points_Total,1,3);
free_dmatrix(At,1,3,1,Points_Total);
free_dmatrix(b,1,Points_Total,1,1);
free_dmatrix(Ata,1,3,1,3);
free_dmatrix(Inv,1,3,1,3);
free_ivector(indx,1,3);
free_dvector(col,1,3);
}

