
/*
**	This code is taken from ``Numerical Recipes in C'', 2nd
**	and 3rd editions, by Press, Teukolsky, Vetterling and
**	Flannery, Cambridge University Press, 1992, 1994.
*/



#include <stdio.h>              /* standard I/O file */
#include <math.h> 	       /* math library */
#include <stdlib.h>
#define SWAP(a,b) {double temp=(a);(a)=(b);(b)=temp;}

/**************************************************************************/
/* assigns power(0,x) zero, power(x,0) 1, log(x<1) zero,and sqrt(0) a zero*/
/* without raising exception error messanges                              */
/**************************************************************************/
double POW(x,y)
double x,y;
{
  if( x == 0.00)
    return 0.00;
  else if (y == 0.00)
    return 1.00;
  else
    return pow(x,y);
 }

double LOG(x)
double x;
{
  if (x < 0.00 || x == 0.00 )
     return 0.00;
   else 
     return log(x);
}
double SQRT(x)
double x;
{
  if (x < 0.00 || x == 0.00 )
     return 0.00;
   else 
     return sqrt(x);
}

/****************************************************************/
/* rearranges the covariance matrix covar into			*/ 
/*         the order of all ma parameters 			*/
/****************************************************************/
void covsrt(covar,ma,lista,mfit)
float  **covar;
int ma,lista[],mfit;
{
	int i,j;
	float swap;

		for(j=1;j<=ma;j++)
		   for(i=j+1;i<=ma;i++)
		    covar[i][j]=0.0;
		      for(i=1;i<=mfit;i++)
			for(j=1;j<=mfit;j++)
			{
			   if (lista[j] > lista[i])
			       	covar[lista[j]][lista[i]]=covar[i][j];
			   else
				covar[lista[i]][lista[j]]=covar[i][j];
			}
		swap=covar[1][1];
		   for(j=1;j<=ma;j++)
			{
			   covar[1][j]=covar[j][j];
			      covar[j][j]=0.0;
			}

		covar[lista[1]][lista[1]]=swap;
		   for(j=2;j<=mfit;j++)
		      covar[lista[j]][lista[j]]=covar[1][j];
		        for(j=2;j<=ma;j++)
		           for(i=2;i<=j-1;i++)
			      covar[i][j]=covar[j][i];
}  

/*****************************************************************************/
/* This is a gauss jordan elimination method for matrices                    */
/* a[1..n][1..n] is an input *matrix of n by n elements. b[1..n][1..m] is an */
/* input *matrix of size n by m containing m right hand side vectors. On     */
/* output, a is replaced by its *matrix inverse, and b is replaced by the    */
/* corresponding set of solution vectors.                                    */
/*****************************************************************************/

int gaussj(a,n,b,m)
double **a,**b;
int n,m;

