# correlations

Usage: Run setup_cpu.py to compile the c files using `python3 -c 'from setup_cpu import build; build()'`

The classes for importing baseband data are in baseband_data_classes.py.

To choose which packets to import, set the spec_selection argument to true, and then the low_specnum and high_specnum arguments to the upper and lower bounds of the spectra you want to import. It will import the packets containing the chosen specnums including both ends.

Use the filename as the argument for average_cross_correlations in correlations.py to find the average. The second argument is the chunk size, or the bin size.

The unpacking_gpu.cu file is currently not finished. It only contains a cuda version of dropped_packets, which on its own is slower than the cpu version.
