# correlations
Better correlations including CPU and GPU versions.

This is an early commit and it doesn't work yet.

Usage: Both c files need to be compiled into .so files. I'll write a setup script to do this.

The classes for importing baseband data are in baseband_data_classes.py. More will be added. Currently only 4 bit unpacking is supported.

Use the unpacked version of the class as the argument for average_cross_correlations in correlations.py to find the average.