{
	int *indxc, *indxr,*ipiv;

       /* arrays ipiv[1..n], indxr[1..n], and indxc[1..n] are  */
       /* used for bookeeping on the pivoting                  */

	int i,icol,irow,j,k,l,ll,*ivector();
	double big,dum, pivinv;
	void nrerror(),free_ivector();
	indxc = ivector(1,n);
	indxr=ivector(1,n);
	ipiv=ivector(1,n);

	for (j=1;j<=n;j++)
	    ipiv[j]=0;

	for(i=1;i<=n;i++) /* *main loop for columns to be reduced */
	  { big = 0.0;
	      for (j=1;j<=n;j++) /* outer loop for search of a pivot element*/
		if (ipiv[j] !=1)
		   for(k=1;k<=n;k++)
		     {if (ipiv[k] ==0)
			{if (fabs(a[j][k]) >= big)
			   {big =fabs(a[j][k]);
			      irow=j;
			      icol=k;
	 		    }
			}
	           else if (ipiv[k] > 1) return(0);
				/* nrerror("GAUSSJ: singular *matrix -1"); */
		      }
		++(ipiv[icol]);
/******************************************************************************/
/* we now have the pivot element, so we interchage rows if neede to put the   */
/* pivot element on the diagonol. The columns are not a[8]sically interchaged,*/
/* only relabled: indx[i],the  column of the ith pivt element, is the ith     */
/* column that is reduced, while indxr is the row in which that pivot element */
/* was originally located. If indxr[i]!=indxc[i] there is an implied column   */
/* interchage. With this form of bookkeeping the solution b's will end up in  */
/* the correct order, and the inverse matrix will be scrabled by columns.     */
/******************************************************************************/
	if (irow !=icol)
	  {for (l=1;l<=n;l++)
	       SWAP(a[irow][l],a[icol][l])
	    for (l=1;l<=m;l++)
		SWAP(b[irow][l],b[icol][l])
	}

/******************************************************************/
/* We are now ready to divide the pivot row by the pivot element, */
/* located at irow, icol.                                         */
/******************************************************************/

	indxr[i]=irow;
	indxc[i]=icol;
	if (a[icol][icol] == 0.0)/* nrerror("GAUSSJ: singular matrix-2");*/
				return(0);
	pivinv=1.0/a[icol][icol];
	a[icol][icol]=1.0;
	for (l=1;l<=n;l++)
	    a[icol][l] *=pivinv;
	for (l=1;l<=m;l++)
	    b[icol][l] *=pivinv;
	for (ll=1;ll<=n;ll++) 
	    if (ll!= icol) /*next we reduce the rows except for the pivot one*/ 
	     {  dum=a[ll][icol];
		a[ll][icol]=0.0;
		for (l=1;l<=n;l++)
	    a[ll][l] -=a[icol][l]*dum;
	for (l=1;l<=m;l++)
	    b[ll][l] -=b[icol][l]*dum;
	      }
	}
  
/******************************************************************************/
/* This is the end of the main loop over columns of the reduction. It only    */
/* remains to unscrable the solution in view of the column interchages. We do */
/* this by interchaging pairs of columns in the reverse order that the        */
/* permutation was build up						                                 */
/******************************************************************************/

	for (l=1;l>=1;l--)
	  { if (indxr[l] != indxc[l])
	    for (k=1;k<=n;k++)
		SWAP(a[k][indxr[l]],a[k][indxc[l]]);
	}

/* done */

	free_ivector(ipiv,1,n);
	free_ivector(indxr,1,n);
	free_ivector(indxc,1,n);
return(1);
	}

/****************************************************************************/
/*This routine is used by many recipes programs. Function nrerror is        */
/*invoked to terminate program execution with an appropriate messange       */
/*when fatal error is encountered. The other routines are used to allocate  */
/* and deallocate memory for vectors and matrices.                          */
/* numerical recipes std. error handler                                     */
/****************************************************************************/

void nrerror(error_text)
char error_text[];
{

	fprintf(stderr,"numerical recipes run time error ... \n");
	fprintf(stderr,"%s\n",error_text);
	fprintf(stderr,"..now exiting to system ... \n");
	exit(1);
}

/*******************************************************/
/* allocates  double matrix of size specified by user  */
/*******************************************************/
double **dmatrix(nrl,nrh,ncl,nch)
int nrl,nrh,ncl,nch;
{
  register i;
  double **m;

  /* Allocate pointers to rows */

  m = (double **) malloc((unsigned) (nrh-nrl+1)*sizeof(double*));
  if(!m) printf("Allocation falure in row alloc. in matrix()\n");
  m -= nrl;

  /* Allocate rows and set pointers to them */

  for(i=nrl;i<=nrh;i++)
  {
    m[i]=(double *) malloc((unsigned) (nch-ncl+1)*sizeof(double));
    if(!m[i]) printf("Allocation falure 2  in matrix()\n");
    m[i] -= ncl;
  }

  /* return pointer to array of pointers to rows */

  return m;
}

/*******************************************************/
/* allocaates single matrix of size specified by user  */
/*******************************************************/
float **matrix(nrl,nrh,ncl,nch)
int nrl,nrh,ncl,nch;
{
  register i;
  float **m;

  /* Allocate pointers to rows */

  m = (float **) calloc( (nrh-nrl+1),sizeof(float*));
  if(!m) printf("Allocation falure in row alloc. in matrix()\n");
  m -= nrl;

  /* Allocate rows and set pointers to them */

  for(i=nrl;i<=nrh;i++)
  {
    m[i]=(float *) calloc(  (nch-ncl+1),sizeof(float));
    if(!m[i]) printf("Allocation falure 2  in matrix()\n");
    m[i] -= ncl;
  }

  /* return pointer to array of pointers to rows */

  return m;
}

