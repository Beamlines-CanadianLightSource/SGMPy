# Open date file and get scan details

from numpy import arange
from open_spec import *
import h5py
import numpy as np

def export_data(export_file_directory, origin_file_directory, energy_array, name, scaler_data=None, pfy_data=None, scan_number=None):

	# MCA is SDD; after getting PFY of ROI then it becomes PFY_SDD
	pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
	scaler_dict = {'TEY': 0, 'I0': 1, 'Diode': 2}
    
	if name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
		sub_pfy_index = int(pfy_dict[name])
		export_pfy(export_file_directory, origin_file_directory, energy_array, pfy_data[sub_pfy_index], name, scan_number)
		print "Export data complete!"

	elif name == "TEY" or name == "I0" or name == "Diode":
		sub_scaler_index = scaler_dict[name]
		export_scaler(export_file_directory, origin_file_directory, energy_array, scaler_data[sub_scaler_index], name, scan_number)
		print "Export data complete!"

	else:
		print "Unable to export data."


def get_date_time(opened_file):
	str_date_time = opened_file['1'].attrs['file_date']
	return str_date_time[4:]


#def get_original_file_name(opened_file):
#	str_file_name = opened_file['1'].attrs['file_origin']
#	return str_file_name[3:]


def get_comments(file_directory):
	with open(file_directory) as content:
		lines = content.readlines()
		temp = lines[:40]
		comments = []
		for i in range (0, 40):
			if temp[i][:2] == '#C':
				comments.append(temp[i])
	return comments


def get_comment_details(comments):
	split_comma = []
	split_dot = []
	for i in range(0, len(comments)):
		split_comma.append(comments[i].split(','))      
	for i in range(0, len(split_comma)):
		for j in range(0, len(split_comma[i])):
			split_dot.append(split_comma[i][j].split(':'))
            
	for i in range (0, len(split_dot)):
		if split_dot[i][0] == ' Grating':
			grating = split_dot[i][1].strip()
			exit_slit = split_dot[i+1][-1].strip()
			stripe = split_dot[i+2][-1].strip()
	return grating[:-1], exit_slit, stripe[:-1]


def get_header_hdf5(file_directory):
	with h5py.File(file_directory,'r') as hf:
		comments = hf.get('S1/comments')
		comments = np.array(comments)
		date = hf.get('S1/date')
		date = np.array(date)[0]
	return comments, date

def get_grating_hdf5(comments):
	parsed_str = comments[0].split('\n')
	grating_str = [x.strip() for x in parsed_str[1].split(",")]
	print grating_str[-1]
	return grating_str[-1][9:-1]    


def get_exit_slit_and_stripe(comments):
	parsed_str = comments[0].split('\n')
	parsed_str_length = len(parsed_str)
	if parsed_str_length == 2:
		temp_str = [x.strip() for x in parsed_str[1].split(",")]
		print temp_str[-2]
		temp_str_2 = [x.strip() for x in temp_str[-2].split(":")]
		exit_slit_str = temp_str_2[-1]    
		stripe_str = temp_str[-1][7:-1]
	else:
		temp_str = [x.strip() for x in parsed_str[2].split(",")]
		print temp_str[-2]
		temp_str_2 = [x.strip() for x in temp_str[-2].split(":")]
		exit_slit_str = temp_str_2[-1]    
		stripe_str = temp_str[-1][7:-1]
    
	return exit_slit_str, stripe_str

def check_file_type(origin_file_directory):
	file_directory = origin_file_directory.split('.')
	file_extension = file_directory[-1]
	file_name = file_directory[0].split('/')[-1]
	return file_extension, file_name

    
def export_pfy(export_file_directory, origin_file_directory, energy_array, sub_pfy, name, scan_number=None):
	file_extension, original_file_name = check_file_type(origin_file_directory)
	if file_extension == "dat":
		opened_file = open_spec_data_file(origin_file_directory)
		date = get_date_time(opened_file)
		comments = get_comments(origin_file_directory)
		grating, exit_slit, stripe = get_comment_details(comments)
	else:
		comments, date = get_header_hdf5(origin_file_directory)
		grating = get_grating_hdf5(comments)
		exit_slit, stripe = get_exit_slit_and_stripe(comments)
		# date = date[0]

	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		if scan_number== None:
			out_file.write("# Beamline.file-content: binned and averaged " + name + "\n")
		else:
			out_file.write("# Beamline.file-content: " + name + "of scan No." + scan_number + "\n")
		str_origin_file_name = "# Beamline.origin-filename: " + original_file_name + "\n"
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		str_grating = "# Beamline.grating: " + grating + "\n"
		out_file.write(str_grating)
		str_stripe = "# Beamline.stripe: " + stripe + "\n"
		out_file.write(str_stripe)
		str_exit_slit = "# Beamline.exit-slit: " + exit_slit + "\n"
		out_file.write(str_exit_slit)
		str_date_time = "# Time.start: " + date + "\n"
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")
    
		# write table header into the data file
		out_file.write("# Energy\t")
		out_file.write(name)
		out_file.write("\n")
    
		for i in range(0, len(energy_array)):
			out_string = ""
			# print energy_array[i]
			out_string += str(energy_array[i])
			out_string += "\t"
			out_string += str(sub_pfy[i])
			# print sub_pfy[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)


