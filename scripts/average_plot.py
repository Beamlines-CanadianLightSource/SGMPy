# Selection and Binning

from praxes.io import spec
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO
from scan_details import *
from basic_plot import *


def prepare_average_plot(good_scan, opened_file, start_energy, end_energy, number_of_bins, start_range_of_interest, end_range_of_interest):
    
	data_point_array = get_good_datapoint(good_scan, opened_file)

	temp_array = create_bins(start_energy, end_energy, number_of_bins)
	edges_array = temp_array[0]
	bins_mean_array = temp_array[1]
	assigned_data_array = assign_data(data_point_array , edges_array)
    # calculate average
	result = calculate_avg_mca(assigned_data_array, data_point_array)
	avg_mca = result[:-1]
	empty_bin_num = result[-1]
	avg_scaler = calculate_avg_scalers(assigned_data_array, data_point_array)
	pyf_data = get_pfy_avg(avg_mca, start_range_of_interest, end_range_of_interest)
    
    #remove empty bins
    
	return bins_mean_array[:-empty_bin_num], avg_mca, avg_scaler, pyf_data


# Eliminate bad scans and select good scans (data points)
def get_good_datapoint(good_scan_Array, opened_file):
    
	print "Total good scan numbers:", len(good_scan_Array)
	# initial arrays    
	scan=[]
	mca1=[]
	mca2=[]
	mca3=[]
	mca4=[]
    
	# open and read all data from the file and it could take a while
	scan, mca1, mca2, mca3, mca4 = openAllSGMXAS(opened_file)
    
	# Initial arrayOfPoints
	data_array=[[[],[],[],[],[]] for i in range(len(good_scan_Array))]
    
	for i in range (0, len(good_scan_Array)):
		# scan number is start from 1
		# print "This is the scan number: ", goodScanArray[i]
		# array index is start from 0
		# get all scalers of good scans from original scans' array
		data_array[i][0] = scan[good_scan_Array[i]-1]
		# get all MCA1 of good scans from original scans
		data_array[i][1] = mca1[good_scan_Array[i]-1]
		# get all MCA2 of good scans from original scans
		data_array[i][2] = mca2[good_scan_Array[i]-1]
		# get all MCA3 of good scans from original scans
		data_array[i][3] = mca3[good_scan_Array[i]-1]
		# get all MCA4 of good scans from original scans
		data_array[i][4] = mca4[good_scan_Array[i]-1]
	return data_array

# create bins (for testing startEnergy = 690, endEnergy = 750, numberOfBins = 120, energyArray = scan[goodScan_2[i]-1]['Energy'])
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
		mean_energy_array.append(first_mean + 0.1 * i)
	# print "Mean of energy bins: ", mean_energy_array
	print "created bins completed."
	print
	return  edges_array, mean_energy_array


def assign_data (data_array, edges):
	bin_num = len(edges) - 1
	bin_array = [[] for i in range(bin_num)]

	# interation to assign data into bins
	bin_width = (edges[-1] - edges[0]) / bin_num
	print "The width of a bin is:", bin_width
	print "Start assigning data points into bins" 
	for scan_index in range (0, len(data_array)):
		for datapoint_index in range (0, len(data_array[scan_index][0]['Energy']) ):
			x = data_array[scan_index][0]['Energy'][datapoint_index] - edges[0]
			# how to get integer part + 1?????
			assign_bin_num = int(x / bin_width) + 1
			# print assignBinNum
			bin_array[assign_bin_num-1].append([scan_index, datapoint_index])
	print "Assign data points completed"   
	return bin_array

