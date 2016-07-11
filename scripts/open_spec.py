import os
from praxes.io import spec

# open one scan of map
def open_sgm_map(sgm_file, scan_num):

	print "Opening scan", str(scan_num)
	print "in", sgm_file

	f = spec.open(sgm_file)
	scan=f[str(scan_num)]

	hex_x = scan['Hex_XP']
	hex_y = scan['Hex_YP']

	scaler_array = [[],[],[]]
	scaler_array[0] =  scan['TEY']
	scaler_array[1] =  scan['I0']
	scaler_array[2] =  scan['Diode']
    
	print "Parsing MCAs"
	mcadata = scan['@A1']
	mca_array = [[],[],[],[]]

	for i in range(0,len(hex_x)):
		mca_array[0].append(mcadata[i*4])
		mca_array[1].append(mcadata[i*4 + 1])
		mca_array[2].append(mcadata[i*4 + 2])
		mca_array[3].append(mcadata[i*4 + 3])

	print "Done!"
	return hex_x, hex_y, mca_array, scaler_array, scan_num

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
	for i in range (0, len(opened_file.keys())):
		index = opened_file.keys()[i] 
		# print "Scan No.", i
		scan_commmand_str =  opened_file[index].attrs['command']
		temp_array = scan_commmand_str.split( )
		if temp_array[0] == "cmesh":
			scan_num_str = str(index)
			cmesh_array.append(scan_num_str)
	return cmesh_array


def get_c_scan(opened_file):
	c_array = []
	for i in range (0, len(opened_file.keys())):
		index = opened_file.keys()[i] 
		scan_commmand_str =  opened_file[index].attrs['command']
		temp_array = scan_commmand_str.split( )
		if temp_array[0] == "cscan" and len(opened_file[index]['Energy']) != 0 :
			# print "Scan No.", i
			c_array.append(index)
	return c_array


# open a specific scan of spectrum        
def open_sgm_xas(sgm_file, scan_num):

	print "Opening scan", str(scan_num)
	print "in", sgm_file

	f = spec.open(sgm_file)
	scan=f[str(scan_num)]

	energy_array = scan['Energy']
	scaler_array = [[],[],[]]
	scaler_array[0] =  scan['TEY']
	scaler_array[1] =  scan['I0']
	scaler_array[2] =  scan['Diode']
    
	mcadata = scan['@A1']
	print "Parsing MCAs"
	mca_array = [[],[],[],[]]
	for i in range(0,len(energy_array)):
		mca_array[0].append(mcadata[i*4])
		mca_array[1].append(mcadata[i*4 + 1])
		mca_array[2].append(mcadata[i*4 + 2])
		mca_array[3].append(mcadata[i*4 + 3])

	print "Done!"
	return energy_array, mca_array, scaler_array

# open all scans of spectra
def open_all_sgm_xas(sgm_file):
	counter = 0
	c_scan = get_c_scan(sgm_file)
	total_scan_num = len(c_scan)
    
	# print "OriginalTotal scan: ", total_scan_num
	scan=[]
	energy_array=[]
	mca_array = [[[],[],[],[]] for a in range(total_scan_num)]

	scaler_array = [[[],[],[]] for a in range(total_scan_num)]
	for j in range (0, total_scan_num):
		# print 'index of the for loop is: ', j
		print 'Scan No.', j+1
		print c_scan[j]

		scan.append(sgm_file[ c_scan[j] ])
		energy_array.append( scan[j]['Energy'])
		scaler_array[j][0] = scan[j]['TEY']
		scaler_array[j][1] = scan[j]['I0']
		scaler_array[j][2] = scan[j]['Diode']
		mcadata = scan[j]['@A1']

		# print "Parsing MCAs"

		for i in range(0,len(scan[j]['Energy'])):
			mca_array[j][0].append(mcadata[i*4])
			mca_array[j][1].append(mcadata[i*4 + 1])
			mca_array[j][2].append(mcadata[i*4 + 2])
			mca_array[j][3].append(mcadata[i*4 + 3])
              
		# print "Done!"
	print "Opened all scans."
	return energy_array, mca_array, scaler_array, c_scan