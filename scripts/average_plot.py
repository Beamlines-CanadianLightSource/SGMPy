# Selection and Binning

from praxes.io import spec
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
from matplotlib.colors import colorConverter
import numpy as np
from scan_details import *
from basic_plot import *


# Eliminate bad scans and select good scans (data points)
def getGoodDataPoints(goodScanArray, fileDirectory):
	# initial arrays    
	scan=[]
	mca1=[]
	mca2=[]
	mca3=[]
	mca4=[]
    
	# open and read all data from the file and it could take a while
	scan, mca1, mca2, mca3, mca4 = openAllSGMXAS(fileDirectory)
    
	# Initial arrayOfPoints
	arrayOfPoints=[[[],[],[],[],[]] for i in range(len(goodScanArray))]
    
	for i in range (0, len(goodScanArray)):
		# scan number is start from 1
		# print "This is the scan number: ", goodScanArray[i]
		# array index is start from 0
		# get all scalers of good scans from original scans' array
		arrayOfPoints[i][0] = scan[goodScanArray[i]-1]
		# get all MCA1 of good scans from original scans
		arrayOfPoints[i][1] = mca1[goodScanArray[i]-1]
		# get all MCA2 of good scans from original scans
		arrayOfPoints[i][2] = mca2[goodScanArray[i]-1]
		# get all MCA3 of good scans from original scans
		arrayOfPoints[i][3] = mca3[goodScanArray[i]-1]
		# get all MCA4 of good scans from original scans
		arrayOfPoints[i][4] = mca4[goodScanArray[i]-1]
	return arrayOfPoints

# create bins (for testing startEnergy = 690, endEnergy = 750, numberOfBins = 120, energyArray = scan[goodScan_2[i]-1]['Energy'])
def createBins(startEnergy, endEnergy, numberOfEdges):
	energyRange = endEnergy - startEnergy
	print energyRange
	edges_array = np.linspace(startEnergy, endEnergy, numberOfEdges)
	return  edges_array


def AssignData (arrayOfPoints, edges):
	binNum = len(edges) - 1
	arrayOfBins = [[] for i in range(binNum)]

	# interation to assign data into bins
	binWidth = (edges[-1] - edges[0]) / binNum
	print "The width of a bin is:", binWidth
	print "Start assigning data points into bins" 
	for indexOfScan in range (0, len(arrayOfPoints)):
		for indexOfDataPoint in range (0, len(arrayOfPoints[indexOfScan][0]['Energy'])):
			x = arrayOfPoints[indexOfScan][0]['Energy'][indexOfDataPoint] - edges[0]
			# how to get integer part + 1?????
			assignBinNum = int (x / binWidth) + 1
			# print assignBinNum
			arrayOfBins[assignBinNum-1].append([indexOfScan,indexOfDataPoint])
	print "Assign data points completed"        
	return arrayOfBins

def calculateAvgMCA(arrayOfBins, arrayOfPoints):
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
			print
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
	return mca1AvgArray, mca2AvgArray, mca3AvgArray, mca4AvgArray


def calculateAvgOfScalers(arrayOfBins, arrayOfPoints):

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
			print
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
    
	return teyAvgArray, i0AvgArray, diodeAvgArray


def plotAvgOfMAC(binNum, avgMCA):
    
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


# plot a kind of average scaler
def plot_one_avg_scaler(mean_energy_array, scalerArray, name):
    
	# binNumArray = list(range(1, binNum + 1))
	# print binNumArray
	# print len(binNumArray)
    
	plt.scatter(mean_energy_array, scalerArray)
	plt.xlabel('Energy (eV)')
	plt.ylabel(['Average of',name])
	plt.show()
    
    
def getPFY_Avg(mcaAvgArray, enStart, enStop):

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


def plotAvgXAS_all(energyArray, scalerArray, pfyData):
	
	print "Plotting XAS."

	en = energyArray
	tey = scalerArray[0]
	i0 = scalerArray[1]
	diode = scalerArray[2]

	plt.figure(1)
	plt.subplot(241)
	plt.plot(en, i0)
	# add lable for x and y axis
	plt.xlabel('Energy (eV)')
	plt.ylabel('I0')
    
	plt.subplot(242)
	plt.plot(en, tey)
	plt.xlabel('Energy (eV)')
	plt.ylabel('TEY')
    
	plt.subplot(243)
	plt.plot(en, diode)
	plt.xlabel('Energy (eV)')
	plt.ylabel('Diode')

	plt.subplot(245)
	plt.plot(en, pfyData[0])
	plt.xlabel('Energy (eV)')
	plt.ylabel('MCA1')
    
	plt.subplot(246)
	plt.plot(en, pfyData[1])
	plt.xlabel('Energy (eV)')
	plt.ylabel('MCA2')
    
	plt.subplot(247)
	plt.plot(en, pfyData[2])
	plt.xlabel('Energy (eV)')
	plt.ylabel('MCA3')
    
	plt.subplot(248)
	plt.plot(en, pfyData[3])
	plt.xlabel('Energy (eV)')
	plt.ylabel('MCA4')
    
	figManager = plt.get_current_fig_manager()
	figManager.window.showMaximized()
	# tight_layout() will also adjust spacing between subplots to minimize the overlaps.
	plt.tight_layout()
	plt.show()
    