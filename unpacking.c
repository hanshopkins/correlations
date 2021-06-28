#include <stdio.h>
#include <stdint.h>

/*void unpack_4bit(uint8_t* data, double* pol0, double* pol1, int ndat, int nchan)
{
    uint8_t rmask = 15;
    uint8_t imask = 255 - 15;

    long nn = ndat * nchan / 2;
    
    for (int i = 0; i < nn; i++) {
        uint8_t r = data[2 * i] & rmask;
        uint8_t im = (data[2 * i] & imask) >> 4;
        /*pol0[2 * i] = im;
        pol0[2 * i + 1] = r;
        if (pol0[2 * i] > 8)
            pol0[2 * i] -= 16;
        if (pol0[2 * i + 1] > 8)
            pol0[2 * i + 1] -= 16;
        

        r = data[2 * i + 1] & rmask;
        im = (data[2 * i + 1] & imask) >> 4;
        pol1[2 * i] = im;
        pol1[2 * i + 1] = r;
        if (pol1[2 * i] > 8)
            pol1[2 * i] -= 16;
        if (pol1[2 * i + 1] > 8)
            pol1[2 * i + 1] -= 16;

    }
}*/

void unpack_4bit_float(uint8_t *data,float *pol0, float *pol1, int ndat, int nchan)
{
  uint8_t rmask=15;
  uint8_t imask=255-15;

  long nn=ndat*nchan/2;

  for (int i=0;i<nn;i++) {
    uint8_t r=data[2*i]&rmask;
    uint8_t im=(data[2*i]&imask)>>4;
    
    if (im > 8){pol0[2*i] = im - 16;}
    else {pol0[2*i] = im;}
    
    if (r > 8){pol0[2*i+1] = r - 16;}
    else {pol0[2*i+1] = r;}

    r = data[2*i+1]&rmask;
    im = (data[2*i+1]&imask)>>4;
    
    if (im > 8){pol1[2*i] = im - 16;}
    else {pol1[2*i] = im;}
    
    if (r > 8){pol1[2*i+1] = r - 16;}
    else {pol1[2*i+1] = r;}

  }
}

void sortpols (uint8_t *data, uint8_t *pol0, uint8_t *pol1, int ndat, int nchan, short bit_depth)
{
	if (bit_depth == 4){ //do the other bit depths
		long nn=ndat*nchan/2;
		for (int i = 0; i < nn; i++)
		{
			pol0[i] = data[2 * i];//this might be wrong
			pol1[i] = data[2 * i + 1];
		}
	}
}
