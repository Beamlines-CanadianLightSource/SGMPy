import os
import numpy as np
from praxes.io import spec
from xas_process_para import XASProcessPara
from map_process_para import MapProcessPara
import time


# For Windows, Please use "/" instead of "\" in the file directory (URI)
def open_spec_data_file(file_directory):
    opened_file = spec.open(file_directory)
    return opened_file


def get_abs_path(rel_path):
    script_dir = os.path.dirname(os.path.realpath('__file__'))
    abs_path = os.path.join(script_dir, rel_path)
    print "File is at: ", abs_path
    return abs_path


def get_scan_details(file_directory):
    opened_file = open_spec_data_file(file_directory)
    scan_details_list = opened_file.keys()
    for i in range(0, len(scan_details_list)):
        labels = opened_file[scan_details_list[i]].attrs['labels']
        command = opened_file[scan_details_list[i]].attrs['command']
        date = opened_file[scan_details_list[i]].attrs['date']
        print 'Scan:', scan_details_list[i], '    The Command is: ', command, '    DateTime: ', date


def get_diff_scan(file_directory):
    opened_file = open_spec_data_file(file_directory)
    cmesh_array = []
    c_array = []
    a_array = []
    mesh_array = []

    for i in range(1, len(opened_file.keys()) + 1):
        # print "Scan No.", i
        scan_commmand_str = opened_file[opened_file.keys()[i - 1]].attrs['command']
        temp_array = scan_commmand_str.split()
        if temp_array[0] == "cmesh":
            cmesh_array.append(i)
        elif temp_array[0] == "cscan":
            c_array.append(i)
        elif temp_array[0] == "ascan":
            a_array.append(i)
        elif temp_array[0] == "mesh":
            mesh_array.append(i)
    print "C Scan: ", c_array, "\n"
    print "A Scan: ", a_array, "\n"
    print "C Mesh Scan: ", cmesh_array, "\n"
    print "Mesh Scan: ", mesh_array, "\n"
    return c_array, a_array, cmesh_array, mesh_array


def get_c_scan(opened_file):
    c_array = []
    for i in range(0, len(opened_file.keys())):
        index = opened_file.keys()[i]
        scan_commmand_str = opened_file[index].attrs['command']
        temp_array = scan_commmand_str.split()
        if temp_array[0] == "cscan" and len(opened_file[index]['Energy']) != 0:
            # print "Scan No.", i
            c_array.append(index)
    return c_array


def get_cmesh_scan(opened_file):
    cmesh_array = []
    for i in range(0, len(opened_file.keys())):
        index = opened_file.keys()[i]
        # print "Scan No.", i
        scan_commmand_str = opened_file[index].attrs['command']
        temp_array = scan_commmand_str.split()
        if temp_array[0] == "cmesh":
            scan_num_str = str(index)
            cmesh_array.append(scan_num_str)
    return cmesh_array


