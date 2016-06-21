# binning and plotting

from praxes.io import spec
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO
from open_hdf5 import *
from open_spec import *


def generate_good_scan_index(scan_num_array, bad_scan_str):
	#good_scan_index = []
	# if badScanStr is null, then return original arrays
	if bad_scan_str == '':
		print "In if"
		length = len(scan_num_array)
		good_scan_index = range(0, length, 1)
		return good_scan_index
	# to get good scan numbers
	else:
		print "In else"
		# split the array based on comma symbol
		bad_scan_num_array = bad_scan_str.split(',', )
		# convert char(string) to int
		bad_scan_num_array = map(float, bad_scan_num_array)
		length = len(scan_num_array)
		good_scan_index = range(1, length+1, 1)
		print "original good_scan_index:", good_scan_index
		for i in range(0, len(scan_num_array)):
			for j in range (0, len(bad_scan_num_array)):
				if scan_num_array[i] == bad_scan_num_array[j]:
					print "removed", scan_num_array[i]
					good_scan_index.remove(i+1)
		return good_scan_index


def prepare_bin_plot_hdf5 (good_scan, file_directory, start_energy, end_energy, number_of_bins, start_region_of_interest, end_region_of_interest):

	energy_data, mca_data, scaler_data = read_hdf5(file_directory)
	energy_array, mca_array, scaler_array = get_good_datapoint_hdf5(good_scan_index, energy_data, mca_data, scaler_data)

	edges_array, bins_mean_array = create_bins(start_energy, end_energy, number_of_bins)
	assigned_data_array = assign_data(energy_array , edges_array)
    # calculate average
	result = calculate_bin_mca(assigned_data_array, mca_array)
	bin_mca = result[:-1]
	empty_bin_num = result[-1]
	bin_scaler = calculate_bin_scalers(assigned_data_array, scaler_array)
	pyf_data = get_pfy_bin(bin_mca, start_region_of_interest, end_region_of_interest)
    
	#remove empty bins
	return bins_mean_array[:-empty_bin_num], bin_mca, bin_scaler, pyf_data
    
    
def get_good_datapoint_hdf5(good_scan_index, energy_data, mca_data, scaler_data):
	good_scan_index_length = len(good_scan_index)
	print "Total good scan numbers:", good_scan_index_length
    
	energy_array = []
	scaler_array = [[[],[],[]] for i in range(good_scan_index_length)]
	mca_array=[[[],[],[],[]] for i in range(good_scan_index_length)]
	for i in range (0, len(good_scan_index)):
		# scan number is start from 1
		# print "This is the scan number: ", goodScanArray[i]
		# array index is start from 0
		# get all scalers of good scans from original scans' array
		energy_array.append(energy_data[good_scan_index[i]-1])
		scaler_array[i][0] = scaler_data[good_scan_index[i]-1][0]
		scaler_array[i][1] = scaler_data[good_scan_index[i]-1][1]
		scaler_array[i][2] = scaler_data[good_scan_index[i]-1][2]
		# get all MCA1 of good scans from original scans
		mca_array[i][0] = mca_data[good_scan_index[i]-1][0]
		# get all MCA2 of good scans from original scans
		mca_array[i][1] = mca_data[good_scan_index[i]-1][1]
		# get all MCA3 of good scans from original scans
		mca_array[i][2] = mca_data[good_scan_index[i]-1][2]
		# get all MCA4 of good scans from original scans
		mca_array[i][3] = mca_data[good_scan_index[i]-1][3]
	return energy_array, mca_array, scaler_array



def prepare_blank_bin_plot_spec(good_scan_index, opened_blank_file, start_energy, end_energy, number_of_bins, start_region_of_interest, end_region_of_interest):
	energy_array, sdd1_array = get_good_datapoint_sdd1_spec(good_scan_index, opened_blank_file)
	edges_array, mean_energy_array = create_bins(start_energy, end_energy, number_of_bins)
	bin_array = assign_data(energy_array, edges_array)
	blank_sdd1_binned_array = calculate_blank_sdd1(bin_array, sdd1_array)
	blank_pfy_sdd1_binned_array = get_one_pfy_bin(blank_sdd1_binned_array, start_region_of_interest, end_region_of_interest)
	return blank_pfy_sdd1_binned_array


