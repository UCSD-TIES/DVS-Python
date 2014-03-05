
	/*******************************************************************
	** Some routines which deal with files (reading, writing, etc.)
	*******************************************************************/

#define HAVE_BOOLEAN

#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <jpeglib.h>
#include "resource.h"
#include "globals.h"


	/*******************************************************************
	** Takes in a complete filename (may include paths, prefix, and any
	** number of suffixes) and returns the stripped prefix (without any
	** paths or suffixes attached).
	*******************************************************************/

void StripFilename(char *input,char *stripped)

{
int		c; 

c=strlen(input)-1;
while (c >= 0  &&  input[c] != '/')
  c--;
if (c >= 0)
  strcpy(stripped,&(input[c+1]));
else
  strcpy(stripped,input);
c=0;
while (c < (int)strlen(stripped)  &&  stripped[c] != '.')
  c++;
if (c < (int)strlen(stripped))
  stripped[c]='\0';
}



	/*******************************************************************
	** Read a photo-screening image from a file.  Returns a 1 after a
	** successful read, 0 otherwise.
	*******************************************************************/

int ReadImage(char			*filename,			/* complete name of image to read */
			  unsigned char	**raw,				/* image data, returned */
			  int			*ROWS,int *COLS)	/* size of image, returned */

{
FILE							*fpt;
int								i,r,BYTES;
char							text[30];
struct jpeg_decompress_struct	cinfo;
struct jpeg_error_mgr			jerr;
JSAMPARRAY						buffer;
HDC								hDC;
char							LoadText[50];

if ((fpt=fopen(filename,"rb")) == NULL)
  {
  MessageBox(MainWnd,filename,"Unable to open file:",MB_APPLMODAL | MB_OK);
  return(0);
  }

		/* see if in jpeg format */
text[0]=getc(fpt); text[1]=getc(fpt);
if (text[0] == -1  &&  text[1] == -40)
  {		/* is in jpeg format -- start over and read in */
  fclose(fpt);
  fpt=fopen(filename,"rb");
  cinfo.err = jpeg_std_error(&jerr);
  jpeg_create_decompress(&cinfo);
  jpeg_stdio_src(&cinfo, fpt);
  jpeg_read_header(&cinfo, TRUE);
  jpeg_start_decompress(&cinfo);
  *COLS=cinfo.output_width;
  *ROWS=cinfo.output_height;
  if ((*ROWS != 960  ||  *COLS != 1280)  &&  strcmp(filename,"EyeDxBg.jpg") != 0)
    if (DialogBox(hInst,"ID_ILLLOAD_DIALOG",MainWnd,(DLGPROC)ContinueDlgProc) == ID_CANCEL)
	  {
	  (*ROWS)=(*COLS)=0;
	  return(0);
	  }
  if ((*raw=(unsigned char *)calloc((*ROWS)*(*COLS)*3,1)) == NULL)
    {
    MessageBox(MainWnd,"Unable to allocate memory","ReadImage()",MB_APPLMODAL | MB_OK);
	(*ROWS)=(*COLS)=0;
	return(0);
    }
  if (cinfo.output_components != 3)
    {
    MessageBox(MainWnd,filename,"File is not RGB jpeg format",MB_APPLMODAL | MB_OK);
	free(*raw);
	*raw=NULL;
	(*ROWS)=(*COLS)=0;
	return(0);
    }
  r=0;
  buffer = (*cinfo.mem->alloc_sarray)((j_common_ptr) &cinfo, JPOOL_IMAGE, (*COLS)*3, 1);
  hDC=GetDC(MainWnd);
  sprintf(LoadText,"Loading %s ...",filename);
  while (r < *ROWS)
    {
	if (r%50 == 0)
	  {
	  strcat(LoadText,".");
	  TextOut(hDC,0,0,LoadText,strlen(LoadText));
	  }
    jpeg_read_scanlines(&cinfo, buffer, 1);
    for (i=0; i<(*COLS)*3; i++)
      (*raw)[r*(*COLS)*3+i]=(unsigned char)buffer[0][i];
    r++;
    }
  ReleaseDC(MainWnd,hDC);
  jpeg_finish_decompress(&cinfo);
  jpeg_destroy_decompress(&cinfo);
  fclose(fpt);
  return(1);
  }
fclose(fpt);
fpt=fopen(filename,"rb");	/* try again, in ppm format */
text[0]=getc(fpt); text[1]=getc(fpt); text[2]=getc(fpt); text[2]='\0';
if (strcmp(text,"P6") == 0)
  {
  (*ROWS)=(*COLS)=BYTES=-1;
  while (BYTES == -1)
    {
    fscanf(fpt,"%s",text);
    if (text[0] == '#') /* comment -- ignore */
      {
      while ((text[0]=fgetc(fpt)) != '\n');
      continue;
      }
    if ((*COLS) == -1)
      (*COLS)=atoi(text);
    else if ((*ROWS) == -1)
      (*ROWS)=atoi(text);
    else
      BYTES=atoi(text);
    }  
  if (BYTES != 255)
    {
    MessageBox(MainWnd,filename,"File is not 8-bit ppm format",MB_APPLMODAL | MB_OK);
	(*ROWS)=(*COLS)=0;
	return(0);
    }
  if (((*raw)=(unsigned char *)calloc((*ROWS)*(*COLS)*3,1)) == NULL)
    {
    MessageBox(MainWnd,"Unable to allocate memory (raw)","ReadImage()",MB_APPLMODAL | MB_OK);
	(*ROWS)=(*COLS)=0;
	return(0);
    }
  text[0]=getc(fpt);
  fread(*raw,1,3*(*ROWS)*(*COLS),fpt);
  fclose(fpt);
  return(1);
  }
fclose(fpt);
MessageBox(MainWnd,filename,"Unknown image format",MB_APPLMODAL | MB_OK);
return(0);
}


	/*******************************************************************
	** Write an annotated image to a file.  Returns a 1 after a
	** successful write, 0 otherwise.
	*******************************************************************/

