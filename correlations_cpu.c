#include <stdio.h>
#include <stdint.h>

void bin_crosses_2bit(uint8_t *pol0, uint8_t *pol1, int *sum, int ndata, int nchan, int chunk)
{
	const uint8_t mask = 3;
	const int nchunk = ndata/chunk;
	for (int i = 0; i < nchunk; i++)
	{
		unsigned int chunkIdx = 2 * i * nchan;
		for (int j=0;j<nchan;j++)
		{
      			sum[chunkIdx + 2 * j] = 0;
      			sum[chunkIdx + 2 * j + 1] = 0;
      		}
      	}
      	
      	unsigned int totalndata = ndata * nchan;
      	unsigned int chunkData = chunk * nchan;
      	for (unsigned int i = 0; i < totalndata; i++)
      	{
      		int currentChannel = i % nchan;
      		int currentChunk = i % chunkData;
      		
      		int8_t pol0_re;
      		int8_t pol0_im;
      		int8_t pol1_re;
      		int8_t pol1_im;
      		if (i % 2 == 0) //some of the data is in the beginning four bytes, and some of the data is in the ending four bytes.
      		{
      			pol0_re = ((pol0[i] >> 6) & mask) - 1;
      			pol0_im = ((pol0[i] >> 4) & mask) - 1;
      			pol1_re = ((pol1[i] >> 6) & mask) - 1;
      			pol1_im = ((pol1[i] >> 4) & mask) - 1;
      		}
      		else
      		{
      			pol0_re = ((pol0[i] >> 2) & mask) - 1;
      			pol0_im = (pol0[i] & mask) - 1;
      			pol1_re = (pol1[i] >> 2 & mask) - 1;
      			pol1_im = (pol1[i] & mask) - 1;
      		}
      		
      		if (pol0_re <= 0) {pol0_re --;}
      		if (pol0_im <= 0) {pol0_im --;}
      		if (pol1_re <= 0) {pol1_re --;}
      		if (pol1_im <= 0) {pol1_im --;}
      		
      		sum[currentChunk * nchan * 2 + currentChannel * 2] += pol0_re * pol1_re + pol0_im * pol1_im;
      		sum[currentChunk * nchan * 2 + currentChannel * 2 + 1] += pol0_im * pol1_re - pol0_re * pol1_im;
      	}
}

void bin_crosses_4bit(uint8_t *pol0, uint8_t *pol1, int *sum, int ndata, int nchan, int chunk)
{
	const uint8_t rmask = 15;
	const uint8_t imask = 255-15;
	const int nchunk = ndata/chunk;
	for (int i = 0; i < nchunk; i++)
	{
		unsigned int chunkIdx = 2 * i * nchan;
		for (int j=0;j<nchan;j++) 
		{
      			sum[chunkIdx + 2 * j] = 0;
      			sum[chunkIdx + 2 * j + 1] = 0;
      			for (int k = 0; k < chunk; k++)
      			{
      				unsigned int idx = i * nchan * chunk + j + k * nchan;
      				
      				//getting the values
      				int8_t pol0_re = pol0[idx] & rmask;
      				int8_t pol0_im = (pol0[idx] & imask) >> 4;
      				int8_t pol1_re = pol1[idx] & rmask;
      				int8_t pol1_im = (pol1[idx] & imask) >> 4;
      				if (pol0_re > 8) {pol0_re -= 16;}
      				if (pol0_im > 8) {pol0_im -= 16;}
      				if (pol1_re > 8) {pol1_re -= 16;}
      				if (pol1_im > 8) {pol1_im -= 16;}
      				
      				sum[chunkIdx + 2 * j] += pol0_re * pol1_re + pol0_im * pol1_im;
      				sum[chunkIdx + 2 * j + 1] += pol0_im * pol1_re - pol0_re * pol1_im;
      			}
    		}
	}
}

void average_cross_correlations (uint8_t *pol0, uint8_t *pol1, float *averages, int ndata, int nchan, int chunk, short bit_depth)
{
	int sum [2 * nchan * (ndata/chunk)];
	
	if (bit_depth == 4)
	{
		bin_crosses_4bit(pol0, pol1, sum, ndata, nchan, chunk);
	}
	else if (bit_depth == 2)
	{
		bin_crosses_2bit(pol0, pol1, sum, ndata, nchan, chunk);
	}
	else if (bit_depth == 1)
	{
		//bin_crosses_1bit(pol0, pol1, sum, ndata, nchan, chunk); not implemented yet
	}
	else printf("Average Cross Correlations Unknown Bit Depth\n");
	
	for (int i = 0; i < 2 * nchan; i++)
	{
		int sumssum = 0;
		for (int j = 0; j < ndata/chunk; j ++)
		{
			sumssum += sum[i + j * 2 * nchan];
		}
		averages[i] = sumssum * 1.0 / (ndata/chunk);
	}
}