def calculate_avg_mca(arrayOfBins, arrayOfPoints):
	binNum = len(arrayOfBins)
	empty_bins = 0
	# Initial 4 arrays for 4 Average of MCAs
	# Added 256 of zero into each sub array, so that it could calculate summary and then get the average
	mca1AvgArray = np.zeros(shape=(binNum,256))
	mca2AvgArray = np.zeros(shape=(binNum,256))
	mca3AvgArray = np.zeros(shape=(binNum,256))
	mca4AvgArray = np.zeros(shape=(binNum,256))

	print "Start calcualting Average of SDD1(MCA1), SDD2(MCA2), SDD3(MCA3) & SDD4(MCA4)..."
        
	for index1 in range (0, binNum):
		# get the total number of data points in a particular bins
		totalDataPoints = len(arrayOfBins[index1])

		for index2 in range (0, totalDataPoints):
			# get index of scans
			indexOfScan = arrayOfBins[index1][index2][0]
			# get index of data points
			indexOfDataPoint = arrayOfBins[index1][index2][1]
			# print "indexOfScan: ", indexOfScan_2, "  ;  ", "indexOfDataPoint: ", indexOfDataPoint

			# calculate the sum of MCA1
			mca1AvgArray[index1] = mca1AvgArray[index1] + arrayOfPoints[indexOfScan][1][indexOfDataPoint]
			# calculate the sum of MCA2
			mca2AvgArray[index1] = mca2AvgArray[index1] + arrayOfPoints[indexOfScan][2][indexOfDataPoint]
			# calculate the sum of MCA3
			mca3AvgArray[index1] = mca3AvgArray[index1] + arrayOfPoints[indexOfScan][3][indexOfDataPoint]
			# calculate the sum of MCA4
			mca4AvgArray[index1] = mca4AvgArray[index1] + arrayOfPoints[indexOfScan][4][indexOfDataPoint]
            
		# print "Bin No.", index1+1, "; it contains ", totalDataPoints, "data points"
        
		if totalDataPoints == 0:
			empty_bins = empty_bins + 1
			print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
		else:
			# calculate the average of MCAs
			# print "Calculating Average of MCA1."
			mca1AvgArray[index1] = mca1AvgArray[index1] / totalDataPoints
			# print "Calculation Average of MCA1 is completed."
			# print "Calculating Average of MCA2."
			mca2AvgArray[index1] = mca2AvgArray[index1] / totalDataPoints
			# print "Calculation Average of MCA2 is completed."
			# print "Calculating Average of MCA3."
			mca3AvgArray[index1] = mca3AvgArray[index1] / totalDataPoints
			# print "Calculation Average of MCA3 is completed."
			# print "Calculating Average of MCA4."
			mca4AvgArray[index1] = mca4AvgArray[index1] / totalDataPoints
			# print "Calculation Average of MCA4 is completed."
			# print

	print "Calculation completed."
	print
	return mca1AvgArray[:-empty_bins], mca2AvgArray[:-empty_bins], mca3AvgArray[:-empty_bins], mca4AvgArray[:-empty_bins], empty_bins


def calculate_avg_scalers(arrayOfBins, arrayOfPoints):

	binNum = len(arrayOfBins)
	empty_bins = 0
	teyAvgArray = np.zeros(binNum)
	i0AvgArray = np.zeros(binNum)
	diodeAvgArray = np.zeros(binNum)
    
	print "Start calcualting Average of I0, TEY & Diode..."
    
	for index1 in range (0, binNum):
		for index2 in range (0, len(arrayOfBins[index1])):
			# get index of scans
			indexOfScan = arrayOfBins[index1][index2][0]
			# print indexOfScan
			# get index of data points
			indexOfDataPoint = arrayOfBins[index1][index2][1]
			# print indexOfDataPoint_2
            
			# calculate the sum of data (TEY, I0, Diode)
			teyAvgArray[index1] = teyAvgArray[index1] + arrayOfPoints[indexOfScan][0]['TEY'][indexOfDataPoint]
			i0AvgArray[index1] = i0AvgArray[index1] + arrayOfPoints[indexOfScan][0]['I0'][indexOfDataPoint]
			diodeAvgArray[index1] = diodeAvgArray[index1] + arrayOfPoints[indexOfScan][0]['Diode'][indexOfDataPoint]

		# get the total number of data points in a particular bins
		totalDataPoints = len(arrayOfBins[index1])
		# print "Bin No.", index1+1, "; it contains ", totalDataPoints, "data point"   
        
		if totalDataPoints == 0:
			empty_bins = empty_bins + 1
			print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
		else:
			# print totalDataPoints
			# calculate the average of data (TEY, I0, Diode)
			# print "Calculating Average of TEY."
			teyAvgArray[index1] = teyAvgArray[index1] / totalDataPoints
			# print "Calculation Average of TEY is completed."
			# print "Calculating Average of I0."
			i0AvgArray[index1] = i0AvgArray[index1] / totalDataPoints
			# print "Calculation Average of I0 is completed."
			# print "Calculating Average of Diode."
			diodeAvgArray[index1] = diodeAvgArray[index1] / totalDataPoints
			# print "Calculation Average of Diode is completed."
			# print "Index of bins:", index1, "   Average of TEY:", TEYAvgArray[index1]
			# print "Index of bins:", index1, "   Average of I0:", I0AvgArray[index1]
			# print "Index of bins:", index1, "   Average of Diode:", DiodeAvgAverage[index1]
			# print

	print "Calculation completed."
	print
    
	return teyAvgArray[:-empty_bins], i0AvgArray[:-empty_bins], diodeAvgArray[:-empty_bins]