class OpenMultiCScan(object):

    def __init__(self):
        self.energy_array = None
        self.mca_array = None
        self.scaler_array = None
        self.c_scan_num = None
        self.file_direct = None

    def get_energy_array(self):
        return self.energy_array

    def set_energy_array(self, energy_array):
        self.energy_array = energy_array

    def get_mca_array(self):
        return self.mca_array

    def set_mca_array(self, mca_array):
        self.mca_array = mca_array

    def get_scaler_array(self):
        return self.scaler_array

    def set_scaler_array(self, scaler_array):
        self.scaler_array = scaler_array

    def get_c_scan(self):
        return self.c_scan_num

    def set_c_scan(self, c_scan_num):
        self.c_scan_num = c_scan_num

    def get_file_direct(self):
        return self.file_direct

    def set_file_direct(self, file_direct):
        self.file_direct = file_direct

    # open all scans of spectra
    def open_all_xas(self, file_directory):

        # start_time = time.time()
        print "Start opening c-scans."

        try:
            sgm_file = open_spec_data_file(file_directory)
        except IOError:
            print("No such file or directory:", file_directory)
            return None
        counter = 0
        c_scan_num = get_c_scan(sgm_file)
        total_scan_num = len(c_scan_num)

        scan=[]
        energy_array=[]
        mca_array = [[[],[],[],[]] for a in range(total_scan_num)]
        scaler_array = [[[],[],[]] for a in range(total_scan_num)]

        for j in range (0, total_scan_num):
            # print 'Scan index.', j+1
            # print "Scan number:", c_scan_num[j]

            scan.append(sgm_file[ c_scan_num[j] ])
            energy_array.append( scan[j]['Energy'])
            num_points = len(scan[j]['Energy'])
            # print num_points
            iteration_index1 = np.arange(0, num_points*4, 4)
            iteration_index2 = iteration_index1 + 1
            iteration_index3 = iteration_index1 + 2
            iteration_index4 = iteration_index1 + 3
            # print iteration_index1
            # print iteration_index2
            # print iteration_index3
            # print iteration_index4
            scaler_array[j][0] = scan[j]['TEY']
            scaler_array[j][1] = scan[j]['I0']
            scaler_array[j][2] = scan[j]['Diode']
            # print "scan[j]['@A1']: ", len(scan[j]['@A1'])
            mca_array[j][0] = list(scan[j]['@A1'][iteration_index1[0:]])
            mca_array[j][1] = list(scan[j]['@A1'][iteration_index2[0:]])
            mca_array[j][2] = list(scan[j]['@A1'][iteration_index3[0:]])
            mca_array[j][3] = list(scan[j]['@A1'][iteration_index4[0:]])
            counter += 1

            # print "Parsing MCAs"

            # for i in range(0,len(scan[j]['Energy'])):
            #     mca_array[j][0].append(mcadata[i*4])
            #     mca_array[j][1].append(mcadata[i*4 + 1])
            #     mca_array[j][2].append(mcadata[i*4 + 2])
            #     mca_array[j][3].append(mcadata[i*4 + 3])

        print "Opened ", counter, " c-scans.\n"
        self.set_energy_array(energy_array)
        self.set_mca_array(mca_array)
        self.set_scaler_array(scaler_array)
        self.set_c_scan(c_scan_num)
        self.set_file_direct(file_directory)
        estimate_xas_process_para = self.estimate_roi(file_directory, c_scan_num)
        # print("--- %s seconds ---" % (time.time() - start_time))
        return estimate_xas_process_para

    def estimate_roi(self, file_directory, scan_num):
        opened_file = open_spec_data_file(file_directory)
        string = opened_file[scan_num[0]].attrs['command']
        split_str = string.split(" ")

        # find min and max of scan energy
        if int(split_str[2]) > int(split_str[3]):
            start_energy = int(split_str[3])
            end_energy = int(split_str[2])
        else:
            start_energy = int(split_str[2])
            end_energy = int(split_str[3])
        medium_energy = (start_energy + end_energy) / 2
        medium_roi = medium_energy / 10
        roi_start = medium_roi - 8
        roi_end = medium_roi + 8

        print "estimate energy range: ", start_energy, "-", end_energy
        print "estimate roi: ", roi_start, "-", roi_end
        print "default bin interval: 0.1"

        estimate_xas_process_para = XASProcessPara(start_energy, end_energy, roi_start, roi_end, 0.1)
        return estimate_xas_process_para


class OpenSingleCScan(object):

    def __init__(self):
        self.energy_array = None
        self.mca_array = None
        self.scaler_array = None
        self.scan_num = None
        self.file_direct = None

    def get_energy_array(self):
        return self.energy_array

    def get_mca_array(self):
        return self.mca_array

    def get_scaler_array(self):
        return self.scaler_array

    def get_scan_num(self):
        return self.scan_num

    def get_file_direct(self):
        return self.file_direct

    # open a single scan of spectrum
    def open_single_xas(self, file_directory, scan_num):

        # start_time = time.time()

        print "Opening scan", str(scan_num)
        #print "in", file_directory

        f = spec.open(file_directory)
        scan=f[str(scan_num)]

        energy_array = scan['Energy']
        scaler_array = [[],[],[]]
        scaler_array[0] =  scan['TEY']
        scaler_array[1] =  scan['I0']
        scaler_array[2] =  scan['Diode']

        # mcadata = scan['@A1']
        print "Parsing MCAs"
        mca_array = [[],[],[],[]]

        num_points = len(energy_array)
        # print num_points
        iteration_index1 = np.arange(0, num_points * 4, 4)
        iteration_index2 = iteration_index1 + 1
        iteration_index3 = iteration_index1 + 2
        iteration_index4 = iteration_index1 + 3

        mca_array[0] = list(scan['@A1'][iteration_index1[0:]])
        mca_array[1] = list(scan['@A1'][iteration_index2[0:]])
        mca_array[2] = list(scan['@A1'][iteration_index3[0:]])
        mca_array[3] = list(scan['@A1'][iteration_index4[0:]])

        # for i in range(0,len(energy_array)):
        #     mca_array[0].append(mcadata[i*4])
        #     mca_array[1].append(mcadata[i*4 + 1])
        #     mca_array[2].append(mcadata[i*4 + 2])
        #     mca_array[3].append(mcadata[i*4 + 3])

        print "Done!"
        self.energy_array = energy_array
        self.mca_array = mca_array
        self.scaler_array = scaler_array
        self.scan_num = scan_num
        self.file_direct = file_directory
        # print("--- %s seconds ---" % (time.time() - start_time))