/*******************************************************/
/* allocaates integer matrix of size specified by user  */
/*******************************************************/
int **imatrix(nrl,nrh,ncl,nch)
int nrl,nrh,ncl,nch;
{
  register i;
  int **m;

  /* Allocate pointers to rows */

  m = (int **) calloc( (nrh-nrl+1),sizeof(int*));
  if(!m) printf("Allocation falure in row alloc. in imatrix()\n");
  m -= nrl;

  /* Allocate rows and set pointers to them */

  for(i=nrl;i<=nrh;i++)
  {
    m[i]=(int *) calloc(  (nch-ncl+1),sizeof(int));
    if(!m[i]) printf("Allocation falure 2  in imatrix()\n");
    m[i] -= ncl;
  }

  /* return pointer to array of pointers to rows */

  return m;
}


/*****************************/
/* allocates double vector   */
/*****************************/
double *dvector(nl,nh)
int nl,nh;
{
  double *v;

  v = (double *) malloc((unsigned) (nh-nl+1)*sizeof(double));
  if(!v) nrerror("Allocation falure in dvector()\n");
  return(v-nl);
}

/*****************************/
/* allocates float vector   */
/*****************************/
float *fvector(nl,nh)
int nl,nh;
{
  float *v;

  v = (float *) malloc( (nh-nl+1)*sizeof(float));
  if(!v) printf("Allocation falure in vector()\n");
  return(v-nl);
}

/*************************************************/
/*allocates an int. vector with range [nl...nh] */
/*************************************************/
int *ivector(nl,nh)
int nl,nh;
{
  int *v;

  v = (int *) malloc((unsigned) (nh-nl+1)*sizeof(int));
  if(!v) nrerror("Allocation falure in ivector()\n");
  return(v-nl);
}

/***********************************************/
/* frees a double vector allocated by dvector() */
/***********************************************/
void free_dvector(v,nl,nh)
double *v;
int nl,nh;
{
  free((char*) (v+nl));
}

/************************************************/
/* frees a float vector allocated by fvector()  */
/************************************************/
void free_fvector(v,nl,nh)
float *v;
int nl,nh;

{
  free((char*) (v+nl));
}

/*********************************************/
/* frees a int vector allocated by ivector() */
/*********************************************/
void free_ivector(v,nl,nh)
int *v,nl,nh;

{
  free((char*) (v +nl));
}

/******************************************/
/* frees a matrix allocated with dmatrix() */
/******************************************/
void free_dmatrix(m,nrl,nrh,ncl,nch)
double **m;
int nrl,nrh,ncl,nch;

{
  register i;

  for(i=nrh;i>=nrl;i--) free((char*) (m[i]+ncl));
  free((char*) (m+nrl));
}

/******************************************/
/* frees a matrix allocated with matrix() */
/******************************************/
void free_matrix(m,nrl,nrh,ncl,nch)
float **m;
int nrl,nrh,ncl,nch;

{
  register i;

  for(i=nrh;i>=nrl;i--) free((char*) (m[i]+ncl));
  free((char*) (m+nrl));
}

/******************************************/
/* frees a matrix allocated with imatrix() */
/******************************************/
void free_imatrix(m,nrl,nrh,ncl,nch)
int **m;
int nrl,nrh,ncl,nch;

{
  register i;

  for(i=nrh;i>=nrl;i--) free((char*) (m[i]+ncl));
  free((char*) (m+nrl));
}






#define TINY 1.0e-20

