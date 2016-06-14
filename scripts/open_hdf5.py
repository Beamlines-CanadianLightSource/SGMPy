import numpy as np
import h5py

def read_hdf5(file_directory):
	energy_array = []
	scaler_array = []
	mca_array = []
	with h5py.File(file_directory,'r') as hf:
		print('List of arrays in this file: \n', hf.keys())
		total_num = len(hf.keys())
		scaler_array = [[[],[],[]] for i in range(total_num)]
		for i in range (0, total_num):
			scan = mca_data = hf.get(hf.keys()[i])
			energy_array.append(scan['data']['Energy'][0:])
			scaler_array[i][0] = scan['data']['TEY'][0:]
			scaler_array[i][1] = scan['data']['I0'][0:]
			scaler_array[i][2] = scan['data']['Diode'][0:]
			mca_data = scan['data']['_mca_']
			mca_array.append( get_mca_from_hdf5(mca_data) )
	return energy_array, mca_array, scaler_array


def get_mca_from_hdf5(mca_data):
	array_mca1 = []
	array_mca2 = []
	array_mca3 = []
	array_mca4 = []
	for i in range (0, len(mca_data)):
		if mca_data[i][0] == 1.0:
			# get 256 values and exclude the first column in the dataset
			array_mca1.append(mca_data[i][1:])
		elif mca_data[i][0] == 2.0:
			array_mca2.append(mca_data[i][1:])
		elif mca_data[i][0] == 3.0:
			array_mca3.append(mca_data[i][1:])
		else:
			array_mca4.append(mca_data[i][1:])
	return array_mca1, array_mca2, array_mca3, array_mca4


def mock_read_hdf5(file_directory):
	energy_array = []
	scaler_array = []
	mca_array = []
	with h5py.File(file_directory,'r') as hf:
		print('List of arrays in this file: \n', hf.keys())
		total_num = len(hf.keys())
		scaler_array = [[[],[],[]] for i in range(total_num)]
		for i in range (0, total_num):
			scan = mca_data = hf.get(hf.keys()[i])
			energy_array.append(scan['data']['Energy'][0:])
			scaler_array[i][0] = scan['data']['TEY'][0:]
			scaler_array[i][1] = scan['data']['I0'][0:]
			scaler_array[i][2] = scan['data']['Diode'][0:]
			mca_array.append(scan['data']['_mca_'][0:])
	return energy_array, mca_array, scaler_array