def prepare_bin_plot_spec(good_scan, opened_file, start_energy, end_energy, number_of_bins, start_region_of_interest, end_region_of_interest):
    
	energy_array, mca_array, scaler_array = get_good_datapoint_spec(good_scan, opened_file)

	edges_array, bins_mean_array = create_bins(start_energy, end_energy, number_of_bins)
	assigned_data_array = assign_data(energy_array , edges_array)
    # calculate average
	result = calculate_bin_mca(assigned_data_array, mca_array)
	bin_mca = result[:-1]
	empty_bin_num = result[-1]
	bin_scaler = calculate_bin_scalers(assigned_data_array, scaler_array)
	pyf_data = get_pfy_bin(bin_mca, start_region_of_interest, end_region_of_interest)
    
	#remove empty bins
	return bins_mean_array[:-empty_bin_num], bin_mca, bin_scaler, pyf_data


# Eliminate bad scans and select good scans (data points)
def get_good_datapoint_spec(good_scan_index, opened_file):
	good_scan_index_length = len(good_scan_index)
	print "Total good scan numbers:", good_scan_index_length
    
	energy_array = []
	scaler_array = [[[],[],[]] for i in range(good_scan_index_length)]
	mca_array=[[[],[],[],[]] for i in range(good_scan_index_length)]

	# open and read all data from the file and it could take a while
	scan, mca1, mca2, mca3, mca4 = openAllSGMXAS(opened_file)
        
	for i in range (0, good_scan_index_length):
		# scan number is start from 1
		# print "This is the scan number: ", goodScanArray[i]
		# array index is start from 0
		# get all scalers of good scans from original scans' array
		energy_array.append(scan[good_scan_index[i]-1]['Energy'])
		scaler_array[i][0] = scan[good_scan_index[i]-1]['TEY']
		scaler_array[i][1] = scan[good_scan_index[i]-1]['I0']
		scaler_array[i][2] = scan[good_scan_index[i]-1]['Diode']
		# get all MCA1 of good scans from original scans
		mca_array[i][0] = mca1[good_scan_index[i]-1]
		# get all MCA2 of good scans from original scans
		mca_array[i][1] = mca2[good_scan_index[i]-1]
		# get all MCA3 of good scans from original scans
		mca_array[i][2] = mca3[good_scan_index[i]-1]
		# get all MCA4 of good scans from original scans
		mca_array[i][3] = mca4[good_scan_index[i]-1]
	return energy_array, mca_array, scaler_array

# create bins (startEnergy = 690, endEnergy = 750, numberOfBins = 600)
def create_bins(start_energy, end_energy, num_of_bins):
	print "Start creating bins" 
	num_of_edges = num_of_bins + 1
	print "Number of Bins:", num_of_bins
	print "Number of Edges:", num_of_edges
	print "Energy range is: ", start_energy,"-", end_energy
	edges_array = np.linspace(start_energy, end_energy, num_of_edges)

	# generate mean of bins  
	mean_energy_array = []
	first_mean = (edges_array[1] + edges_array[0]) / 2
	bin_width = edges_array[1] - edges_array[0]
	for i in range (0, num_of_bins):
		mean_energy_array.append(first_mean + bin_width * i)
	# print "Mean of energy bins: ", mean_energy_array
	print "created bins completed."
	print
	return  edges_array, mean_energy_array


def assign_data (energy_array, edges):
	bin_num = len(edges) - 1
	bin_array = [[] for i in range(bin_num)]

	# interation to assign data into bins
	bin_width = (edges[-1] - edges[0]) / bin_num
	print "The width of a bin is:", bin_width
	print "Start assigning data points into bins" 
	for scan_index in range (0, len(energy_array)):
		for datapoint_index in range (0, len(energy_array[scan_index]) ):
			x = energy_array[scan_index][datapoint_index] - edges[0]
			#Get integer part and plus 1
			assign_bin_num = int(x / bin_width) + 1
			# print assign_bin_num
			bin_array[assign_bin_num-1].append([scan_index, datapoint_index])
	print "Assign data points completed"   
	return bin_array

def get_good_datapoint_sdd1_spec(good_scan_Array, opened_file):
    
	# print "Total good scan numbers:", len(good_scan_Array)
    
	energy_array = []
	sdd1_array=[]

	# open and read all data from the file and it could take a while
	scan, mca1, mca2, mca3, mca4 = openAllSGMXAS(opened_file)
        
	for i in range (0, len(good_scan_Array)):
		# scan number is start from 1
		# print "This is the scan number: ", goodScanArray[i]
		# array index is start from 0
		# get all scalers of good scans from original scans' array
		energy_array.append(scan[good_scan_Array[i]-1]['Energy'])

		# get all MCA1 of good scans from original scans
		sdd1_array.append( mca1[good_scan_Array[i]-1] )

	return energy_array, sdd1_array