def export_scaler(export_file_directory, origin_file_directory, energy_array, sub_scaler, name, scan_number=None):
	file_extension, original_file_name = check_file_type(origin_file_directory)
	if file_extension == "dat":
		opened_file = open_spec_data_file(origin_file_directory)
		date = get_date_time(opened_file)
		comments = get_comments(origin_file_directory)
		grating, exit_slit, stripe = get_comment_details(comments)
	else:
		comments, date = get_header_hdf5(origin_file_directory)
		grating = get_grating_hdf5(comments)
		exit_slit, stripe = get_exit_slit_and_stripe(comments)
		# date = date[0]

	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		if scan_number== None:
			out_file.write("# Beamline.file-content: binned and averaged " + name + "\n")
		else:
			out_file.write("# Beamline.file-content: " + name + "of scan No." + scan_number + "\n")
		str_origin_file_name = "# Beamline.origin-filename: " + original_file_name + "\n"
		str_origin_file_name = "# Beamline.origin-filename: " + original_file_name + "\n"
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		str_grating = "# Beamline.grating: " + grating + "\n"
		out_file.write(str_grating)
		str_stripe = "# Beamline.stripe: " + stripe + "\n"
		out_file.write(str_stripe)
		str_exit_slit = "# Beamline.exit-slit: " + exit_slit + "\n"
		out_file.write(str_exit_slit)
		str_date_time = "# Time.start: " + date + "\n"
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")
    
		# write table header into the data file
		out_file.write("# Energy\t")
		out_file.write(name)
		out_file.write("\n")
    
		for i in range(0, len(energy_array)):
			out_string = ""
			# print energy_array[i]
			out_string += str(energy_array[i])
			out_string += "\t"
			out_string += str(sub_scaler[i])
			# print sub_scaler[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)


#def export_eem(export_file_directory, origin_file_directory, energy_array, emission_energy, color_variable, name):
#	headers = get_header(origin_file_directory)
#	with open(export_file_directory, "w") as out_file:
#		out_file.write("# Beamline.file-content: " + name + " data from Excitation Emission Matrix\n")
#		str_origin_file_name = "# Beamline.origin-filename: " + get_original_file_name(headers)
#		out_file.write(str_origin_file_name)
#		out_file.write("# Beamline.name: SGM\n")
#		str_grating = "# Beamline.grating: " + get_grating(headers) + "\n"
#		out_file.write(str_grating)
#		str_stripe = "# Beamline.stripe: " + get_stripe(headers) + "\n"
#		out_file.write(str_stripe)
#		str_exit_slit = "# Beamline.exit-slit: " + get_exit_slit(headers) + "\n"
#		out_file.write(str_exit_slit)
#		str_date_time = "# Time.start: " + get_date_time(headers)
#		out_file.write(str_date_time)
#		out_file.write("#-----------------------------------------------------------\n")
#
#		# write table header into the data file
#		out_file.write("# Incident_Energy\t")
#		out_file.write("Emission_Energy\t")
#		out_file.write(name)
#		out_file.write("\n")
#
#		for i in range(0, len(energy_array)):
#			for j in range(0, len(emission_energy)):
#				out_string = ""
#				# print energy_array[i]
#				out_string += str(energy_array[i])
#				out_string += "\t"
#				out_string += str(emission_energy[j])
#				out_string += "\t"
#				out_string += str(color_variable[i][j])
#				# print sub_scaler[i]
#				out_string += "\n"
#				# print out_string
#				out_file.write(out_string)
#	print ("Export data complete.")
                
                
def export_all (export_file_directory, origin_file_directory, energy_array, scaler_data, pfy_data, scan_number=None):
	file_extension, original_file_name = check_file_type(origin_file_directory)
	if file_extension == "dat":
		opened_file = open_spec_data_file(origin_file_directory)
		date = get_date_time(opened_file)
		comments = get_comments(origin_file_directory)
		grating, exit_slit, stripe = get_comment_details(comments)
	else:
		comments, date = get_header_hdf5(origin_file_directory)
		grating = get_grating_hdf5(comments)
		exit_slit, stripe = get_exit_slit_and_stripe(comments)

	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		if scan_number== None:
			out_file.write("# Beamline.file-content: all data\n")
		else:
			out_file.write("# Beamline.file-content: all data of scan No." + scan_number + "\n")
		str_origin_file_name = "# Beamline.origin-filename: " + original_file_name + "\n"
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		str_grating = "# Beamline.grating: " + grating + "\n"
		out_file.write(str_grating)
		str_stripe = "# Beamline.stripe: " + stripe + "\n"
		out_file.write(str_stripe)
		str_exit_slit = "# Beamline.exit-slit: " + exit_slit + "\n"
		out_file.write(str_exit_slit)
		str_date_time = "# Time.start: " + date + "\n"
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")

        # write table header into the data file
		out_file.write("# Energy\tTEY\tI0\tDiode\tPFY_SDD1\tPFY_SDD2\tPFY_SDD3\tPFY_SDD4\n")
		for i in range(0, len(energy_array)):
			out_string = ""
			# print energy_array[i]
			out_string += str(energy_array[i])
			out_string += "\t"
			out_string += str(scaler_data[0][i])
			out_string += "\t"
			out_string += str(scaler_data[1][i])
			out_string += "\t"
			out_string += str(scaler_data[2][i])
			out_string += "\t"
			out_string += str(pfy_data[0][i])
			out_string += "\t"
			out_string += str(pfy_data[1][i])
			out_string += "\t"
			out_string += str(pfy_data[2][i])
			out_string += "\t"
			out_string += str(pfy_data[3][i])
			# print sub_pfy[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)
	print ("Export data complete.")
            
        
