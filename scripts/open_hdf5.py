import numpy as np
import h5py


def get_all_scan_num_hdf5(file_directory):
	with h5py.File(file_directory,'r') as hf:
		scan_num_array = map(str, hf.keys())
		scan_num_array = get_number(scan_num_array)
		scan_num_array = map(int, scan_num_array)
		return scan_num_array
    
def get_number(scan_num_array):
	for i in range (0, len(scan_num_array)):
		scan_num_array[i] = scan_num_array[i][1:]
	return scan_num_array

def check_scan_type(scan):
	temp_array = scan['command'][0].split( )
	scan_name = temp_array[0]
	print scan_name
	return scan_name

def read_hdf5(file_directory):
	energy_array = []
	scaler_array = []
	mca_array = []
	scan_number= []
	with h5py.File(file_directory,'r') as hf:
		print('List of arrays in this file: \n', hf.keys())
		total_num = len(hf.keys())
		#scaler_array = [[[],[],[]] for i in range(total_num)]
		#mca_array = [[[], [], [], []] for i in range(total_num)]
		for i in range (0, total_num):
			scaler_data = [[], [], []]
			mca_data = [[], [], [], []]
			# print hf.keys()[i]
			scan = hf.get(hf.keys()[i])
			scan_name = check_scan_type(scan)
			# exclude empty scan
			if scan_name == "cscan" and len(scan['data']) > 2:
				scan_number.append(hf.keys()[i])
				energy_array.append(scan['data']['Energy'][0:])
				scaler_data[0] = scan['data']['TEY'][0:]
				scaler_data[1] = scan['data']['I0'][0:]
				scaler_data[2] = scan['data']['Diode'][0:]
				scaler_array.append(scaler_data)
				mca_data[0] = scan['data']['_mca1_'][0:]
				mca_data[1] = scan['data']['_mca2_'][0:]
				mca_data[2] = scan['data']['_mca3_'][0:]
				mca_data[3] = scan['data']['_mca4_'][0:]
				mca_array.append(mca_data)
	print "..................."            
	return energy_array, mca_array, scaler_array, scan_number