def calculate_blank_sdd1(bin_array, sdd1):
	bin_num = len(bin_array)
	empty_bins = 0  
	mca1_bin_array = np.zeros(shape=(bin_num,256))
       
	for index1 in range (0, bin_num):
		# get the total number of data points in a particular bins
		total_data_point = len(bin_array[index1])
        
		for index2 in range (0, total_data_point):
			# get index of scans
			index_of_scan = bin_array[index1][index2][0]
			# get index of data points
			index_of_data_point = bin_array[index1][index2][1]
			# print "index_of_scan: ", index_of_scan_2, "  ;  ", "index_of_data_point: ", index_of_data_point

			# calculate the sum of MCA1
			mca1_bin_array[index1] = mca1_bin_array[index1] + sdd1[index_of_scan][index_of_data_point]
		if total_data_point == 0:
			empty_bins = empty_bins + 1
			print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
		else:
			# calculate the average of MCAs
			# print "Calculating Average of MCA1."
			mca1_bin_array[index1] = mca1_bin_array[index1] / total_data_point
			# print "Calculation Average of MCA1 is completed.
	print "Calculation completed."
	print
	return mca1_bin_array[:-empty_bins]
            

def calculate_bin_mca(bin_array, mca_array):
	bin_num = len(bin_array)
	empty_bins = 0
	# Initial 4 arrays for 4 average of MCAs
	# Added 256 of zero into each sub array, so that it could calculate summary and then get the average
	mca1_bin_array = np.zeros(shape=(bin_num,256))
	mca2_bin_array = np.zeros(shape=(bin_num,256))
	mca3_bin_array = np.zeros(shape=(bin_num,256))
	mca4_bin_array = np.zeros(shape=(bin_num,256))

	print "Start calcualting average of SDD1(MCA1), SDD2(MCA2), SDD3(MCA3) & SDD4(MCA4)..."
        
	for index1 in range (0, bin_num):
		# get the total number of data points in a particular bins
		total_data_point = len(bin_array[index1])

		for index2 in range (0, total_data_point):
			# get index of scans
			index_of_scan = bin_array[index1][index2][0]
			# get index of data points
			index_of_data_point = bin_array[index1][index2][1]
			# print "index_of_scan: ", index_of_scan_2, "  ;  ", "index_of_data_point: ", index_of_data_point

			# calculate the sum of MCA1
			mca1_bin_array[index1] = mca1_bin_array[index1] + mca_array[index_of_scan][0][index_of_data_point]
			# calculate the sum of MCA2
			mca2_bin_array[index1] = mca2_bin_array[index1] + mca_array[index_of_scan][1][index_of_data_point]
			# calculate the sum of MCA3
			mca3_bin_array[index1] = mca3_bin_array[index1] + mca_array[index_of_scan][2][index_of_data_point]
			# calculate the sum of MCA4
			mca4_bin_array[index1] = mca4_bin_array[index1] + mca_array[index_of_scan][3][index_of_data_point]
            
		# print "Bin No.", index1+1, "; it contains ", total_data_point, "data points"
        
		if total_data_point == 0:
			empty_bins = empty_bins + 1
			print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
		else:
			# calculate the average of MCAs
			# print "Calculating Average of MCA1."
			mca1_bin_array[index1] = mca1_bin_array[index1] / total_data_point
			# print "Calculation Average of MCA1 is completed."
			# print "Calculating Average of MCA2."
			mca2_bin_array[index1] = mca2_bin_array[index1] / total_data_point
			# print "Calculation Average of MCA2 is completed."
			# print "Calculating Average of MCA3."
			mca3_bin_array[index1] = mca3_bin_array[index1] / total_data_point
			# print "Calculation Average of MCA3 is completed."
			# print "Calculating Average of MCA4."
			mca4_bin_array[index1] = mca4_bin_array[index1] / total_data_point
			# print "Calculation Average of MCA4 is completed."
			# print

	print "Calculation completed."
	print
	return mca1_bin_array[:-empty_bins], mca2_bin_array[:-empty_bins], mca3_bin_array[:-empty_bins], mca4_bin_array[:-empty_bins], empty_bins