int WriteImage(	char			*filename,	/* path and prefix of image(s) to write */
				unsigned char	*raw,		/* original image data */
											/* bytes are ordered bgr0,bgr1,bgr2,... */
				int				ROWS,int COLS,	/* size of image */
				double			left_circles[4],		/* 2 concentric circles */
				int				*left_corneal_reflex_indices,	/* image indices of CR */
				int				left_CR_size,			/* count of CR indices */
				int				*left_abnormal_red_reflex_indices, /* image indices of ARR */
				int				left_ARR_size,			/* count of ARR indices */
				int				left_ARR_class,			/* color to code blob */
				double			right_circles[4],		/* 2 concentric circles */
				int				*right_corneal_reflex_indices,	/* image indices of CR */
				int				right_CR_size,			/* count of CR indices */
				int				*right_abnormal_red_reflex_indices, /* image indices of ARR */
				int				right_ARR_size,			/* count of ARR indices */
				int				right_ARR_class,		/* color to code blob */
				int				OrientationFlag,	/* 0=>up, 1=>left, 2=>right */
				int				FullImageFlag,	/* 0 => don't write, 1 => do write */
												/* 2 => anonymize (grey all but eyes) */
				int				RawEyesFlag,	/* 0 => don't write, 1 => do write */
				int				EyesFlag)		/* 0 => don't write, 1 => do write */