def plot_excitation_emission_matrix(bins_mean_array, avg_mca, name):
    
	print "Plotting incident v emission energy coordinate based on average of SDD(MCA)"    
	plt.close('all')
	# MCA is SDD and SDD is MCA
	mca_dict = {'SDD1': 0, 'SDD2': 1, 'SDD3': 2, 'SDD4': 3}
	sub_mca_array_index = mca_dict[name]
	sub_mca_array = avg_mca[sub_mca_array_index]
    
	num_of_bin = len (bins_mean_array)
	num_of_emission_bins = len(sub_mca_array[0])
    
	bin_num_for_x = [[]for i in range(num_of_bin)]
	for bin in range (0, num_of_bin):
		bin_num_for_x[bin] = np.empty(num_of_emission_bins)
		# fill energy into the array
		bin_num_for_x[bin].fill(bins_mean_array[bin])

	# generate a list of number to present 1 - 256 bins for emission energy
	bin_num_for_y = list(range(1,num_of_emission_bins+1))

	for x in range (0, num_of_bin):
		plt.scatter(bin_num_for_x[x], bin_num_for_y, c= sub_mca_array[x], s=7, linewidths=0)
        
	plt.xlabel('Incident Energy (eV)')
	plt.ylabel('Emission Energy (eV)')
	plt.show()
	print "Incident Energy range:", bin_num_for_x[0][0], "-", bin_num_for_x[-1][0]
	print "Incident Energy range:", bin_num_for_y[0], "-", bin_num_for_y[-1]
	return bin_num_for_y
    
def get_pfy_avg(mca_avg_array, start_energy, stop_energy):

	print "Getting PFY ROIs"

	pfy1=[]
	pfy2=[]
	pfy3=[]
	pfy4=[]

	for i in range(0, len(mca_avg_array[0])):
		pfy1.append(np.sum(mca_avg_array[0][i][start_energy:stop_energy]))
		pfy2.append(np.sum(mca_avg_array[1][i][start_energy:stop_energy]))
		pfy3.append(np.sum(mca_avg_array[2][i][start_energy:stop_energy]))
		pfy4.append(np.sum(mca_avg_array[3][i][start_energy:stop_energy]))
	
	return pfy1, pfy2, pfy3, pfy4


def get_one_pfy_avg(mca_avg_array, start_energy, stop_energy):

	print "Getting PFY ROIs"

	pfy=[]

	for i in range(0, len(mca_avg_array)):
		pfy.append(np.sum(mca_avg_array[i][start_energy:stop_energy]))
	return pfy


# plot a kind of average scaler
def plot_avg_xas(mean_energy_array, name, scaler_data=None, pfy_data=None):
	plt.close('all')
	if name == "TEY" or name == "I0" or name == "Diode":
		plot_avg_xas_scaler(mean_energy_array, scaler_data, name)
	elif name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
		plot_avg_xas_pfy(mean_energy_array, pfy_data, name)
	else:
		print "Errors with the name input"

        
def plot_avg_xas_scaler(mean_energy_array, scaler_data, name):
	plt.close('all')
	scaler_dict = {'TEY': 0, 'I0': 1, 'Diode':2}
	scaler_index = scaler_dict[name]
	plt.plot(mean_energy_array, scaler_data[scaler_index])
	plt.xlabel('Energy (eV)')
	plt.ylabel(name)
	plt.show()
    
def plot_avg_xas_pfy(mean_energy_array, pfy_data, name):
	plt.close('all')
    
	pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
	pfy_index = pfy_dict[name]
	plt.plot(mean_energy_array, pfy_data[pfy_index])
	plt.xlabel('Energy (eV)')
	plt.ylabel(name)
	plt.show()


def plot_avg_xas_all(energy_array, scaler_array, pfy_data):
	
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
    
    
def pfy_sdd_division(pfy_data, dividend_mca, divisor_mca):
	# initial new_mca_array
	new_mca_array = np.empty(len(pfy_data[0]))
	# initial a dictionary for 4 SDD(MCA) name
	pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
	if dividend_mca == divisor_mca:
		print "Cannot division same SDD(MCA)"
	# calculate division
	else:
		dividend_mca_index = pfy_dict[dividend_mca]
		divisor_mca_index = pfy_dict[divisor_mca]
		new_mca_array = np.array(pfy_data[dividend_mca_index]) / np.array(pfy_data[divisor_mca_index])
		return new_mca_array


def plot_pfy_sdd_division(bins_mean_array, pfy_data, dividend_mca, divisor_mca):

	print "Plotting disivion SDD."    
	plt.close('all')
	division_pfy_array = pfy_sdd_division(pfy_data, dividend_mca, divisor_mca)
	plt.plot(bins_mean_array, division_pfy_array)
	plt.xlabel('Energy (eV)')
	str_y_axis = StringIO()
	str_y_axis.write(dividend_mca)
	str_y_axis.write('/')
	str_y_axis.write(divisor_mca)
	plt.ylabel(str_y_axis.getvalue())
	plt.show()
    