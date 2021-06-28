import numpy
import struct
import time
import ctypes
import os

mylib=ctypes.cdll.LoadLibrary(os.path.realpath(__file__+r"/..")+"/lib_unpacking.so")
unpack_4bit_float_c = mylib.unpack_4bit_float
unpack_4bit_float_c.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
sortpols_c = mylib.sortpols
sortpols_c.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_short]

def unpack_4bit(data, length_channels, isfloat):
	if isfloat:
		pol0 = numpy.zeros([data.shape[0]//2,length_channels],dtype='complex64')
		pol1 = numpy.zeros([data.shape[0]//2,length_channels],dtype='complex64')
			
		t1 = time.time()
		unpack_4bit_float_c(data.ctypes.data,pol0.ctypes.data,pol1.ctypes.data,data.shape[0],data.shape[1])
		t2 = time.time()
		print("Took " + str(t2 - t1) + " to unpack")
	else:
		print("not float")
	return pol0, pol1

class baseband_data_float:
	def __init__(self, file_name, items = -1):
		file_data=open(file_name, "rb") #,encoding='ascii')
		header_bytes = struct.unpack(">Q", file_data.read(8))[0]
		header_raw = file_data.read(header_bytes)
		header_data = numpy.frombuffer(header_raw, dtype=[("bytes_per_packet", ">Q"), ("length_channels", ">Q"), ("spectra_per_packet", ">Q"), ("bit_mode", ">Q"), ("have_trimble", ">Q"), ("channels", ">%dQ"%(int((header_bytes-8*10)/8))), ("gps_week", ">Q"), ("gps_seconds", ">Q"), ("gps_lat", ">d"), ("gps_lon", ">d"), ("gps_elev", ">d")])
	    	
	    	#setting all the header values
		self.header_bytes = 8 + header_bytes
		self.bytes_per_packet = header_data["bytes_per_packet"][0]
		self.length_channels = header_data["length_channels"][0]
		self.spectra_per_packet = header_data["spectra_per_packet"][0]
		self.bit_mode = header_data["bit_mode"][0]
		self.have_trimble = header_data["have_trimble"][0]
		self.channels = header_data["channels"][0]
		#self.dtype = "" I don't know where this was given before
		self.gps_week = header_data["gps_week"][0]
		self.gps_timestamp = header_data["gps_seconds"][0]
		self.gps_latitude = header_data["gps_lat"][0]
		self.gps_longitude = header_data["gps_lon"][0]
		self.gps_elevation = header_data["gps_elev"][0]
	    	
		if self.bit_mode == 1:
			self.channels = numpy.ravel(numpy.column_stack((self.channels, self.channels+1)))
			self.length_channels = int(self.length_channels * 2)
		if self.bit_mode == 4:
			self.channels = self.channels[::2]
			self.length_channels = int(self.length_channels / 2)
	    	
		file_data.seek(self.header_bytes)
	    	
		t1 = time.time()
		data = numpy.fromfile(file_data, count= items , dtype=[("spec_num", ">I"), ("spectra", "%dB"%(self.bytes_per_packet-4))])
		t2 = time.time()
		print('took ',t2-t1,' seconds to read raw data on ', file_name)
		file_data.close()
		
		if self.bit_mode == 4:
			raw_spectra = data["spectra"].reshape(-1, self.length_channels)
			self.pol0, self.pol1 = unpack_4bit(raw_spectra, self.length_channels, True)
		else:
			print("bit mode is not 4")
    
	def print_header(self):
		print("Header Bytes = " + str(self.header_bytes) + ". Bytes per packet = " + str(self.bytes_per_packet) + ". Channel length = " + str(self.length_channels) + ". Spectra per packet: " + str(self.spectra_per_packet) + ". Bit mode: " + str(self.bit_mode) + ". Have trimble = " + str(self.have_trimble) + ". Channels: " + str(self.channels) + " GPS week = " + str(self.gps_week)+ ". GPS timestamp = " + str(self.gps_timestamp) + ". GPS latitude = " + str(self.gps_latitude) + ". GPS longitude = " + str(self.gps_longitude) + ". GPS elevation = " + str(self.gps_elevation) + ".")
		
		
def sortpols(data, length_channels, bit_mode):
	pol0 = numpy.zeros([data.shape[0]//2,length_channels],dtype='uint8') #this causes an error when it's //2. I think sortpols is the wrong size or something.
	pol1 = numpy.zeros([data.shape[0]//2,length_channels],dtype='uint8')
			
	t1 = time.time()
	sortpols_c(data.ctypes.data,pol0.ctypes.data,pol1.ctypes.data,data.shape[0],data.shape[1], bit_mode)
	t2 = time.time()
	print("Took " + str(t2 - t1) + " to unpack")
	
	return pol0, pol1
		
class baseband_data_packed:
	def __init__(self, file_name, items = -1):
		file_data=open(file_name, "rb") #,encoding='ascii')
		header_bytes = struct.unpack(">Q", file_data.read(8))[0]
		header_raw = file_data.read(header_bytes)
		header_data = numpy.frombuffer(header_raw, dtype=[("bytes_per_packet", ">Q"), ("length_channels", ">Q"), ("spectra_per_packet", ">Q"), ("bit_mode", ">Q"), ("have_trimble", ">Q"), ("channels", ">%dQ"%(int((header_bytes-8*10)/8))), ("gps_week", ">Q"), ("gps_seconds", ">Q"), ("gps_lat", ">d"), ("gps_lon", ">d"), ("gps_elev", ">d")])
	    	
	    	#setting all the header values
		self.header_bytes = 8 + header_bytes
		self.bytes_per_packet = header_data["bytes_per_packet"][0]
		self.length_channels = header_data["length_channels"][0]
		self.spectra_per_packet = header_data["spectra_per_packet"][0]
		self.bit_mode = header_data["bit_mode"][0]
		self.have_trimble = header_data["have_trimble"][0]
		self.channels = header_data["channels"][0]
		#self.dtype = "" I don't know where this was given before
		self.gps_week = header_data["gps_week"][0]
		self.gps_timestamp = header_data["gps_seconds"][0]
		self.gps_latitude = header_data["gps_lat"][0]
		self.gps_longitude = header_data["gps_lon"][0]
		self.gps_elevation = header_data["gps_elev"][0]
	    	
		if self.bit_mode == 1:
			self.channels = numpy.ravel(numpy.column_stack((self.channels, self.channels+1)))
			self.length_channels = int(self.length_channels * 2)
		if self.bit_mode == 4:
			self.channels = self.channels[::2]
			self.length_channels = int(self.length_channels / 2)
	    	
		file_data.seek(self.header_bytes)
	    	
		t1 = time.time()
		data = numpy.fromfile(file_data, count= items , dtype=[("spec_num", ">I"), ("spectra", "%dB"%(self.bytes_per_packet-4))])
		t2 = time.time()
		print('took ',t2-t1,' seconds to read raw data on ', file_name)
		file_data.close()
		
		if self.bit_mode == 4:
			raw_spectra = data["spectra"].reshape(-1, self.length_channels)
			self.pol0, self.pol1 = sortpols(raw_spectra, self.length_channels, self.bit_mode)
		else:
			print("bit mode is not 4")
		
    
	def print_header(self):
		print("Header Bytes = " + str(self.header_bytes) + ". Bytes per packet = " + str(self.bytes_per_packet) + ". Channel length = " + str(self.length_channels) + ". Spectra per packet: " + str(self.spectra_per_packet) + ". Bit mode: " + str(self.bit_mode) + ". Have trimble = " + str(self.have_trimble) + ". Channels: " + str(self.channels) + " GPS week = " + str(self.gps_week)+ ". GPS timestamp = " + str(self.gps_timestamp) + ". GPS latitude = " + str(self.gps_latitude) + ". GPS longitude = " + str(self.gps_longitude) + ". GPS elevation = " + str(self.gps_elevation) + ".")
