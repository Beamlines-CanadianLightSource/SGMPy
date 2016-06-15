import os
from praxes.io import spec


def openSGMSpec(sgmFile, scanNum):

	print "Opening scan", str(scanNum)
	print "in", sgmFile

	f = spec.open(sgmFile)
	scan=f[str(scanNum)]

	hex_x = scan['Hex_XP']
	mcadata=scan['@A1']

	print "Parsing MCAs"

	mca1=[]
	mca2=[]
	mca3=[]
	mca4=[]

	for i in range(0,len(hex_x)):
		mca1.append(mcadata[i*4])
		mca2.append(mcadata[i*4 + 1])
		mca3.append(mcadata[i*4 + 2])
		mca4.append(mcadata[i*4 + 3])

	print "Done!"
	return scan, mca1, mca2, mca3, mca4


# For Windows, Please use "/" instead of "\" in the file directory (URI)
def open_spec_data_file(file_directory):
	opened_file = spec.open(file_directory)
	return opened_file

def get_all_scan_num(opened_file):
	scan_num_array = opened_file.keys()
	# convert char(string) to integer
	scan_num_array = map(int, scan_num_array)
	return scan_num_array


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
        
        
def openSGMXAS(sgmFile, scanNum):

	print "Opening scan", str(scanNum)
	print "in", sgmFile

	f = spec.open(sgmFile)
	scan=f[str(scanNum)]

	energy = scan['Energy']	

	mcadata=scan['@A1']

	print "Parsing MCAs"

	mca1=[]
	mca2=[]
	mca3=[]
	mca4=[]

	for i in range(0,len(energy)):
		mca1.append(mcadata[i*4])
		mca2.append(mcadata[i*4 + 1])
		mca3.append(mcadata[i*4 + 2])
		mca4.append(mcadata[i*4 + 3])

	print "Done!"
	return scan, mca1, mca2, mca3, mca4


def openAllSGMXAS(opened_file):
	totalScanNum = len(opened_file.keys())
	# print "OriginalTotal scan: ", totalScanNum
	scan=[]
	mca1=[[] for a in range(totalScanNum)]
	mca2=[[] for a in range(totalScanNum)]
	mca3=[[] for a in range(totalScanNum)]
	mca4=[[] for a in range(totalScanNum)]
    
	for j in range (0, totalScanNum):
		# print 'index of the for loop is: ', j
		# print 'Scan No.', j+1
		scan.append(opened_file[str(j+1)])
		energy = scan[j]['Energy']	
		mcadata=scan[j]['@A1']

		# print "Parsing MCAs"

		for i in range(0,len(energy)):
			mca1[j].append(mcadata[i*4])
			mca2[j].append(mcadata[i*4 + 1])
			mca3[j].append(mcadata[i*4 + 2])
			mca4[j].append(mcadata[i*4 + 3])
              
		# print "Done!"
	print "Opened all scans."
	return scan, mca1, mca2, mca3, mca4