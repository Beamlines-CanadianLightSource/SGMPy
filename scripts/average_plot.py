# Selection and Binning

from praxes.io import spec
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from matplotlib.colors import colorConverter
import numpy as np
from scan_details import *
from basic_plot import *


def prepare_average_plot(good_scan, opened_file, start_energy, end_energy, number_of_bins, start_range_of_interest, end_range_of_interest):
    
	data_point_array = get_good_datapoint(good_scan, opened_file)

	temp_array = create_bins(start_energy, end_energy, number_of_bins)
	edges_array = temp_array[0]
	bins_mean_array = temp_array[1]
	assigned_data_array = assign_data(data_point_array , edges_array)
    # calculate average
	avg_mca = calculate_avg_mca(assigned_data_array, data_point_array)
	avg_scaler= calculate_avg_scalers (assigned_data_array, data_point_array)
	pyf_data = get_pfy_avg(avg_mca, start_range_of_interest, end_range_of_interest)
    
	return bins_mean_array, avg_mca, avg_scaler, pyf_data


# Eliminate bad scans and select good scans (data points)
def get_good_datapoint(good_scan_Array, opened_file):
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
	print
	return bin_array

def calculate_avg_mca(arrayOfBins, arrayOfPoints):
	binNum = len(arrayOfBins)
    
	# Initial 4 arrays for 4 Average of MCAs
	mca1AvgArray = [[] for i in range(binNum)]
	mca2AvgArray = [[] for i in range(binNum)]
	mca3AvgArray = [[] for i in range(binNum)]
	mca4AvgArray = [[] for i in range(binNum)]
    
	# Added 256 of zero into each sub array, so that it could calculate summary and then get the average
	for i in range(binNum):
		mca1AvgArray[i] = np.empty(256)
		mca1AvgArray[i].fill(0)

		mca2AvgArray[i] = np.empty(256)
		mca2AvgArray[i].fill(0)
        
		mca3AvgArray[i] = np.empty(256)
		mca3AvgArray[i].fill(0)
        
		mca4AvgArray[i] = np.empty(256)
		mca4AvgArray[i].fill(0)

	print "Start calcualting Average of MCA1, MCA2, MCA3 & MCA4..."
        
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
	return mca1AvgArray, mca2AvgArray, mca3AvgArray, mca4AvgArray


def calculate_avg_scalers(arrayOfBins, arrayOfPoints):

	binNum = len(arrayOfBins)
    
	teyAvgArray = []
	teyAvgArray = np.empty(binNum)
	teyAvgArray.fill(0)
    
	i0AvgArray = []
	i0AvgArray = np.empty(binNum)
	i0AvgArray.fill(0)
    
	diodeAvgArray = []
	diodeAvgArray = np.empty(binNum)
	diodeAvgArray.fill(0)
    
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
			print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
		else:
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
    
	return teyAvgArray, i0AvgArray, diodeAvgArray


def plotAvgOfMAC(binNum, avgMCA):
    
	plt.close('all')
    
	binNumForX = [[]for i in range(binNum)]
	for bin in range (0, binNum):
		binNumForX[bin]=np.empty(256)
		# bin number start from 1
		binNumForX[bin].fill(bin+1)

	# generate a list of number to present 1 - 256 bins for emission energy
	binNumForY = list(range(1,257))

	for x in range (0, binNum):
		plt.scatter(binNumForX[x], binNumForY, c= avgMCA[x] ,s=7, linewidths=0)
        
	plt.xlabel('Bin Numbers for Incident Energy')
	plt.ylabel('Bin Numbers for Emission Energy')
	plt.show()
    
    
def get_pfy_avg(mcaAvgArray, enStart, enStop):

	print "Getting PFY ROIs"

	pfy1=[]
	pfy2=[]
	pfy3=[]
	pfy4=[]

	for i in range(0, len(mcaAvgArray[0])):
		pfy1.append(np.sum(mcaAvgArray[0][i][enStart:enStop]))
		pfy2.append(np.sum(mcaAvgArray[1][i][enStart:enStop]))
		pfy3.append(np.sum(mcaAvgArray[2][i][enStart:enStop]))
		pfy4.append(np.sum(mcaAvgArray[3][i][enStart:enStop]))
	
	return pfy1, pfy2, pfy3, pfy4


def get_one_pfy_avg(mca_avg_array, start_energy, stop_energy):

	print "Getting PFY ROIs"

	pfy=[]

	for i in range(0, len(mca_avg_array)):
		pfy.append(np.sum(mca_avg_array[i][start_energy:stop_energy]))
	return pfy


# plot a kind of average scaler
def plot_one_avg_scaler(mean_energy_array, scaler_array, name):
    
	plt.close('all')
	plt.scatter(mean_energy_array, scaler_array)
	plt.xlabel('Energy (eV)')
	plt.ylabel(['Average of',name])
	plt.show()


def plot_avg_xas_all(energy_array, scaler_array, pfy_data):
	
	print "Plotting XAS."    
	plt.close('all')

	en = energy_array
	tey = scaler_array[0]
	i0 = scaler_array[1]
	diode = scaler_array[2]

	plt.figure(1)
	plt.subplot(4, 2, 1)
	plt.plot(en, i0)
	# add lable for x and y axis
	plt.xlabel('Energy (eV)')
	plt.ylabel('I0')
    
	plt.subplot(4, 2, 2)
	plt.plot(en, tey)
	plt.xlabel('Energy (eV)')
	plt.ylabel('TEY')
    
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
    
    
def mca_division(mca_avg_array, dividend_mca, divisor_mca):
	# initial new_mca_array
	new_mca_array = []
	# initial a dict for 4 MCAs name
	dictionary = {'MCA1': 0, 'MCA2': 1, 'MCA3': 2, 'MCA4': 3}
	if dividend_mca == divisor_mca :
		print "Cannot division same MCAs"
	# calculate division
	else:
		dividend_mca_index = dictionary[dividend_mca]
		divisor_mca_index = dictionary[divisor_mca]
		for i in range (0, len(mca_avg_array[0])):
			divisor_value = mca_avg_array[divisor_mca_index][i]
			# print mca_avg_array[dividend_mca_index][i] / mca_avg_array[divisor_mca_index][i]
			new_mca_array.append( mca_avg_array[dividend_mca_index][i] / mca_avg_array[divisor_mca_index][i])

	return new_mca_array


def plot_mca_division(bins_mean_array, mca_avg_array, dividend_mca, divisor_mca, start_energy, end_energy):

	new_mca_array = mca_division(mca_avg_array, dividend_mca, divisor_mca)
	pfy_data = get_one_pfy_avg(new_mca_array, start_energy, end_energy)
	# print "x:", bins_mean_array
	# print "y:", pfy_data
	plt.plot(bins_mean_array, pfy_data)
	plt.xlabel('Energy (eV)')
	plt.ylabel('Value')
	plt.show()
    