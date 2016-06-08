# Open date file and get scan details

from numpy import arange
from average_plot import *


def export_data(export_file_directory, origin_file_directory, mean_energy_array, name, avg_scaler=None, pfy_data=None):
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


def get_original_file_name(header_lines):
	str_file_name = header_lines[0]
	return str_file_name[3:]


def get_grating(header_lines):
	str_line_17 = header_lines[17]
	str_list = str_line_17.split()
	output = str_list[-2]+" "+str_list[-1]
	return output

def get_exit_slit(header_lines):
	str_line_18 = header_lines[18]
	str_list = str_line_18.split()
	output = str_list[8].rstrip(',')
	return output

def get_stripe(header_lines):
	str_line_18 = header_lines[18]
	str_list = str_line_18.split()
	output = str_list[-1].rstrip('.')
	return output
    
def export_pfy(export_file_directory, headers, mean_energy_array, sub_pfy, name):
	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		out_file.write("# Beamline.file-content: average ")
		out_file.write(name)
		out_file.write("\n# Beamline.origin-filename: ")
		str_origin_file_name = get_original_file_name(headers)
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		out_file.write("# Beamline.grating: ")
		str_grating = get_grating(headers)
		out_file.write(str_grating)
		out_file.write("\n# Beamline.stripe: ")
		str_stripe = get_stripe(headers)
		out_file.write(str_stripe)
		out_file.write("\n# Beamline.exit-slit: ")
		str_exit_slit = get_exit_slit(headers)
		out_file.write(str_exit_slit)
		out_file.write("\n# Time.start: ")
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
		out_file.write("\n# Beamline.origin-filename: ")
		str_origin_file_name = get_original_file_name(headers)
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		out_file.write("# Beamline.grating: ")
		str_grating = get_grating(headers)
		out_file.write(str_grating)
		out_file.write("\n# Beamline.stripe: ")
		str_stripe = get_stripe(headers)
		out_file.write(str_stripe)
		out_file.write("\n# Beamline.exit-slit: ")
		str_exit_slit = get_exit_slit(headers)
		out_file.write(str_exit_slit)
		out_file.write("\n# Time.start: ")
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


def export_eem(export_file_directory, origin_file_directory, mean_energy_array, emission_energy, color_variable, name):
	headers = get_header(origin_file_directory)
	with open(export_file_directory, "w") as out_file:
		out_file.write("# Beamline.file-content: ")
		out_file.write(name)
		out_file.write(" data from Excitation Emission Matrix\n")
		out_file.write("\n# Beamline.origin-filename: ")
		str_origin_file_name = get_original_file_name(headers)
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		out_file.write("# Beamline.grating: ")
		str_grating = get_grating(headers)
		out_file.write(str_grating)
		out_file.write("\n# Beamline.stripe: ")
		str_stripe = get_stripe(headers)
		out_file.write(str_stripe)
		out_file.write("\n# Beamline.exit-slit: ")
		str_exit_slit = get_exit_slit(headers)
		out_file.write(str_exit_slit)
		out_file.write("\n# Time.start: ")
		str_date_time = get_date_time(headers)
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")

		# write table header into the data file
		out_file.write("# Incident_Energy\t")
		out_file.write("Emission_Energy\t")
		out_file.write(name)
		out_file.write("\n")

		for i in range(0, len(mean_energy_array)):
			for j in range(0, len(emission_energy)):
				out_string = ""
				# print mean_energy_array[i]
				out_string += str(mean_energy_array[i])
				out_string += "\t"
				out_string += str(emission_energy[j])
				out_string += "\t"
				out_string += str(color_variable[i][j])
				# print sub_avg_scaler[i]
				out_string += "\n"
				# print out_string
				out_file.write(out_string)
                
                
def export_all (export_file_directory, origin_file_directory, mean_energy_array, avg_scaler, avg_pfy):
	headers = get_header(origin_file_directory)
	with open(export_file_directory, "w") as out_file:
		out_file.write("# Beamline.file-content: all data\n")
		out_file.write("\n# Beamline.origin-filename: ")
		str_origin_file_name = get_original_file_name(headers)
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		out_file.write("# Beamline.grating: ")
		str_grating = get_grating(headers)
		out_file.write(str_grating)
		out_file.write("\n# Beamline.stripe: ")
		str_stripe = get_stripe(headers)
		out_file.write(str_stripe)
		out_file.write("\n# Beamline.exit-slit: ")
		str_exit_slit = get_exit_slit(headers)
		out_file.write(str_exit_slit)
		out_file.write("\n# Time.start: ")
		str_date_time = get_date_time(headers)
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")
		# write table header into the data file
		out_file.write("# Energy\tTEY\tI0\tDiode\tPFY_SDD1\tPFY_SDD2\tPFY_SDD3\tPFY_SDD4\n")

		for i in range(0, len(mean_energy_array)):
			out_string = ""
			# print mean_energy_array[i]
			out_string += str(mean_energy_array[i])
			out_string += "\t"
			out_string += str(avg_scaler[0][i])
			out_string += "\t"
			out_string += str(avg_scaler[1][i])
			out_string += "\t"
			out_string += str(avg_scaler[2][i])
			out_string += "\t"
			out_string += str(avg_pfy[0][i])
			out_string += "\t"
			out_string += str(avg_pfy[1][i])
			out_string += "\t"
			out_string += str(avg_pfy[2][i])
			out_string += "\t"
			out_string += str(avg_pfy[3][i])
			# print sub_pfy[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)