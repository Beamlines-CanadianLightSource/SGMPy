# Present summary for all scans

from praxes.io import spec
import matplotlib.pyplot as plt
import numpy as np
from scan_details import *
from basic_plot import *

def generateSummaryPlot(fileDirectory):
	sgmData=openAllSGMXAS(fileDirectory)
	totalScanNumber = getTotalScanNum(fileDirectory)
	print "Total Scan Number is:", totalScanNumber
    
	for scanNum in range (0, totalScanNumber):
		scanNumList=np.empty(len(sgmData[0][scanNum]['Energy']))
		# scan number start from 1
		scanNumList.fill(scanNum+1)
		print "Generating plot for scan No.", scanNum+1
		plt.scatter(sgmData[0][scanNum]['Energy'], scanNumList, c=sgmData[0][scanNum]['TEY'],  s=5, linewidths=0)
		print "Generated plot for scan No.", scanNum+1, "completed"
    
	# add lable for x and y axis
	plt.xlabel('Incident Energy (ev)')
	plt.ylabel('Scan Numbers')
	# show the plot
	plt.show()

    
def getAllScanNum(fileDirectory):
	OpenedFile = openDataFile(fileDirectory)
	scanNumArray = OpenedFile.keys()
	# convert char(string) to integer
	scanNumArray = map(int, scanNumArray)
	return scanNumArray


def generateGoodScanArray(scanNumArray,badScanStr):
	print "These are the original scan numbers: ", scanNumArray
	print
	# split the array based on comma symbol
	badScanNumArray = badScanStr.split(',', )
	# convert char(string) to int
	badScanNumArray = map(int, badScanNumArray)
	print "These are bad scan numbers: ", badScanNumArray
	print
	# remove all the bad scan number from the original list
	for i in range (0, len(badScanNumArray)):
		scanNumArray.remove(badScanNumArray[i])

	print "These are all good scan numbers: ", scanNumArray
	goodScan = scanNumArray
	return goodScan