def calculate_bin_scalers(arrayOfBins, scaler_array):

	bin_num = len(arrayOfBins)
	empty_bins = 0
	tey_bin_array = np.zeros(bin_num)
	i0_bin_array = np.zeros(bin_num)
	diode_bin_array = np.zeros(bin_num)
    
	print "Start calcualting Average of I0, TEY & Diode..."
    
	for index1 in range (0, bin_num):
		for index2 in range (0, len(arrayOfBins[index1])):
			# get index of scans
			index_of_scan = arrayOfBins[index1][index2][0]
			# print index_of_scan
			# get index of data points
			index_of_data_point = arrayOfBins[index1][index2][1]
			# print index_of_data_point_2
            
			# calculate the sum of data (TEY, I0, Diode)
			tey_bin_array[index1] = tey_bin_array[index1] + scaler_array[index_of_scan][0][index_of_data_point]
			i0_bin_array[index1] = i0_bin_array[index1] + scaler_array[index_of_scan][1][index_of_data_point]
			diode_bin_array[index1] = diode_bin_array[index1] + scaler_array[index_of_scan][2][index_of_data_point]

		# get the total number of data points in a particular bins
		total_data_point = len(arrayOfBins[index1])
		# print "Bin No.", index1+1, "; it contains ", total_data_point, "data point"   
        
		if total_data_point == 0:
			empty_bins = empty_bins + 1
			print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
		else:
			# print total_data_point
			# calculate the average of data (TEY, I0, Diode)
			# print "Calculating Average of TEY."
			tey_bin_array[index1] = tey_bin_array[index1] / total_data_point
			# print "Calculation Average of TEY is completed."
			# print "Calculating Average of I0."
			i0_bin_array[index1] = i0_bin_array[index1] / total_data_point
			# print "Calculation Average of I0 is completed."
			# print "Calculating Average of Diode."
			diode_bin_array[index1] = diode_bin_array[index1] / total_data_point
			# print "Calculation Average of Diode is completed."
			# print "Index of bins:", index1, "   Average of TEY:", tey_bin_array[index1]
			# print "Index of bins:", index1, "   Average of I0:", i0_bin_array[index1]
			# print "Index of bins:", index1, "   Average of Diode:", diode_bin_array[index1]
			# print

	print "Calculation completed."
	print
    
	return tey_bin_array[:-empty_bins], i0_bin_array[:-empty_bins], diode_bin_array[:-empty_bins]


def plot_excitation_emission_matrix(bins_mean_array, bin_mca, name):
    
	print "Plotting incident v emission energy coordinate based on average of SDD(MCA)"    
	plt.close('all')
	# MCA is SDD and SDD is MCA
	mca_dict = {'SDD1': 0, 'SDD2': 1, 'SDD3': 2, 'SDD4': 3}
	sub_mca_array_index = mca_dict[name]
	sub_mca_array = bin_mca[sub_mca_array_index]
    
	num_of_bin = len (bins_mean_array)
	num_of_emission_bins = len(sub_mca_array[0])
    
	bin_num_for_x = [[]for i in range(num_of_bin)]
	for bin in range (0, num_of_bin):
		bin_num_for_x[bin] = np.empty(num_of_emission_bins)
		# fill energy into the array
		bin_num_for_x[bin].fill(bins_mean_array[bin])

	# generate a list of number to present 1 - 256 bins for emission energy
	bin_num_for_y = np.arange(10, (num_of_emission_bins+1)*10, 10)
	for x in range (0, num_of_bin):
		plt.scatter(bin_num_for_x[x], bin_num_for_y, c= sub_mca_array[x], s=7, linewidths=0)
        
	plt.xlabel('Incident Energy (eV)')
	plt.ylabel('Emission Energy (eV)')
	plt.show()
	print "Incident Energy range:", bin_num_for_x[0][0], "-", bin_num_for_x[-1][0]
	print "Emission Energy range:", bin_num_for_y[0], "-", bin_num_for_y[-1]
	return bin_num_for_y
    
def get_pfy_bin(mca_bin_array, start_energy, stop_energy):

	print "Getting PFY ROIs"

	pfy1=[]
	pfy2=[]
	pfy3=[]
	pfy4=[]

	for i in range(0, len(mca_bin_array[0])):
		pfy1.append(np.sum(mca_bin_array[0][i][start_energy:stop_energy]))
		pfy2.append(np.sum(mca_bin_array[1][i][start_energy:stop_energy]))
		pfy3.append(np.sum(mca_bin_array[2][i][start_energy:stop_energy]))
		pfy4.append(np.sum(mca_bin_array[3][i][start_energy:stop_energy]))
	
	return pfy1, pfy2, pfy3, pfy4


