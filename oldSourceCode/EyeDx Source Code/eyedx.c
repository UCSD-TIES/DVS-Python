
		/*********************************************************
		** This program finds eyes in images taken for photoscreening.
		** It then makes measurements on the eye models and produces
		** a (limited) diagnosis and screening decision.
		**
		** Coded by Adam Hoover in June-December '97.
		** Ported to windows in January-February '98. (AH)
		*********************************************************/

#include <stdio.h>
#include <math.h>
#include <time.h>
#include <windows.h>
#include <process.h>
#include "globals.h"

char	*Version="Release Version 1.0";

void EyeDx(char *up_filename,	/* filename of up-image to process; may be empty */
		   char *side_filename,	/* filename of side-image to process; may be empty */
		   int SideOrientation,	/* 0 means left, otherwise right */
		   int FULL_FLAG)		/* flag on outputing full-size annotated images */

{
char	text[250],text1[250],text2[250],savepath[150];
char	BrowserCommand[MAX_FILENAME_CHARS],BrowserPath[MAX_FILENAME_CHARS];
int		up_report,side_report,i;
double	up_lefteye_circles[4],up_righteye_circles[4];
double	side_lefteye_circles[4],side_righteye_circles[4];
int		up_strabismus,side_strabismus;
int		up_red_reflex_lumin,side_red_reflex_lumin;
int		up_left_arr_class,up_right_arr_class;
int		side_left_arr_class,side_right_arr_class;
int		up_left_arr_row,up_left_arr_col;
int		up_right_arr_row,up_right_arr_col;
int		side_left_arr_row,side_left_arr_col;
int		side_right_arr_row,side_right_arr_col,Referral;
FILE	*fpt;
struct tm *newtime;
time_t	aclock;
HANDLE	hFind;
WIN32_FIND_DATA	fd;
HKEY	hKeyHTML,hKeyCommand;
DWORD	Type,Bytes;
char	strab_names[6][20]={"N.A.","NONE","EXOTROPIA","ESOTROPIA",\
					"HYPERTROPIA","NOT LOOKING?"};
char	lumin_names[4][20]={"N.A.","NORMAL","NOT_DETECTED","UNEQUAL"};
char	arr_names[4][20]={"N.A.","NONE","CRESCENT","OTHER"};


		/*********************************************************
		** Process given images.  Result for each image is an eye
		** model (two concentric circles), a strabismus value (0-5),
		** a red reflex luminensce value (0-3), and left & right
		** abnormal red reflex values (0-3).
		*********************************************************/

if (strcmp(up_filename,"") != 0)
  up_report=ProcessImage(up_filename,0,up_lefteye_circles,
	up_righteye_circles,&up_strabismus,&up_red_reflex_lumin,
	&up_left_arr_class,&up_right_arr_class,&up_left_arr_col,
	&up_left_arr_row,&up_right_arr_col,&up_right_arr_row,
	FULL_FLAG,1);
else
  up_report=-1;
if (strcmp(side_filename,"") != 0  &&  SideOrientation == 0)
  side_report=ProcessImage(side_filename,1,side_lefteye_circles,
	side_righteye_circles,&side_strabismus,&side_red_reflex_lumin,
	&side_left_arr_class,&side_right_arr_class,&side_left_arr_col,
	&side_left_arr_row,&side_right_arr_col,&side_right_arr_row,
	FULL_FLAG,1);
else if (strcmp(side_filename,"") != 0  &&  SideOrientation != 0)
  side_report=ProcessImage(side_filename,2,side_lefteye_circles,
	side_righteye_circles,&side_strabismus,&side_red_reflex_lumin,
	&side_left_arr_class,&side_right_arr_class,&side_left_arr_col,
	&side_left_arr_row,&side_right_arr_col,&side_right_arr_row,
	FULL_FLAG,1);
else
  side_report=-1;

		/*********************************************************
		** Make referral decision based on reports
		*********************************************************/

Referral=0;	/* don't refer */
if (up_report >= 0  &&  side_report >= 0)
  {
  if (up_strabismus == 5  ||  side_strabismus == 5  ||
		(up_strabismus == 0  &&  side_strabismus == 0))
    Referral=2;	/* retry */
  if (Referral == 0  &&  (up_strabismus > 1  ||  side_strabismus > 1  ||
		up_red_reflex_lumin == 2  ||  side_red_reflex_lumin == 2  ||
		up_right_arr_class > 1  ||  up_left_arr_class > 1  ||
		side_right_arr_class > 1  ||  side_left_arr_class > 1))
	Referral=1;	/* refer */
  if (Referral == 1  &&  up_strabismus == 1  &&  side_strabismus == 1  &&
	    up_red_reflex_lumin == 1  &&  side_red_reflex_lumin == 1  &&
		up_right_arr_class >= 1  &&  up_right_arr_class <= 2  &&
		up_left_arr_class >= 1  &&  up_left_arr_class <= 2  &&
		side_right_arr_class >= 1  &&  side_right_arr_class <= 2  &&
		side_left_arr_class >= 1  &&  side_left_arr_class <= 2)
	if (DialogBox(hInst,"ID_ONE_YEAR_DIALOG",MainWnd,(DLGPROC)YesNoDlgProc) == IDYES)
	  Referral=0;	/* crescent only, less than one year old = don't refer */
/*
    fprintf(fpt,"Strabismus: <B> %s, %s </B><P>\n",strab_names[up_strabismus],
		strab_names[side_strabismus]);
    fprintf(fpt,"Red Reflex: <B> %s, %s </B><P>\n",
		lumin_names[up_red_reflex_lumin],
		lumin_names[side_red_reflex_lumin]);
    fprintf(fpt,"Abnormal Pupil Area: <B> %s, %s ; %s , %s </B><P>\n",
		arr_names[up_right_arr_class],arr_names[up_left_arr_class],
		arr_names[side_right_arr_class],arr_names[side_left_arr_class]);
*/
  }
else if (up_report >= 0)
  {
  if (up_strabismus == 5  ||  up_strabismus == 0)
    Referral=2;	/* retry */
  if (Referral == 0  &&  (up_strabismus > 1  ||  up_red_reflex_lumin == 2  ||
		up_right_arr_class > 1  ||  up_left_arr_class > 1))
    Referral=1;	/* refer */
  if (Referral == 1  &&  side_strabismus == 1  &&
	    side_red_reflex_lumin == 1  &&
		side_right_arr_class >= 1  &&  side_right_arr_class <= 2  &&
		side_left_arr_class >= 1  &&  side_left_arr_class <= 2)
	if (DialogBox(hInst,"ID_ONE_YEAR_DIALOG",MainWnd,(DLGPROC)YesNoDlgProc) == IDYES)
	  Referral=0;	/* crescent only, less than one year old = don't refer */
/*
    fprintf(fpt,"Strabismus: <B> %s </B><P>\n",strab_names[up_strabismus]);
    fprintf(fpt,"Red Reflex: <B> %s </B><P>\n",lumin_names[up_red_reflex_lumin]);
    fprintf(fpt,"Abnormal Pupil Area: <B> %s, %s </B><P>\n",
		arr_names[up_right_arr_class],arr_names[up_left_arr_class]);
*/
  }
else if (side_report >= 0)
  {
  if (side_strabismus == 5  ||  side_strabismus == 0)
    Referral=2;	/* retry */
  if (Referral == 0  &&  (side_strabismus > 1  ||  side_red_reflex_lumin == 2  ||
		side_right_arr_class > 1  ||  side_left_arr_class > 1))
    Referral=1;	/* refer */
  if (Referral == 1  &&  up_strabismus == 1  &&
	    up_red_reflex_lumin == 1  &&
		up_right_arr_class >= 1  &&  up_right_arr_class <= 2  &&
		up_left_arr_class >= 1  &&  up_left_arr_class <= 2)
	if (DialogBox(hInst,"ID_ONE_YEAR_DIALOG",MainWnd,(DLGPROC)YesNoDlgProc) == IDYES)
	  Referral=0;	/* crescent only, less than one year old = don't refer */
/*
    fprintf(fpt,"Strabismus: <B>%s</B><P>\n",strab_names[side_strabismus]);
    fprintf(fpt,"Red Reflex: <B>%s</B><P>\n",lumin_names[side_red_reflex_lumin]);
    fprintf(fpt,"Abnormal Pupil Area: <B> %s, %s </B><P>\n",
		arr_names[side_right_arr_class],arr_names[side_left_arr_class]);
*/
  }

		/*********************************************************
		** Write graphic and/or letter report
		*********************************************************/

time( &aclock );                 /* Get time in seconds */
newtime = localtime( &aclock );  /* Convert time to struct tm form */
if (/* DisplayGraphics == */1)
  {
  strcpy(savepath,DataPath);
  if (savepath[strlen(savepath)-1] != '\\')
	strcat(savepath,"\\");
  strcat(savepath,"reports");
  if ((hFind=FindFirstFile(savepath,&fd)) == INVALID_HANDLE_VALUE)
    {
    if (!CreateDirectory(savepath,NULL))
	  {
	  MessageBox(NULL,"Saving report","Unable to create reports folder; saving in runtime folder",
		  MB_APPLMODAL | MB_OK);
	  strcpy(savepath,".");
	  }
    }

  FindClose(hFind);

  if (up_report >= 0)
    StripFilename(up_filename,text1);
  if (side_report >= 0)
    StripFilename(side_filename,text2);
  /*
  if (up_report >= 0  &&  side_report >= 0)
    sprintf(text,"%s\\%s-%s.htm",savepath,text1,text2);
  else if (up_report >= 0)
    sprintf(text,"%s\\%s.htm",savepath,text1);
  else
    sprintf(text,"%s\\%s.htm",savepath,text2);
  */
  sprintf(text,"%s\\%s.htm",savepath,report_filename);
  if ((fpt=fopen(text,"w")) == NULL)
    {
    MessageBox(MainWnd,text,"Unable to open report for writing:",MB_APPLMODAL | MB_OK);
    exit(0);
    }
  fprintf(fpt,"<TITLE>EyeDx Photoscreening Results</TITLE>\n");
  fprintf(fpt,"<CENTER><H3>EyeDx Photoscreening Results:  %s</H3><P>\n",report_filename);
  fprintf(fpt,"<H3>Referral recommended: ");
  if (Referral == 1)
	fprintf(fpt,"Yes");
  else if (Referral == 0)
	fprintf(fpt,"No");
  else
	fprintf(fpt,"Image(s) unclear.  Please repeat.");
  fprintf(fpt,"</H3><P>\n<CENTER>\n\n");
  fprintf(fpt,"<TABLE BORDER=3 CELLSPACING=2 CELLPADDING=2>\n");
  fprintf(fpt,"<TR ALIGN=CENTER> ");
  if (up_report >= 0)
    fprintf(fpt,"<TD> Photo ID:  %s (up) ",text1);
  if (side_report >= 0)
    fprintf(fpt,"<TD> Photo ID:  %s (%s) ",text2,
		(SideOrientation == 0 ? "left" : "right"));
  fprintf(fpt,"\n");
    fprintf(fpt,"<TR> ");
  if (up_report >= 0)
    fprintf(fpt,"<TD> <IMG HEIGHT=240 WIDTH=320 SRC=\"..\\Simages\\S%s\">\n",&(up_filename[1]));
  if (side_report >= 0)
    fprintf(fpt,"<TD> <IMG HEIGHT=240 WIDTH=320 SRC=\"..\\Simages\\S%s\">\n",&(side_filename[1]));
  fprintf(fpt,"\n");

  fprintf(fpt,"<TR ALIGN=CENTER> ");
  if (up_report >= 0)
    {
    fprintf(fpt,"<TD> <TABLE BORDER=1 CELLSPACING=2 CELLPADDING=2>\n");
    fprintf(fpt,"  <TR ALIGN=CENTER> <TD> ");
    if (up_report == 0)
      fprintf(fpt,"Please try another photograph.\n");
    else
      {
      fprintf(fpt,"<IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.right_raw.jpg\">\n",text1);
      fprintf(fpt,"  <TD> <IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.left_raw.jpg\">\n",text1);
      }
    fprintf(fpt,"  </TABLE><P>\n");
    }
  if (side_report >= 0)
    {
    fprintf(fpt,"<TD> <TABLE BORDER=1 CELLSPACING=2 CELLPADDING=2>\n");
    fprintf(fpt,"  <TR ALIGN=CENTER> <TD> ");
    if (side_report == 0)
      fprintf(fpt,"Please try another photograph.\n");
    else
      {
      fprintf(fpt,"<IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.right_raw.jpg\">\n",text2);
      fprintf(fpt,"  <TD> <IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.left_raw.jpg\">\n",text2);
      }
    fprintf(fpt,"  </TABLE><P>\n");
    }
  if (1 /* DisplayGraphics == 1 */)
    {
    fprintf(fpt,"<TR ALIGN=CENTER> ");
    if (up_report >= 0)
      {
      fprintf(fpt,"<TD> <TABLE BORDER=1 CELLSPACING=2 CELLPADDING=2>\n");
      fprintf(fpt,"  <TR ALIGN=CENTER> <TD> ");
      if (up_report == 0)
        fprintf(fpt,"Photo inconclusive.\n");
      else
        {
        fprintf(fpt,"<IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.right_eye.jpg\">\n",text1);
        fprintf(fpt,"  <TD> <IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.left_eye.jpg\">\n",text1);
        }
      fprintf(fpt,"  </TABLE><P>\n");
      }
    if (side_report >= 0)
      {
      fprintf(fpt,"<TD> <TABLE BORDER=1 CELLSPACING=2 CELLPADDING=2>\n");
      fprintf(fpt,"  <TR ALIGN=CENTER> <TD> ");
      if (side_report == 0)
        fprintf(fpt,"Photo inconclusive.\n");
      else
        {
        fprintf(fpt,"<IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.right_eye.jpg\">\n",text2);
        fprintf(fpt,"  <TD> <IMG HEIGHT=150 WIDTH=150 SRC=\"..\\eyes\\%s.left_eye.jpg\">\n",text2);
       }
      fprintf(fpt,"  </TABLE><P>\n");
      }
	}
  fprintf(fpt,"</TABLE><P>\n");
  fprintf(fpt,"</CENTER>\n\n");
  fprintf(fpt,"EyeDx screening estimates refractive errors, strabismus and pupil opacities.\n");
  fprintf(fpt,"Please be aware of the tolerances of the system noted in your manual.\n");
  fprintf(fpt,"Display of annotated eyes is for viewing purposes only and is not required\n");
  fprintf(fpt,"by the EyeDx software to provide the referral recommendation.\n");
  fprintf(fpt,"Patent pending.\n");

  fprintf(fpt,"\n<HR>\n\n");
  fprintf(fpt,"<ADDRESS> eyedx@san.rr.com / %s / %s </A></ADDRESS>\n",Version,asctime(newtime));
  fclose(fpt);
  }
if (1 /* AutoReport == 1 */)
  {		/* look in Windows registry for default command to open html file */
  if (RegOpenKeyEx(HKEY_CLASSES_ROOT,".htm",0,KEY_ALL_ACCESS,&hKeyHTML) == ERROR_SUCCESS)
    {
	Bytes=250;
	RegQueryValueEx(hKeyHTML,"",0,&Type,text1,&Bytes);
	strcat(text1,"\\shell\\open\\command");
	if (RegOpenKeyEx(HKEY_CLASSES_ROOT,text1,0,KEY_ALL_ACCESS,&hKeyCommand) == ERROR_SUCCESS)
	  {
	  Bytes=MAX_FILENAME_CHARS;
	  RegQueryValueEx(hKeyCommand,"",0,&Type,BrowserCommand,&Bytes);
	  i=1;
	  while (BrowserCommand[i] != ':'  ||  BrowserCommand[i+1] != '\\')
		i++;
	  strcpy(BrowserPath,&(BrowserCommand[i-1]));
	  i=0;
	  while (i < (int)strlen(BrowserPath)  &&  BrowserPath[i] != ' ')
		i++;
	  while (i > 0  &&  !(BrowserPath[i] == 'e'  ||  BrowserPath[i] == 'E'))
		i--;
	  BrowserPath[i+1]='\0';
	  RegCloseKey(hKeyCommand);
	  i=strlen(BrowserPath)-1;
	  while (BrowserPath[i] != '\\')
		i--;
	  strcpy(BrowserCommand,&(BrowserPath[i+1]));
	  }
	else
	  {
	  strcpy(BrowserPath,"NotGoingToWork");
	  strcpy(BrowserCommand,"CouldNotFindIt");
	  }
	RegCloseKey(hKeyHTML);
    if (_spawnlp(_P_NOWAIT,BrowserPath,BrowserCommand,text,NULL) == -1)
      MessageBox(NULL,"Unable to start web browser.\nPlease display report manually.",
				"Report finished",MB_OK | MB_APPLMODAL);
	}
  else	/* try some default locations... */
	{
    if (_spawnlp(_P_NOWAIT,"C:\\Program Files\\Netscape\\Navigator\\Program\\netscape","netscape",text,NULL) == -1)
      if (_spawnlp(_P_NOWAIT,"C:\\Program Files\\Netscape\\Communicator\\Program\\netscape","netscape",text,NULL) == -1)
        MessageBox(NULL,"Unable to start web browser.\nPlease display report manually.",
				"Report finished",MB_OK | MB_APPLMODAL);
	}
  }
}





		/*********************************************************
		** Takes in a single image (filename).  Produces a report,
		** saying whether or not reliable eye models were found.
		** If they were found, then the eye models, and classif.s
		** for strabisumus, red reflex lumin, and any abnormal
		** red reflex areas, are returned.  This routine also writes
		** out annotated image files.
		*********************************************************/

