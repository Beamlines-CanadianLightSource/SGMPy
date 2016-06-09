# Present summary for all scans

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import matplotlib

matplotlib.use('agg')
from scan_details import *
from basic_plot import *


def summary_plot(opened_file, name, start_energy=None, stop_energy=None):
	# mandetory to close all the existing matplot figures
	plt.close('all')
	scan_array = check_scan_variety(opened_file)
	cscan_array = scan_array[0]
	print "C Scan are including: ", cscan_array
	sgm_data=openAllSGMXAS(opened_file)
    
	if name == "TEY" or name == "I0" or name == "Diode" or name == "SDD1_OCR" or name == "SDD1_ICR" or name == "SDD2_OCR" or name == "SDD2_ICR" or name == "SDD3_OCR" or name == "SDD3_ICR" or name == "SDD4_OCR" or name == "SDD4_ICR":
		generate_summary_plot_with_scaler(cscan_array, sgm_data, name)
	elif name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
		generate_summary_plot_with_pfy(cscan_array, sgm_data, name, start_energy, stop_energy)
	else:
		print "Errors with the name input"
	return cscan_array


def generate_summary_plot_with_pfy(cscan_array, sgm_data, pfy_name, start_energy, stop_energy):
        
	# MCA is SDD; after getting PFY of ROI then it becomes PFY_SDD
	pfy_dict = {'PFY_SDD1': 'MCA1', 'PFY_SDD2': 'MCA2', 'PFY_SDD3': 'MCA3', 'PFY_SDD4': 'MCA4'}
	mca_dict = {'MCA1': 0, 'MCA2': 1, 'MCA3': 2, 'MCA4': 3}
	mca_name = pfy_dict[pfy_name]
	mca = mca_dict[mca_name]
         
	str_scaler_name = mca_name
	total_cscan_num = len(cscan_array)
	for index in range (0, total_cscan_num):
		real_cscan_number = cscan_array[index]
		cscan_index = real_cscan_number - 1
		scanNumList=np.empty(len(sgm_data[0][cscan_index]['Energy']))
		scanNumList.fill(real_cscan_number)
        
		energy_array = sgm_data[0][cscan_index]['Energy']
		total_pfy = get_one_pfy_from_all_scan(sgm_data, mca_name, start_energy, stop_energy)

		#print "Generating plot for scan No.", real_cscan_number
		plt.scatter(energy_array, scanNumList, c=total_pfy[cscan_index],  s=140, linewidths=0, marker='s')
		print "Generated plot for scan No.", real_cscan_number
	# setup the y-axis ticks
	#plt.ylim(0, total_cscan_num+1)
	plt.yticks(np.arange(0+1, total_cscan_num+1, 1.0))
	# add lable for x and y axis
	plt.xlabel('Incident Energy (eV)')
	plt.ylabel('Scan Numbers')
	plt.colorbar()
	plt.title(['color is :', str_scaler_name])
	y_axis_height = total_cscan_num * 0.25
	# change the figure configuration
	fig = plt.gcf()
	fig.set_size_inches(11, y_axis_height)
	plt.grid()
	# show the plot
	plt.show()


def generate_summary_plot_with_scaler(cscan_array, sgm_data, scaler_name):
	str_scaler_name = scaler_name
	total_cscan_num = len(cscan_array)
	for index in range (0, total_cscan_num):
		real_cscan_number = cscan_array[index]
		cscan_index = real_cscan_number - 1
		scanNumList=np.empty(len(sgm_data[0][cscan_index]['Energy']))
		# create a list including all the scan number
		scanNumList.fill(real_cscan_number)
		# print "Generating plot for scan No.", real_cscan_number
		plt.scatter(sgm_data[0][cscan_index]['Energy'], scanNumList, c=sgm_data[0][cscan_index][str_scaler_name],  s=140, linewidths=0, marker='s')
		print "Generated plot for scan No.", real_cscan_number
	# setup the y-axis ticks
	# plt.ylim(0, total_cscan_num+1)
	plt.yticks(np.arange(0+1, total_cscan_num+1, 1.0))
	# add lable for x and y axis
	plt.xlabel('Incident Energy (eV)')
	plt.ylabel('Scan Numbers')
	plt.colorbar()
	plt.title(['color is :', str_scaler_name])
	y_axis_height = total_cscan_num * 0.25
	# change the figure configuration
	fig = plt.gcf()
	fig.set_size_inches(11, y_axis_height)
	plt.grid()
	# show the plot
	plt.show()

    
def get_all_scan_num(opened_file):
	scan_num_array = opened_file.keys()
	# convert char(string) to integer
	scan_num_array = map(int, scan_num_array)
	return scan_num_array


def generate_good_scan_array(scan_num_array, bad_scan_str):
	print "These are the original scan numbers: ", scan_num_array
	print
	# if badScanStr is null, then return original arrays
	if bad_scan_str == '':
		return scan_num_array
	# to get good scan numbers
	else:
		# split the array based on comma symbol
		bad_scan_num_array = bad_scan_str.split(',', )
		# convert char(string) to int
		bad_scan_num_array = map(int, bad_scan_num_array)
		print "These are bad scan numbers: ", bad_scan_num_array
		print
		# remove all the bad scan number from the original list
		for i in range (0, len(bad_scan_num_array)):
			scan_num_array.remove(bad_scan_num_array[i])

		print "These are all good scan numbers: ", scan_num_array
		good_scan = scan_num_array
		return good_scan

    
def get_one_pfy_from_all_scan(sgm_data, mca_name, enStart, enStop):

	if mca_name == "MCA1":
		mca = 1
	elif mca_name == "MCA2":
		mca = 2
	elif mca_name == "MCA3":
		mca = 3
	elif mca_name == "MCA4":
		mca = 4    
	else:
		print "Error!!!"
    
	print "Getting PFY ROIs for", mca_name

	pfy=[[] for i in range(len(sgm_data[1]) )]
	for i in range(0, len(sgm_data[mca])):
		for j in range(0, len(sgm_data[mca][i])):
			pfy[i].append(np.sum(sgm_data[mca][i][j][enStart:enStop]))
		# print "Length of PFY:", len(pfy[i])
		# print "Length of Energy", sgm_data[0][i]['Energy']
	print "Done!"   
	return pfy    
    