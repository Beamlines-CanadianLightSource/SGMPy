# Open date file and get scan details

from numpy import arange
from average_plot import *


def export_data(export_file_directory, origin_file_directory, mean_energy_array, name, avg_scaler, pfy_data):
	headers = get_header(origin_file_directory)
	# MCA is SDD; after getting PFY of ROI then it becomes PFY_SDD
	pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
	scaler_dict = {'TEY': 0, 'I0': 1, 'Diode': 2}
    
	if name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
		sub_pfy_index = int(pfy_dict[name])
		export_pfy(export_file_directory, headers, mean_energy_array, pfy_data[sub_pfy_index], name)
		print "Export data complete!"

	elif name == "TEY" or name == "I0" or name == "Diode":
		sub_scaler_index = scaler_dict[name]
		export_scaler(export_file_directory, headers, mean_energy_array, avg_scaler[sub_scaler_index], name)
		print "Export data complete!"

	else:
		print "Unable to export data."


def get_header(file_directory):
	with open(file_directory) as content:
		lines = content.readlines()
	return lines[:19]

def get_date_time(header_lines):
	str_date_time = header_lines[2]
	print str_date_time[3:]
	return str_date_time[3:]
    

def export_pfy(export_file_directory, headers, mean_energy_array, sub_pfy, name):
	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		out_file.write("# Beamline.file-content: average ")
		out_file.write(name)
		out_file.write("\n")
		out_file.write("# Beamline.name: SGM\n")
		out_file.write("# Beamline.grating: Medium Energy\n")
		out_file.write("# Time.start: ")
		str_date_time = get_date_time(headers)
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")
    
		# write table header into the data file
		out_file.write("# Energy\t")
		out_file.write(name)
		out_file.write("\n")
    
		for i in range(0, len(mean_energy_array)):
			out_string = ""
			# print mean_energy_array[i]
			out_string += str(mean_energy_array[i])
			out_string += "\t"
			out_string += str(sub_pfy[i])
			# print sub_pfy[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)


def export_scaler(export_file_directory, headers, mean_energy_array, sub_avg_scaler, name):
	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		out_file.write("# Beamline.file-content: average ")
		out_file.write(name)
		out_file.write("\n")
		out_file.write("# Beamline.name: SGM\n")
		out_file.write("# Beamline.grating: Medium Energy\n")
		out_file.write("# Time.start: ")
		str_date_time = get_date_time(headers)
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")
    
		# write table header into the data file
		out_file.write("# Energy\t")
		out_file.write(name)
		out_file.write("\n")
    
		for i in range(0, len(mean_energy_array)):
			out_string = ""
			# print mean_energy_array[i]
			out_string += str(mean_energy_array[i])
			out_string += "\t"
			out_string += str(sub_avg_scaler[i])
			# print sub_avg_scaler[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)