int ProcessImage(char	*filename,		/* input filename */
				int	OrientationFlag,	/* input:  0 => up, 1 => left, 2 => right */
				double	lefteye_circles[4],	/* output: for coord system aligning */
				double	righteye_circles[4],	/* output: for coord system aligning */
				int	*strabismus,		/* output:  flag has 0-3 for value */
				int	*red_reflex_lumin,	/* output:  flag has 0-2 for value */
				int	*left_arr_class,	/* output:  flag has 0-2 for value */
				int	*right_arr_class,	/* output:  flag has 0-2 for value */
				int	*left_arr_col,		/* output:  X-centroid of left-eye ARR */
				int	*left_arr_row,		/* output:  Y-centroid of left-eye ARR */
				int	*right_arr_col,		/* output:  X-centroid of right-eye ARR */
				int	*right_arr_row,		/* output:  Y-centroid of right-eye ARR */
				int	FullImagesFlag,		/* input:  write out full-size images? */
				int	RawEyesFlag)		/* input:  write out raw zoomed eyes? */

{
char		text[300],savepath[300],savefile[300];
HANDLE		hFind;
WIN32_FIND_DATA	fd;
HDC			hDC;
HBRUSH		DrawBrush;
RECT		outline;
unsigned char	*Raw,*threshimage,*dispimage;
int			i,ROWS,COLS,temp;
int			*points,total_points,one,two,total_circles;
double		**red_circles,*red_spacings;
double		*red_gradients,*red_residuals;
double		**white_circles,*white_spacings;
double		*white_gradients,*white_residuals;
double		*white_red_radii;
int			corneal_reflex_indices1[400],total_cr1;
int			corneal_reflex_indices2[400],total_cr2;
int			abnormal_red_reflex_indices1[4000],total_arr1;
int			abnormal_red_reflex_indices2[4000],total_arr2;
double		pupil_to_pupil_dist,pupils_horizon_angle,temp_d;
int			lefteye_cr_point,righteye_cr_point,diff;
int			red_reflex_avg1[3],red_reflex_avg2[3];

		/*********************************************************
		** All reports start out not available
		*********************************************************/

(*strabismus)=NOT_AVAILABLE;
(*red_reflex_lumin)=NOT_AVAILABLE;
(*left_arr_class)=NOT_AVAILABLE;
(*right_arr_class)=NOT_AVAILABLE;

		/*********************************************************
		** Get memory dynamically -- it's a bunch
		*********************************************************/

if ((points=(int *)calloc(MAX_BRIGHTS,sizeof(int))) == NULL  ||
    (red_circles=(double **)calloc(MAX_BRIGHTS,sizeof(double *))) == NULL  ||
    (red_spacings=(double *)calloc(MAX_BRIGHTS,sizeof(double))) == NULL  ||
    (red_gradients=(double *)calloc(MAX_BRIGHTS,sizeof(double))) == NULL  ||
    (red_residuals=(double *)calloc(MAX_BRIGHTS,sizeof(double))) == NULL  ||
    (white_circles=(double **)calloc(MAX_BRIGHTS,sizeof(double *))) == NULL  ||
    (white_spacings=(double *)calloc(MAX_BRIGHTS,sizeof(double))) == NULL  ||
    (white_gradients=(double *)calloc(MAX_BRIGHTS,sizeof(double))) == NULL  ||
    (white_residuals=(double *)calloc(MAX_BRIGHTS,sizeof(double))) == NULL  ||
    (white_red_radii=(double *)calloc(MAX_BRIGHTS,sizeof(double))) == NULL)
  {
  MessageBox(MainWnd,"Unable to allocate memory","ProcessImage()",MB_OK | MB_APPLMODAL);
  exit(0);
  }
for (i=0; i<MAX_BRIGHTS; i++)
  {
  red_circles[i]=(double *)calloc(3,sizeof(double));
  white_circles[i]=(double *)calloc(3,sizeof(double));
  }

		/*********************************************************
		** Get image ready to process -- load used to happen here,
		** but with GUI interface, just copy for display
		*********************************************************/

StripFilename(filename,text);
if (OrientationFlag == 0)
  {
  Raw=up_image;
  ROWS=UP_ROWS;
  COLS=UP_COLS;
  }
else
  {
  Raw=side_image;
  ROWS=SIDE_ROWS;
  COLS=SIDE_COLS;
  }
threshimage=(unsigned char *)calloc(ROWS*COLS,1);
if (DisplayGraphics == 1)
  dispimage=(unsigned char *)calloc(ROWS*COLS*3,1);
else
  dispimage=NULL;
if (threshimage == NULL  ||  (DisplayGraphics == 1  &&  dispimage == NULL))
  {
  MessageBox(MainWnd,"Unable to allocate memory 2","ProcessImage()",MB_OK | MB_APPLMODAL);
  exit(0);
  }
if (DisplayGraphics == 1)
  {
  for (i=0; i<ROWS*COLS*3; i++)
    dispimage[i]=Raw[i]/2;
  MakeDisplayImage(dispimage,ROWS,COLS,0);
  PaintImage();
  }
sprintf(savepath,"Analyzing image %s ...",text);
hDC=GetDC(MainWnd);
outline.top=0; outline.bottom=25;
outline.left=0; outline.right=385;
DrawBrush=CreateSolidBrush(RGB(255,255,255));
FillRect(hDC,&outline,DrawBrush);
DeleteObject(DrawBrush);
TextOut(hDC,0,0,savepath,strlen(savepath));
ReleaseDC(MainWnd,hDC);

		/*********************************************************
		** Find eye models -- corneal reflexes (CRs) modeled by
		** blobs, followed by pupil and iris boundaries modeled
		** by concentric circles.
		*********************************************************/

i=FindBrightSpots(Raw,ROWS,COLS,threshimage,&total_points,points);
if (i == 0)
  {
  MessageBox(MainWnd,"Please try another photograph.","Image too dark or too bright",MB_OK | MB_APPLMODAL);
  return(0);	/* too many bright spots */
  }
FindCircles(Raw,ROWS,COLS,dispimage,points,total_points,
        red_circles,red_gradients,red_spacings,red_residuals,white_circles,
        white_red_radii,white_gradients,white_spacings,white_residuals);
total_circles=BestTwoCircles(points,COLS,total_points,red_circles,red_gradients,
        red_spacings,red_residuals,white_circles,white_red_radii,
        white_gradients,white_spacings,white_residuals,&one,&two);
if (total_circles < 2)
  {
  /* if (AutoReport == 0) */
    MessageBox(MainWnd,"Please try another photograph.","Photo inconclusive",MB_OK | MB_APPLMODAL);
  return(0);	/* no eyes, no report */
  }

if (DisplayGraphics == 1)
  {
  for (i=0; i<ROWS*COLS*3; i++)
    dispimage[i]=Raw[i]/2;
  MakeDisplayImage(dispimage,ROWS,COLS,0);
  PaintImage();
  FlashCircles(dispimage,ROWS,COLS,
	  red_circles[one][2] >= 0.0 ? red_circles[one] : white_circles[one],
	  red_circles[two][2] >= 0.0 ? red_circles[two] : white_circles[two]);
  for (i=0; i<ROWS*COLS*3; i++)
    dispimage[i]=Raw[i];
  }

		/*********************************************************
		** Test resulting eye model pair.  Red circles must be
		** minimum strength, minimum spacing (of points in circle).
		** Eyes must not be overlapping, and must have tolerable
		** angle of inclination with user-given orientation.
		*********************************************************/

/* printf("red circle tests %lf,%lf %lf,%lf ",
	red_residuals[one],red_spacings[one],
	red_residuals[two],red_spacings[two]); */
//if (red_residuals[one] >= MAX_EYE_RESID  ||  red_spacings[one] > MAX_EYE_SPACE  ||
//	red_residuals[two] >= MAX_EYE_RESID  ||  red_spacings[two] > MAX_EYE_SPACE )
//  {
//  if (AutoReport == 0)
//    MessageBox(MainWnd,"Please try another photograph.","Photo inconclusive",MB_OK | MB_APPLMODAL);
//  return(0);	/* not good circle fits */
//  }
if (red_residuals[one] > 0.0)
  {
  lefteye_circles[0]=red_circles[one][0];
  lefteye_circles[1]=red_circles[one][1];
  lefteye_circles[2]=red_circles[one][2];
  lefteye_circles[3]=white_red_radii[one];
  }
else
  {
  lefteye_circles[0]=white_circles[one][0];
  lefteye_circles[1]=white_circles[one][1];
  lefteye_circles[2]=-1.0;
  lefteye_circles[3]=white_circles[one][2];
  }
lefteye_cr_point=points[one];
if (red_residuals[two] > 0.0)
  {
  righteye_circles[0]=red_circles[two][0];
  righteye_circles[1]=red_circles[two][1];
  righteye_circles[2]=red_circles[two][2];
  righteye_circles[3]=white_red_radii[two];
  }
else
  {
  righteye_circles[0]=white_circles[two][0];
  righteye_circles[1]=white_circles[two][1];
  righteye_circles[2]=-1.0;
  righteye_circles[3]=white_circles[two][2];
  }
righteye_cr_point=points[two];
pupil_to_pupil_dist=sqrt(SQR(lefteye_circles[0]-righteye_circles[0])+
	SQR(lefteye_circles[1]-righteye_circles[1]));
if (OrientationFlag == 0)	/* up-image */
  pupils_horizon_angle=atan2(fabs(lefteye_circles[1]-righteye_circles[1]),
	fabs(lefteye_circles[0]-righteye_circles[0]));
else				/* side image, right or left */
  pupils_horizon_angle=atan2(fabs(lefteye_circles[0]-righteye_circles[0]),
	fabs(lefteye_circles[1]-righteye_circles[1]));
/* printf("\neye model tests %lf-%lf-%lf  %lf  ", 
	pupil_to_pupil_dist,lefteye_circles[3],righteye_circles[3],
	pupils_horizon_angle*180/M_PI); */
if (pupil_to_pupil_dist < lefteye_circles[3]  ||
	pupil_to_pupil_dist < righteye_circles[3]  ||
	pupils_horizon_angle > 30.0*M_PI/180.0)
  {
  if (DisplayGraphics == 1)
    MessageBox(MainWnd,"Please try another photograph.","Eye orientation not consistent",MB_OK | MB_APPLMODAL);
  return(0);			/* reliable eye models not found */
  }
if (lefteye_circles[2] <= 7.5  ||  righteye_circles[2] <= 7.5)
  {
  if (DisplayGraphics == 1)
    MessageBox(MainWnd,"Please try another photograph.","Pupils need to be more dilated.",MB_OK | MB_APPLMODAL);
  return(0);			/* reliable eye models not found */
  }

		/*********************************************************
		** Switch left and right eye models if not in proper place
		*********************************************************/

if ((OrientationFlag == 0  &&  lefteye_circles[0] < righteye_circles[0])  ||
      (OrientationFlag == 1  &&  lefteye_circles[1] > righteye_circles[1])  ||
      (OrientationFlag == 2  &&  lefteye_circles[1] < righteye_circles[1]))
  {	/* switch left and right eye to proper places */
  for (i=0; i<4; i++)
    {
    temp_d=lefteye_circles[i];
    lefteye_circles[i]=righteye_circles[i];
    righteye_circles[i]=temp_d;
    }
  temp=lefteye_cr_point;
  lefteye_cr_point=righteye_cr_point;
  righteye_cr_point=temp;
  }

		/*********************************************************
		** Classify pupil interior.  This finds any abnormal areas
		** in the red reflexes, and classifies them.  It also
		** classifies any possible strabismus, and decides if
		** the red reflexes have equal luminensce.
		*********************************************************/

ClassifyPupilInterior(Raw,threshimage,dispimage,ROWS,COLS,lefteye_circles,
	lefteye_cr_point,corneal_reflex_indices1,&total_cr1,
	abnormal_red_reflex_indices1,&total_arr1,red_reflex_avg1,
	left_arr_class,left_arr_col,left_arr_row);
ClassifyPupilInterior(Raw,threshimage,dispimage,ROWS,COLS,righteye_circles,
	righteye_cr_point,corneal_reflex_indices2,&total_cr2,
	abnormal_red_reflex_indices2,&total_arr2,red_reflex_avg2,
	right_arr_class,right_arr_col,right_arr_row);
ClassifyPupilAlignment(lefteye_circles,corneal_reflex_indices1,total_cr1,
	righteye_circles,corneal_reflex_indices2,total_cr2,
	COLS,OrientationFlag,strabismus);
hDC=GetDC(MainWnd);
if (lefteye_circles[2] > 0.0  &&  righteye_circles[2] > 0.0)
  {
  diff=(abs(red_reflex_avg1[0]-red_reflex_avg2[0])+
	  abs(red_reflex_avg1[1]-red_reflex_avg2[1])+
	  abs(red_reflex_avg1[2]-red_reflex_avg2[2]))/3;
  if (diff <= MAX_LUMIN_DIFF)
	{
//	TextOut(hDC,0,0,"RR NORMAL",strlen("RR NORMAL"));
    *red_reflex_lumin=NORMAL;
	}
  else
	{
//	TextOut(hDC,0,0,"RR UNEQUAL",strlen("RR UNEQUAL"));
    *red_reflex_lumin=UNEQUAL_LUMIN;
	}
  }
else
  {
//  TextOut(hDC,0,0,"RR NOT DETECTED",strlen("RR NOT DETECTED"));
  *red_reflex_lumin=NOT_DETECTED;
  }
ReleaseDC(MainWnd,hDC);

		/*********************************************************
		** Write out images for report
		*********************************************************/

sprintf(savepath,"%s%sSimages",DataPath,
		(DataPath[strlen(DataPath)-1] == '\\' ? "" : "\\"));
if ((hFind=FindFirstFile(savepath,&fd)) == INVALID_HANDLE_VALUE)
  {
  if (!CreateDirectory(savepath,NULL))
    {
	MessageBox(NULL,"Saving results","Unable to create Simages folder; saving in runtime folder",
		  MB_APPLMODAL | MB_OK);
	strcpy(savepath,".\\");
	}
  }
FindClose(hFind);
sprintf(savefile,"%s\\S%s",savepath,&(filename[1]));
SaveImage(savefile,Raw,ROWS,COLS,4);

sprintf(savepath,"%s%seyes",DataPath,
		(DataPath[strlen(DataPath)-1] == '\\' ? "" : "\\"));
if ((hFind=FindFirstFile(savepath,&fd)) == INVALID_HANDLE_VALUE)
  {
  if (!CreateDirectory(savepath,NULL))
    {
	MessageBox(NULL,"Saving results","Unable to create eyes folder; saving in runtime folder",
		  MB_APPLMODAL | MB_OK);
	strcpy(savepath,".\\");
	}
  }
FindClose(hFind);
strcat(savepath,"\\"); strcat(savepath,text);
WriteImage(savepath,Raw,ROWS,COLS,
	lefteye_circles,corneal_reflex_indices1,total_cr1,
	abnormal_red_reflex_indices1,total_arr1,*left_arr_class,
	righteye_circles,corneal_reflex_indices2,total_cr2,
	abnormal_red_reflex_indices2,total_arr2,*right_arr_class,
	OrientationFlag,FullImagesFlag,RawEyesFlag,1);

		/*********************************************************
		** Free up dynamic memory
		*********************************************************/

for (i=0; i<MAX_BRIGHTS; i++)
  {
  free(red_circles[i]);
  free(white_circles[i]);
  }
free(points);
free(red_circles);
free(red_spacings);
free(red_gradients);
free(red_residuals);
free(white_circles);
free(white_spacings);
free(white_gradients);
free(white_residuals);
free(white_red_radii);

free(threshimage);
if (DisplayGraphics == 1)
  free(dispimage);
return(1);
}






