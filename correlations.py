from baseband_data_classes import baseband_data_packed
import ctypes
import numpy
import os

mylib=ctypes.cdll.LoadLibrary(os.path.realpath(__file__+r"/..")+"/lib_correlations_cpu.so")
mylib.average_cross_correlations.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_short]

def average_cross_correlations (filename):
	bb_data = baseband_data_packed(filename)
	
	averages_pointer = (ctypes.c_float * (2 * bb_data.length_channels))()
	mylib.average_cross_correlations(bb_data.pol0.ctypes.data, bb_data.pol1.ctypes.data, averages_pointer, bb_data.pol0.shape[0], bb_data.length_channels, 100, bb_data.bit_mode)
	
	averages = numpy.zeros(bb_data.length_channels, dtype = "complex64")
	for i in range(bb_data.length_channels):
		averages[i] = averages_pointer[2 * i] + averages_pointer[2 * i + 1] * 1j
	
	print(averages)
