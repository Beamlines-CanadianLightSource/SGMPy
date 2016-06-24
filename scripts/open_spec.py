import os
from praxes.io import spec

# open one scan of map
def open_sgm_map(sgmFile, scanNum):

	print "Opening scan", str(scanNum)
	print "in", sgmFile

	f = spec.open(sgmFile)
	scan=f[str(scanNum)]

	hex_x = scan['Hex_XP']
	mcadata = scan['@A1']

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

# 
def open_all_sgm_map(opened_file):

	cmesh_scan = get_cmesh_scan(opened_file)
	total_scan_num = len(cmesh_scan)
    
	scan=[]
	mca1=[[] for a in range(total_scan_num)]
	mca2=[[] for a in range(total_scan_num)]
	mca3=[[] for a in range(total_scan_num)]
	mca4=[[] for a in range(total_scan_num)]    

	for j in range (0, total_scan_num):
		scan.append(opened_file[ cmesh_scan[j] ])

		hex_x = scan[j]['Hex_XP']
		mcadata = scan[j]['@A1']

		for i in range(0,len(hex_x)):
			mca1[j].append(mcadata[i*4])
			mca2[j].append(mcadata[i*4 + 1])
			mca3[j].append(mcadata[i*4 + 2])
			mca4[j].append(mcadata[i*4 + 3])

	print "Done!"
	return scan, mca1, mca2, mca3, mca4



# For Windows, Please use "/" instead of "\" in the file directory (URI)
def open_spec_data_file(file_directory):
	opened_file = spec.open(file_directory)
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

def get_diff_scan(opened_file):
	cmesh_array = []
	c_array = []
	a_array = []
	mesh_array = []
    
	for i in range (1, len(opened_file.keys())+1):
		# print "Scan No.", i
		scan_commmand_str =  opened_file[ opened_file.keys()[i-1] ].attrs['command']
		temp_array = scan_commmand_str.split( )
		if temp_array[0] == "cmesh":
			cmesh_array.append(i)
		elif temp_array[0] == "cscan":
			c_array.append(i)
		elif temp_array[0] == "ascan":
			a_array.append(i)
		elif temp_array[0] == "mesh":
			mesh_array.append(i)
	return c_array, a_array, cmesh_array, mesh_array


def get_cmesh_scan(opened_file):
	cmesh_array = []
	for i in range (1, len(opened_file.keys())+1):
		# print "Scan No.", i
		scan_commmand_str =  opened_file[ opened_file.keys()[i-1] ].attrs['command']
		temp_array = scan_commmand_str.split( )
		if temp_array[0] == "cmesh":
			scan_num_str = str(i)
			cmesh_array.append(scan_num_str)
	return cmesh_array


def get_c_scan(opened_file):
	c_array = []
	for i in range (0, len(opened_file.keys())):
		scan_commmand_str =  opened_file[ str(i+1) ].attrs['command']
		temp_array = scan_commmand_str.split( )
		if temp_array[0] == "cscan" and len(opened_file[str(i+1)]['Energy']) != 0 :
			# print "Scan No.", i
			scan_num_str = str(i+1)
			c_array.append(scan_num_str)
	return c_array


# open a specific scan of spectrum        
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

# open all scans of spectra
def open_all_sgm_xas(opened_file):
	counter = 0
	c_scan = get_c_scan(opened_file)
	total_scan_num = len(c_scan)
    
	# print "OriginalTotal scan: ", totalScanNum
	scan=[]
	mca1=[[] for a in range(total_scan_num)]
	mca2=[[] for a in range(total_scan_num)]
	mca3=[[] for a in range(total_scan_num)]
	mca4=[[] for a in range(total_scan_num)]
    
	for j in range (0, total_scan_num):
		# print 'index of the for loop is: ', j
		# print 'Scan No.', j+1
		# print c_scan[j]

		scan.append(opened_file[ c_scan[j] ])
		energy = scan[j]['Energy']
		mcadata = scan[j]['@A1']

		# print "Parsing MCAs"

		for i in range(0,len(energy)):
			mca1[j].append(mcadata[i*4])
			mca2[j].append(mcadata[i*4 + 1])
			mca3[j].append(mcadata[i*4 + 2])
			mca4[j].append(mcadata[i*4 + 3])
              
		# print "Done!"
	print "Opened all scans."
	return scan, mca1, mca2, mca3, mca4