def get_one_pfy_bin(mca_bin_array, start_energy, stop_energy):

	print "Getting PFY ROIs"

	pfy=[]

	for i in range(0, len(mca_bin_array)):
		pfy.append(np.sum(mca_bin_array[i][start_energy:stop_energy]))
	return pfy


# plot a kind of average scaler
def plot_bin_xas(mean_energy_array, name, scaler_data=None, pfy_data=None):
	plt.close('all')
	if name == "TEY" or name == "I0" or name == "Diode":
		plot_bin_xas_scaler(mean_energy_array, scaler_data, name)
	elif name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
		plot_bin_xas_pfy(mean_energy_array, pfy_data, name)
	else:
		print "Errors with the name input"

        
def plot_bin_xas_scaler(mean_energy_array, scaler_data, name):
	plt.close('all')
	scaler_dict = {'TEY': 0, 'I0': 1, 'Diode':2}
	scaler_index = scaler_dict[name]
	plt.plot(mean_energy_array, scaler_data[scaler_index])
	plt.xlabel('Energy (eV)')
	plt.ylabel(name)
	plt.show()
    
def plot_bin_xas_pfy(mean_energy_array, pfy_data, name):
	plt.close('all')
    
	pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
	pfy_index = pfy_dict[name]
	plt.plot(mean_energy_array, pfy_data[pfy_index])
	plt.xlabel('Energy (eV)')
	plt.ylabel(name)
	plt.show()


def plot_bin_xas_all(energy_array, scaler_array, pfy_data):
	
	print "Plotting average XAS."    
	plt.close('all')

	en = energy_array
	tey = scaler_array[0]
	i0 = scaler_array[1]
	diode = scaler_array[2]

	plt.figure(1)
	plt.subplot(4, 2, 1)
	plt.plot(en, tey)
	# add lable for x and y axis
	plt.xlabel('Energy (eV)')
	plt.ylabel('TEY')
    
	plt.subplot(4, 2, 2)
	plt.plot(en, i0)
	plt.xlabel('Energy (eV)')
	plt.ylabel('I0')
    
	plt.subplot(4, 2, 3)
	plt.plot(en, diode)
	plt.xlabel('Energy (eV)')
	plt.ylabel('Diode')

	plt.subplot(4, 2, 5)
	plt.plot(en, pfy_data[0])
	plt.xlabel('Energy (eV)')
	plt.ylabel('SDD1')
    
	plt.subplot(4, 2, 6)
	plt.plot(en, pfy_data[1])
	plt.xlabel('Energy (eV)')
	plt.ylabel('SDDA2')
    
	plt.subplot(4, 2, 7)
	plt.plot(en, pfy_data[2])
	plt.xlabel('Energy (eV)')
	plt.ylabel('SDD3')
    
	plt.subplot(4, 2, 8)
	plt.plot(en, pfy_data[3])
	plt.xlabel('Energy (eV)')
	plt.ylabel('SDD4')
    
	figManager = plt.get_current_fig_manager()
	# figManager.window.showMaximized()
	# tight_layout() will also adjust spacing between subplots to minimize the overlaps.
	# plt.tight_layout()
	plt.show()
    
    
def division(pfy_data, dividend, divisor, scaler_data = None):
	# initial new_mca_array
	division_pfy_array = np.empty(len(pfy_data[0]))
	# initial a dictionary for 4 SDD(MCA) name
	pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
	scaler_dict = {'TEY': 0, 'I0': 1, 'Diode': 2}
	if dividend == divisor:
		print "Cannot division same SDD(MCA)"
	# calculate division
	else:
		if divisor == "I0" or divisor == "TEY" or divisor =="Diode":
			dividend_index = pfy_dict[dividend]
			divisor_index = scaler_dict[divisor]
			division_array = np.array(pfy_data[dividend_index]) / np.array(scaler_data[divisor_index])
		else:
			dividend_index = pfy_dict[dividend]
			divisor_index = pfy_dict[divisor]
			division_array = np.array(pfy_data[dividend_index]) / np.array(pfy_data[divisor_index])
		return division_array


def plot_division(bins_mean_array, pfy_data, dividend, divisor, scaler_data = None):

	print "Plotting disivion SDD."    
	plt.close('all')
	division_array = division(pfy_data, dividend, divisor, scaler_data)
	plt.plot(bins_mean_array, division_array)
	plt.xlabel('Energy (eV)')
	str_y_axis = StringIO()
	str_y_axis.write(dividend)
	str_y_axis.write('/')
	str_y_axis.write(divisor)
	plt.ylabel(str_y_axis.getvalue())
	plt.show()
    