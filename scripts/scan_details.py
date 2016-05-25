# Open date file and get scan details

from praxes.io import spec
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np

# For Windows, Please use "/" instead of "\" in the file directory (URI)
def openDataFile(fileDirectory):
	file = spec.open(fileDirectory)
	return file

def getTotalScanNum(fileDirectory):
	OpenedFile = openDataFile(fileDirectory)
	totalScanNum = len(OpenedFile.keys())
	return totalScanNum
    
    
def getBasicScanDetails(fileDirectory):
	OpenedFile = openDataFile(fileDirectory)
	ScanDetailsList = OpenedFile.keys()
	for i in range(0,len(ScanDetailsList)):
		labels = OpenedFile[ScanDetailsList[i]].attrs['labels']
		command = OpenedFile[ScanDetailsList[i]].attrs['command']
		date = OpenedFile[ScanDetailsList[i]].attrs['date']
		print 'Scan:', ScanDetailsList[i], '    The Command is: ',command, '    DateTime: ', date
		print
        
        
def checkFileType(fileDirectory):
	OpenedFile = openDataFile(fileDirectory)
	scan = OpenedFile['1']
	keysList = scan.keys()
	# Iterate keys in the list
	for i in range(0,len(keysList)):
		if keysList[i] == 'Energy':
			return 'This is the data file of spectra.'
		elif keysList[i] == 'Hex_XP':
			return 'This is a map data file.'
	# It is a weird case, neither map nor spectra file
	return 'invalid data file!!!'


def check_scan_variety(fileDirectory):
	cmesh_array = []
	c_array = []
	a_array = []
	mesh_array = []
    
	OpenedFile = openDataFile(fileDirectory)
	for i in range (1, len(OpenedFile)+1):
		print "Scan No.", i
		string=str(i)
		string =  OpenedFile[string].attrs['command']
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
            