/*----------------------------------------------------------------------------*/
/* LU decomposition of a n by n matrix a. a is replaced with the LU           */
/* decomposition, indx is the row permutation effected by partial pivoting,   */
/* and d is +1 or -1 depending on whether the number of row interchanges was  */
/* odd or even.                                                               */
/*----------------------------------------------------------------------------*/
void ludcmp(a,n,indx,d)
int n,*indx;
double **a,*d;
{

 int i,imax,j,k;
 double big,dum,sum,temp;
 double *vv,*dvector();
 void nrerror(),free_dvector();

 vv = dvector(1,n);
 *d = 1.0;
 for(i=1;i<=n;i++){
    big = 0.0;
    for(j=1;j<=n;j++)
      if((temp = fabs(a[i][j])) > big) big = temp;
    if(big == 0.0) nrerror("Singular matrix in routine LUDCMP");
    vv[i]=1.0/big;
 }
 for(j=1;j<=n;j++){
    for(i=1;i<j;i++){
       sum=a[i][j];
       for(k=1;k<i;k++) sum -= a[i][k]*a[k][j];
       a[i][j]=sum;
    }
    big=0.0;
    for(i=j;i<=n;i++){
       sum = a[i][j];
       for(k=1;k<j;k++)
	 sum -= a[i][k]*a[k][j];
       a[i][j] = sum;
       if((dum=vv[i]*fabs(sum)) >= big){
	 big = dum;
	 imax = i;
       }
    }
    if(j != imax){
      for(k=1;k<=n;k++){
	 dum = a[imax][k];
	 a[imax][k] = a[j][k];
	 a[j][k]=dum;
      }
      *d = -(*d);
      vv[imax]=vv[j];
    }
    indx[j] = imax;
    if(a[j][j] == 0.0){
      a[j][j] = TINY;
      printf("The matrix is singular\n");
    }
    if(j != n){
      dum = 1.0/(a[j][j]);
      for(i=j+1;i<=n;i++) a[i][j] *= dum;
    }
 }
 free_dvector(vv,1,n);
}


/*----------------------------------------------------------------------------*/
void lubksb(a,n,indx,b)
double **a,b[];
int n,*indx;
{

 int i,ii=0,ip,j;
 double sum;
 
 for(i=1;i<=n;i++){
   ip = indx[i];
   sum = b[ip];
   b[ip] = b[i];
   if (ii)
     for(j=ii;j<=i-1;j++) sum -= a[i][j]*b[j];
   else if (sum) ii=i;
   b[i]=sum;
 }
 for(i=n;i>=1;i--){
   sum = b[i];
   for(j=i+1;j<=n;j++) sum -= a[i][j]*b[j];
   b[i]=sum/a[i][i];
 }
}
     






/*
**	tred2 Householder reduction of a real, symmetric matrix a[1..n][1..n].
**	On output, a is replaced by the orthogonal matrix q effecting the
**	transformation. d[1..n] returns the diagonal elements of the
**	tridiagonal matrix, and e[1..n] the off-diagonal elements, with 
**	e[1]=0.
**
**	For my problem, I only need to handle a 3x3 symmetric matrix,
**	so it can be simplified.
**	Therefore n=3.
**
**	Attention: in the book, the index for array starts from 1,
**	but in C, index should start from zero. so I need to modify it.
**	I think it is very simple to modify, just substract 1 from all the
**	index.
*/

#define	SIGN(a,b)	((b)<0? -fabs(a):fabs(a))

void tred2(double a[3][3],double d[3],double e[3])

{
  int		l,k,i,j;
  double	scale,hh,h,g,f;

	for(i=3;i>=2;i--)
	{
	l=i-1;
	h=scale=0.0;
	if(l>1)
		{
		for(k=1;k<=l;k++)
			scale+=fabs(a[i-1][k-1]);
		if(scale==0.0)		/* skip transformation */
			e[i-1]=a[i-1][l-1];
		else
			{
			for(k=1;k<=l;k++)
				{
				a[i-1][k-1]/=scale;	/* use scaled a's for transformation. */
				h+=a[i-1][k-1]*a[i-1][k-1];	/* form sigma in h. */
				}
			f=a[i-1][l-1];
			g=f>0? -sqrt(h):sqrt(h);
			e[i-1]=scale*g;
			h-=f*g;	/* now h is equation (11.2.4) */
			a[i-1][l-1]=f-g;	/* store u in the ith row of a. */
			f=0.0;
			for(j=1;j<=l;j++)
				{
				a[j-1][i-1]=a[i-1][j-1]/h; /* store u/H in ith column of a. */
				g=0.0;	/* form an element of A.u in g */
				for(k=1;k<=j;k++)
					g+=a[j-1][k-1]*a[i-1][k-1];
				for(k=j+1;k<=l;k++)
					g+=a[k-1][j-1]*a[i-1][k-1];
				e[j-1]=g/h; /* form element of p in temorarliy unused element of e. */
				f+=e[j-1]*a[i-1][j-1];
				}
			hh=f/(h+h);	/* form K, equation (11.2.11) */
			for(j=1;j<=l;j++) /* form q and store in e overwriting p. */
				{
				f=a[i-1][j-1]; /* Note that e[l]=e[i-1] survives */
				e[j-1]=g=e[j-1]-hh*f;
				for(k=1;k<=j;k++) /* reduce a, equation (11.2.13) */
					a[j-1][k-1]-=(f*e[k-1]+g*a[i-1][k-1]);
				}
			}
		}
	else
		e[i-1]=a[i-1][l-1];
	d[i-1]=h;
	}


  /*
  **	For computing eigenvector.
  */
  d[0]=0.0;
  e[0]=0.0;

  for(i=1;i<=3;i++)/* begin accumualting of transfomation matrices */
	{
	l=i-1;
	if(d[i-1]) /* this block skipped when i=1 */
		{
		for(j=1;j<=l;j++)
			{
			g=0.0;
			for(k=1;k<=l;k++) /* use u and u/H stored in a to form P.Q */
				g+=a[i-1][k-1]*a[k-1][j-1];
			for(k=1;k<=l;k++)
				a[k-1][j-1]-=g*a[k-1][i-1];
			}
		}	
	d[i-1]=a[i-1][i-1];
	a[i-1][i-1]=1.0; /* reset row and column of a to identity matrix for next iteration */
	for(j=1;j<=l;j++)
		a[j-1][i-1]=a[i-1][j-1]=0.0;
	}
}



