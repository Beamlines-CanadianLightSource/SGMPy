# Open date file and get scan details

import os
from praxes.io import spec
from praxes.io.phynx import File
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

# For Windows, Please use "/" instead of "\" in the file directory (URI)
def open_spec_data_file(file_directory):
	opened_file = spec.open(file_directory)
	return opened_file

def open_hdf5_file(file_directory):
	opened_file = File(file_directory)
	return opened_file

def get_abs_path(rel_path):
	script_dir = os.path.dirname(os.path.realpath('__file__'))
	abs_path = os.path.join(script_dir, rel_path)
	return abs_path


def get_total_scan_num(opened_file):
	total_scan_num = len(opened_file.keys())
	return total_scan_num
    
    
def get_scan_details(opened_file):
	scan_details_list = opened_file.keys()
	for i in range(0,len(scan_details_list)):
		labels = opened_file[scan_details_list[i]].attrs['labels']
		command = opened_file[scan_details_list[i]].attrs['command']
		date = opened_file[scan_details_list[i]].attrs['date']
		print 'Scan:', scan_details_list[i], '    The Command is: ',command, '    DateTime: ', date
		print
        
        
#def checkFileType(opened_file):
#	scan = opened_file['1']
#	keys_list = scan.keys()
#	# Iterate keys in the list
#	for i in range(0,len(keys_list)):
#		if keys_list[i] == 'Energy':
#			return 'This is the data file of spectra.'
#		elif keys_list[i] == 'Hex_XP':
#			return 'This is a map data file.'
#	# It is a weird case, neither map nor spectra file
#	return 'invalid data file!!!'


def check_scan_variety(opened_file):
	cmesh_array = []
	c_array = []
	a_array = []
	mesh_array = []
    
	for i in range (1, len(opened_file)+1):
		# print "Scan No.", i
		string=str(i)
		string =  opened_file[string].attrs['command']
		temp_array = string.split( )
		if temp_array[0] == "cmesh":
			cmesh_array.append(i)
		elif temp_array[0] == "cscan":
			c_array.append(i)
		elif temp_array[0] == "ascan":
			a_array.append(i)
		elif temp_array[0] == "mesh":
			mesh_array.append(i)
	return c_array, a_array, cmesh_array, mesh_array
            