def export_normalized_data(export_file_directory, origin_file_directory, column1, column2, column1_name, column2_name):
	file_extension, original_file_name = check_file_type(origin_file_directory)
	if file_extension == "dat":
		opened_file = open_spec_data_file(origin_file_directory)
		date = get_date_time(opened_file)
		comments = get_comments(origin_file_directory)
		grating, exit_slit, stripe = get_comment_details(comments)
	else:
		comments, date = get_header_hdf5(origin_file_directory)
		grating = get_grating_hdf5(comments)
		exit_slit, stripe = get_exit_slit_and_stripe(comments)

	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		out_file.write("# Beamline.file-content: Normalized " + column2_name + "\n")
		str_origin_file_name = "# Beamline.origin-filename: " + original_file_name + "\n"
		out_file.write(str_origin_file_name)
		out_file.write("# Beamline.name: SGM\n")
		str_grating = "# Beamline.grating: " + grating + "\n"
		out_file.write(str_grating)
		str_stripe = "# Beamline.stripe: " + stripe + "\n"
		out_file.write(str_stripe)
		str_exit_slit = "# Beamline.exit-slit: " + exit_slit + "\n"
		out_file.write(str_exit_slit)
		str_date_time = "# Time.start: " + date + "\n"
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")
		# write table header into the data file
		string_table_header = "# "+ column1_name + "\t" + column2_name + "\n"
		out_file.write(string_table_header)
		for i in range(0, len(column1)):
			out_string = ""
			# print energy_array[i]
			out_string += str(column1[i])
			out_string += "\t"
			out_string += str(column2[i])
			# print sub_pfy[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)
	print ("Export data complete.")

def export_map_all(export_file_directory, origin_file_directory, hex_xp_data, hex_yp_data, scaler_data, pfy_data, scan_number=None):
	file_extension, original_file_name = check_file_type(origin_file_directory)
	if file_extension == "dat":
		opened_file = open_spec_data_file(origin_file_directory)
		date = get_date_time(opened_file)
		comments = get_comments(origin_file_directory)
		grating, exit_slit, stripe = get_comment_details(comments)
	else:
		comments, date = get_header_hdf5(origin_file_directory)
		grating = get_grating_hdf5(comments)
		exit_slit, stripe = get_exit_slit_and_stripte(comments)
	with open(export_file_directory, "w") as out_file:
		# write header into the data file
		out_file.write("# Beamline.name: SGM\n")
		str_origin_file_name = "# Beamline.origin-filename: " + original_file_name + "\n"
		if scan_number== None:
			out_file.write("# Beamline.file-content: all data\n")
		else:
			out_file.write("# Beamline.file-content: all data of scan No." + scan_number + "\n")
		out_file.write(str_origin_file_name)
		str_grating = "# Beamline.grating: " + grating + "\n"
		out_file.write(str_grating)
		str_stripe = "# Beamline.stripe: " + stripe + "\n"
		out_file.write(str_stripe)
		str_exit_slit = "# Beamline.exit-slit: " + exit_slit + "\n"
		out_file.write(str_exit_slit)
		str_date_time = "# Time.start: " + date + "\n"
		out_file.write(str_date_time)
		out_file.write("#-----------------------------------------------------------\n")
        # write table header into the data file
		out_file.write("# Hex_XP\tHex_YP\tTEY\tI0\tDiode\tPFY_SDD1\tPFY_SDD2\tPFY_SDD3\tPFY_SDD4\n")
		for i in range(0, len(hex_xp_data)):
			out_string = ""
			# print energy_array[i]
			out_string += str(hex_xp_data[i]) + "\t"
			# out_string += "\t"
			out_string += str(hex_yp_data[i])
			out_string += "\t"
			out_string += str(scaler_data[0][i])
			out_string += "\t"
			out_string += str(scaler_data[1][i])
			out_string += "\t"
			out_string += str(scaler_data[2][i])
			out_string += "\t"
			out_string += str(pfy_data[0][i])
			out_string += "\t"
			out_string += str(pfy_data[1][i])
			out_string += "\t"
			out_string += str(pfy_data[2][i])
			out_string += "\t"
			out_string += str(pfy_data[3][i])
			# print sub_pfy[i]
			out_string += "\n"
			# print out_string
			out_file.write(out_string)
	print ("Export data complete.")