/*
**	QL algo with implicit shift, to determine the eigenvalues and 
**	eigenvectors of a real,symmetric  tridiagonal matrix, or of a real, 
**	symmetric matrix previously reduced by algo tred2.
**	On input , d[1..n] contains the diagonal elements of the tridiagonal
**	matrix. On output, it returns the eigenvalues. The vector e[1..n]
**	inputs the subdiagonal elements of the tridiagonal matrix, with e[1]
**	arbitrary. On output e is destroyed. If the eigenvectors of a 
**	tridiagonal matrix are desired, the matrix z[1..n][1..n] is input
**	as the identity matrix. If the eigenvectors of a matrix that has 
**	been reduced by tred2 are required, then z is input as the matrix 
**	output by tred2. In either case, the kth column of z returns the 
**	normalized eigenvector corresponding to d[k]. 
**
*/
void tqli(double d[3],double e[3],double z[3][3])
{
  int		m,l,iter,i,k;
  double	s,r,p,g,f,dd,c,b;

  for(i=2;i<=3;i++)
	e[i-2]=e[i-1];	/* convenient to renumber the elements of e */
  e[2]=0.0;
  for(l=1;l<=3;l++)
	{
	iter=0;
	do
		{
		for(m=l;m<=2;m++)
			{
			/*
			**	Look for a single small subdiagonal element
			**	to split the matrix.
			*/
			dd=fabs(d[m-1])+fabs(d[m]);
			if(fabs(e[m-1])+dd == dd)
				break;
			}
		if(m!=l)
			{
			if(iter++ == 30)
				{
				fprintf(stderr,"Too many interations in TQLI\n");
				}
			g=(d[l]-d[l-1])/(2.0*e[l-1]); /* form shift */
			r=sqrt((g*g)+1.0);
			g=d[m-1]-d[l-1]+e[l-1]/(g+SIGN(r,g)); /* this is dm-ks */
			s=c=1.0;
			p=0.0;
			for(i=m-1;i>=l;i--)
				{
				/*
				**	A plane rotation as in the original 
				**	QL, followed by Givens rotations to
				**	restore tridiagonal form.
				*/
				f=s*e[i-1];
				b=c*e[i-1];
				if(fabs(f) >= fabs(g))
					{
					c=g/f;
					r=sqrt((c*c)+1.0);
					e[i]=f*r;
					c*=(s=1.0/r);
					}
				else
					{
					s=f/g;
					r=sqrt((s*s)+1.0);
					e[i]=g*r;
					s*=(c=1.0/r);
					}
				g=d[i]-p;
				r=(d[i-1]-g)*s+2.0*c*b;
				p=s*r;
				d[i]=g+p;
				g=c*r-b;
				for(k=1;k<=3;k++)
					{
					/*
					**	Form eigenvectors 
					*/
					f=z[k-1][i];
					z[k-1][i]=s*z[k-1][i-1]+c*f;
					z[k-1][i-1]=c*z[k-1][i-1]-s*f;
					}
				}
			d[l-1]=d[l-1]-p;
			e[l-1]=g;
			e[m-1]=0.0;		
			}
		}while(m != l);
	}
}





