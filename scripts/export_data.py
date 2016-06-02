# Open date file and get scan details

from numpy import arange
from average_plot import *


def export_data(file_directory, mean_energy_array, name, avg_scaler, pfy_data):
	headers = get_header(file_directory)
	mca_dict = {'MCA1': 0, 'MCA2': 1, 'MCA3': 2, 'MCA4': 3}
	scaler_dict = {'TEY': 0, 'I0': 1, 'Diode': 2}
    
	if name == "MCA1" or name == "MCA2" or name == "MCA3" or name == "MCA4":
		sub_pfy_index = int(mca_dict[name])
		export_pfy(headers, mean_energy_array, pfy_data[sub_pfy_index], name)
		print "Export data complete!"

	elif name == "TEY" or name == "I0" or name == "Diode":
		sub_scaler_index = scaler_dict[name]
		export_scaler(headers, mean_energy_array, avg_scaler[sub_scaler_index], name)
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
    

def export_pfy(headers, mean_energy_array, sub_pfy, name):
	with open("output_data.xas", "w") as out_file:
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


def export_scaler(headers, mean_energy_array, sub_avg_scaler, name):
	with open("output_data1.xas", "w") as out_file:
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