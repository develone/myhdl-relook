#include "pnmio.h"
#include <stdlib.h>
#include <stdio.h>
#include "lifting.h"
 
int main()

{
  FILE *outptr;
  int ncols, nrows;
  
  ncols = 64;
  nrows = 64;
  unsigned char *img1;
  char *tt; 
  int *buf_red;
  int *wptr,*red_s_ptr,*alt;
  img1 = pgmReadFile("red.pgm", NULL, &ncols, &nrows);
  int *fwd_inv;	

	int i,j;
  buf_red = ( int *)malloc(sizeof( int)* nrows*ncols*2);
  red_s_ptr = buf_red; 
   

  
   
  for(i=0;i<ncols*nrows;i++) {
    buf_red[i] = *img1;
    //printf("img1 %x %d %d\n",img1,buf_red[i], i);
    img1++;
  }
  fwd_inv = (int *)malloc(1);
  *fwd_inv = 0;
    buf_red = red_s_ptr;
		wptr = buf_red;
		alt = &buf_red[ncols*nrows];
    lifting(ncols,wptr,alt,fwd_inv);
    
    outptr = fopen("dwt.bin","wb");
    if (!outptr)
	  {
 	    printf("Unle to open file!");
	    return 1;
    }
    fwrite(buf_red,sizeof( int),65536,outptr);
	   //fwrite(alt,sizeof( int),65536,outptr);
	   fclose(outptr);
    
    free(buf_red);
    free(fwd_inv);
    
    
  return 0;
}