{
FILE						*fpt;
char						outfile[100],SaveText[50];
int							*circle_points,total_points;
int							r,c,e,i,r2,c2,x,y,EYE_ROWS,EYE_COLS,index;
unsigned char				*eye_image,*annotated;
struct jpeg_compress_struct	cinfo;
struct jpeg_error_mgr		jerr;
JSAMPROW					row_pointer[1];
HDC							hDC;


			/* annotate image with model */
if ((annotated=(unsigned char *)calloc(ROWS*COLS*3,1)) == NULL)
  {
  MessageBox(MainWnd,"Unable to allocate memory","WriteImage()",MB_APPLMODAL | MB_OK);
  return(0);
  }
for (i=0; i<ROWS*COLS*3; i++)
  annotated[i]=raw[i];
circle_points=(int *)calloc((int)((double)MaxIrisRad*8.0),sizeof(int));
for (e=0; e<2; e++)
  {
  if (e == 0  &&  left_circles[2] > 0.0)
    MakeCircleIndices(left_circles[0],left_circles[1],
	left_circles[2],ROWS,COLS,circle_points,&total_points);
  else if (e == 1  &&  right_circles[2] > 0.0)
    MakeCircleIndices(right_circles[0],right_circles[1],
	right_circles[2],ROWS,COLS,circle_points,&total_points);
  else
    total_points=0;
  for (i=0; i<total_points; i++)
    {				/* green */
    annotated[circle_points[i]*3+0]=0;
    annotated[circle_points[i]*3+1]=255;
    annotated[circle_points[i]*3+2]=0;
    }
  if (e == 0  &&  left_circles[3] > 0.0)
    MakeCircleIndices(left_circles[0],left_circles[1],
	left_circles[3],ROWS,COLS,circle_points,&total_points);
  else if (e == 1  &&  right_circles[3] > 0.0)
    MakeCircleIndices(right_circles[0],right_circles[1],
	right_circles[3],ROWS,COLS,circle_points,&total_points);
  else
    total_points=0;
  for (i=0; i<total_points; i++)
    {				/* yellow */
    annotated[circle_points[i]*3+0]=255;
    annotated[circle_points[i]*3+1]=255;
    annotated[circle_points[i]*3+2]=0;
    }
  }
free(circle_points);
for (i=0; i<left_CR_size; i++)
  {
  annotated[left_corneal_reflex_indices[i]*3+0]=0;
  annotated[left_corneal_reflex_indices[i]*3+1]=0;
  annotated[left_corneal_reflex_indices[i]*3+2]=255;
  }
for (i=0; i<right_CR_size; i++)
  {
  annotated[right_corneal_reflex_indices[i]*3+0]=0;
  annotated[right_corneal_reflex_indices[i]*3+1]=0;
  annotated[right_corneal_reflex_indices[i]*3+2]=255;
  }
for (i=0; i<left_ARR_size; i++)
  {
  annotated[left_abnormal_red_reflex_indices[i]*3+2]=255;
  if (left_ARR_class == CRESCENT)
    {
    annotated[left_abnormal_red_reflex_indices[i]*3+1]=255;
    annotated[left_abnormal_red_reflex_indices[i]*3+0]=0;
    }
  else
    {
    annotated[left_abnormal_red_reflex_indices[i]*3+1]=175;
    annotated[left_abnormal_red_reflex_indices[i]*3+0]=175;
    }
  }
for (i=0; i<right_ARR_size; i++)
  {
  annotated[right_abnormal_red_reflex_indices[i]*3+2]=255;
  if (right_ARR_class == CRESCENT)
    {
    annotated[right_abnormal_red_reflex_indices[i]*3+1]=255;
    annotated[right_abnormal_red_reflex_indices[i]*3+0]=0;
    }
  else
    {
    annotated[right_abnormal_red_reflex_indices[i]*3+1]=175;
    annotated[right_abnormal_red_reflex_indices[i]*3+0]=175;
    }
  }
			/* save raw (unmarked) and annotated eye images */
if (RawEyesFlag  ||  EyesFlag)
  {
  EYE_ROWS=EYE_COLS=(int)((double)MaxIrisRad*2.0);
  eye_image=(unsigned char *)calloc(EYE_ROWS*EYE_COLS*3,1);
  for (i=0; i<4; i++)
    {
    if (i < 2  &&  !RawEyesFlag)
      continue;
    if (i > 1  &&  !EyesFlag)
      continue;
    if (i%2 == 0)
      {
      y=(int)left_circles[1];
      x=(int)left_circles[0];
      }
    else
      {
      y=(int)right_circles[1];
      x=(int)right_circles[0];
      }
    if (i == 0)
      sprintf(outfile,"%s.left_raw.jpg",filename);
    else if (i == 1)
      sprintf(outfile,"%s.right_raw.jpg",filename);
    else if (i == 2)
      sprintf(outfile,"%s.left_eye.jpg",filename);
    else if (i == 3)
      sprintf(outfile,"%s.right_eye.jpg",filename);
    for (r=y-EYE_ROWS/2,r2=0; r<y+EYE_ROWS/2; r++,r2++)
      for (c=x-EYE_COLS/2,c2=0; c<x+EYE_COLS/2; c++,c2++)
        {
		if (OrientationFlag == 0)
		  index=r2*EYE_COLS+c2;
		else if (OrientationFlag == 1)		/* rotate CW */
		  index=c2*EYE_COLS+EYE_ROWS-1-r2;
		else /* OrientationFlag == 2 */		/* rotate CCW */
		  index=(EYE_COLS-1-c2)*EYE_COLS+r2;
		if (r < 0  ||  r >= ROWS  ||  c < 0  ||  c >= COLS)
          {
          eye_image[index*3+0]=0;
          eye_image[index*3+1]=1;
          eye_image[index*3+2]=2;
          }
        else if (i < 2)
          {
          eye_image[index*3+0]=raw[(r*COLS+c)*3+0];
          eye_image[index*3+1]=raw[(r*COLS+c)*3+1];
          eye_image[index*3+2]=raw[(r*COLS+c)*3+2];
          }
        else
          {
          eye_image[index*3+0]=annotated[(r*COLS+c)*3+0];
          eye_image[index*3+1]=annotated[(r*COLS+c)*3+1];
          eye_image[index*3+2]=annotated[(r*COLS+c)*3+2];
          }
        }
    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_compress(&cinfo);
    if ((fpt=fopen(outfile,"wb")) == NULL)
      {
	  MessageBox(MainWnd,outfile,"Unable to open for writing:",MB_APPLMODAL | MB_OK);
      return(0);
      }
    jpeg_stdio_dest(&cinfo, fpt);
    cinfo.image_width = EYE_COLS;
    cinfo.image_height = EYE_ROWS;
    cinfo.input_components = 3;
    cinfo.in_color_space = JCS_RGB;
    jpeg_set_defaults(&cinfo);
    jpeg_set_quality(&cinfo, 100, TRUE );
    jpeg_start_compress(&cinfo, TRUE);
	hDC=GetDC(MainWnd);
	sprintf(SaveText,"Writing %s ...",outfile);
    while (cinfo.next_scanline < cinfo.image_height)
      {
	  if ((cinfo.next_scanline)%50 == 0)
		{
	    strcat(SaveText,".");
	    TextOut(hDC,0,0,SaveText,strlen(SaveText));
		}
      row_pointer[0] = & eye_image[cinfo.next_scanline * EYE_COLS*3];
      (void) jpeg_write_scanlines(&cinfo, row_pointer, 1);
      }
	ReleaseDC(MainWnd,hDC);
    jpeg_finish_compress(&cinfo);
    fclose(fpt);
    jpeg_destroy_compress(&cinfo);
    }
  free(eye_image);
  }
				/* save full annotated image */
if (FullImageFlag)
  {
  cinfo.err = jpeg_std_error(&jerr);
  jpeg_create_compress(&cinfo);
  sprintf(outfile,"%s.annotated.jpg",filename);
  if ((fpt=fopen(outfile,"wb")) == NULL)
    {
    MessageBox(MainWnd,outfile,"Unable to open for writing:",MB_APPLMODAL | MB_OK);
    return(0);
    }
  jpeg_stdio_dest(&cinfo, fpt);
  cinfo.image_width = COLS;
  cinfo.image_height = ROWS;
  cinfo.input_components = 3;
  cinfo.in_color_space = JCS_RGB;
  jpeg_set_defaults(&cinfo);
  jpeg_set_quality(&cinfo, 100, TRUE );
  jpeg_start_compress(&cinfo, TRUE);
  hDC=GetDC(MainWnd);
  sprintf(SaveText,"Writing %s ...",outfile);
  while (cinfo.next_scanline < cinfo.image_height)
    {
	if ((cinfo.next_scanline)%50 == 0)
	  {
	  strcat(SaveText,".");
	  TextOut(hDC,0,0,SaveText,strlen(SaveText));
	  }
    row_pointer[0] = & annotated[cinfo.next_scanline * COLS*3];
    (void) jpeg_write_scanlines(&cinfo, row_pointer, 1);
    }
  ReleaseDC(MainWnd,hDC);
  jpeg_finish_compress(&cinfo);
  fclose(fpt);
  jpeg_destroy_compress(&cinfo);
  }

free(annotated);
return(1);
}



	/*******************************************************************
	** Saves an image to a file in jpeg format.  Returns a 1 after a
	** successful save, 0 otherwise.
	*******************************************************************/