class OpenSingleCMesh(object):

    def __init__(self):
        self.hex_x = None
        self.hex_y = None
        self.mca_array = None
        self.scaler_array = None
        self.scan_num = None
        self.file_direct = None

    def get_hex_x(self):
        return self.hex_x

    def get_hex_y(self):
        return self.hex_y

    def get_mca_array(self):
        return self.mca_array

    def get_scaler_array(self):
        return self.scaler_array

    def get_scan_num(self):
        return self.scan_num

    def get_file_direct(self):
        return self.file_direct

    # open one scan of map
    def open_sgm_map(self, file_directory, scan_num):

        print ("Opening scan", str(scan_num))
        # print ("in", file_directory)

        f = spec.open(file_directory)
        scan=f[str(scan_num)]
        print scan.attrs['command']
        # command is like: mesh hex_xp 1.3 1.8 50 hex_yp 2.4 2.9 50 0.1
        temp = scan.attrs['command'].split(" ")

        if temp[0] == "cscan":
            print "Cannot open a cscan to plot map and this may cause the following error."
        elif temp[0] == "ascan":
            print "Cannot open a ascan to plot map and this may cause the following error."
        else:

            # find min and max of hex_xp and hex_yp
            if float(temp[2]) > float(temp[3]):
                x_start_energy = float(temp[3]) - 0.01
                x_end_energy = float(temp[2])  +0.01
            else:
                x_start_energy = float(temp[2]) - 0.01
                x_end_energy = float(temp[3])  +0.01

            if float(temp[6]) > float(temp[7]):
                y_start_energy =  float(temp[7]) - 0.01
                y_end_energy = float(temp[6]) + 0.01
            else:
                y_start_energy =  float(temp[6]) - 0.01
                y_end_energy = float(temp[7]) + 0.01

            hex_x = scan['Hex_XP']
            hex_y = scan['Hex_YP']

            scaler_array = [[],[],[]]
            scaler_array[0] =  scan['TEY']
            scaler_array[1] =  scan['I0']
            scaler_array[2] =  scan['Diode']

            print "Parsing MCAs"
            try:
                mcadata = scan['@A1']

                mca_array = [[],[],[],[]]

                num_points = len(scaler_array[0])
                # print num_points
                iteration_index1 = np.arange(0, num_points * 4, 4)
                iteration_index2 = iteration_index1 + 1
                iteration_index3 = iteration_index1 + 2
                iteration_index4 = iteration_index1 + 3

                mca_array[0] = list(scan['@A1'][iteration_index1[0:]])
                mca_array[1] = list(scan['@A1'][iteration_index2[0:]])
                mca_array[2] = list(scan['@A1'][iteration_index3[0:]])
                mca_array[3] = list(scan['@A1'][iteration_index4[0:]])

                # for i in range(0,len(hex_x)):
                #     mca_array[0].append(mcadata[i*4])
                #     mca_array[1].append(mcadata[i*4 + 1])
                #     mca_array[2].append(mcadata[i*4 + 2])
                #     mca_array[3].append(mcadata[i*4 + 3])

                print "Done!"
                self.hex_x = hex_x
                self.hex_y = hex_y
                self.mca_array = mca_array
                self.scaler_array = scaler_array
                self.scan_num = scan_num
                self.file_direct = file_directory

                estimate_xas_process_para = MapProcessPara(x_start_energy, x_end_energy, 0, y_start_energy, y_end_energy, 0)
                return estimate_xas_process_para
            except KeyError:
                print "This is an empty cmesh or mesh scan and this may cause the following error."