int SaveImage(char			*filename,		/* complete name of image to save */
			  unsigned char	*image,			/* image data, RGB L->R T->D format */
			  int			ROWS,int COLS,	/* size of image */
			  int			DownSample)		/* factor to downsample by (1 is full size) */

{
FILE							*fpt;
struct jpeg_compress_struct		cinfo;
struct jpeg_error_mgr			jerr;
JSAMPROW						row_pointer[1];
HDC								hDC;
char							SaveText[50];
unsigned char					*save_image;
int								r,c;

if (DownSample == 1)
  save_image=image;
else
  {
  save_image=(unsigned char *)calloc(ROWS/DownSample*COLS/DownSample*3,1);
  for (r=0; r<ROWS; r+=DownSample)
	for (c=0; c<COLS; c+=DownSample)
	  {
	  save_image[(r/DownSample*COLS/DownSample+c/DownSample)*3+0]=image[(r*COLS+c)*3+0];
	  save_image[(r/DownSample*COLS/DownSample+c/DownSample)*3+1]=image[(r*COLS+c)*3+1];
	  save_image[(r/DownSample*COLS/DownSample+c/DownSample)*3+2]=image[(r*COLS+c)*3+2];
	  }
  }
cinfo.err = jpeg_std_error(&jerr);
jpeg_create_compress(&cinfo);
if ((fpt=fopen(filename,"wb")) == NULL)
  {
  MessageBox(MainWnd,filename,"Unable to open for writing:",MB_APPLMODAL | MB_OK);
  return(0);
  }
jpeg_stdio_dest(&cinfo, fpt);
cinfo.image_width = COLS/DownSample;
cinfo.image_height = ROWS/DownSample;
cinfo.input_components = 3;
cinfo.in_color_space = JCS_RGB;
jpeg_set_defaults(&cinfo);
jpeg_set_quality(&cinfo, 100, TRUE );
jpeg_start_compress(&cinfo, TRUE);
hDC=GetDC(MainWnd);
sprintf(SaveText,"Writing %s ...",filename);
while (cinfo.next_scanline < cinfo.image_height)
  {
  if ((cinfo.next_scanline)%50 == 0)
    {
    strcat(SaveText,".");
    TextOut(hDC,0,0,SaveText,strlen(SaveText));
	}
  row_pointer[0] = & save_image[cinfo.next_scanline*(COLS/DownSample)*3];
  (void) jpeg_write_scanlines(&cinfo, row_pointer, 1);
  }
ReleaseDC(MainWnd,hDC);
jpeg_finish_compress(&cinfo);
fclose(fpt);
jpeg_destroy_compress(&cinfo);
if (DownSample != 1)
  free(save_image);
}


