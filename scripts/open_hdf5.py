import numpy as np
import h5py
from xas_process_para import XASProcessPara

# def get_all_scan_num_hdf5(file_directory):
#     with h5py.File(file_directory,'r') as hf:
#         scan_num_array = map(str, hf.keys())
#         scan_num_array = get_number(scan_num_array)
#         scan_num_array = map(int, scan_num_array)
#         return scan_num_array
#
# def get_number(scan_num_array):
#     for i in range (0, len(scan_num_array)):
#         scan_num_array[i] = scan_num_array[i][1:]
#         return scan_num_array

def check_scan_type(scan):
    temp_array = scan['command'][0].split( )
    scan_name = temp_array[0]
    return scan_name


class HDF5MultiCScan(object):

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

    # open and read multiple c scan from the data file
    def read_all_hdf5_xas(self, file_directory):
        energy_array = []
        scaler_array = []
        mca_array = []
        scan_number= []

        with h5py.File(file_directory,'r') as hf:
            # print('List of arrays in this file: \n', hf.keys())
            total_num = len(hf.keys())
            #scaler_array = [[[],[],[]] for i in range(total_num)]
            #mca_array = [[[], [], [], []] for i in range(total_num)]
            for i in range (0, total_num):
                scaler_data = [[], [], []]
                mca_data = [[], [], [], []]
                # print hf.keys()[i]
                scan = hf.get(hf.keys()[i])
                scan_name = check_scan_type(scan)
                # print "scan ", hf.keys()[i], "is:", scan_name
                # exclude empty scan
                if scan_name == "cscan" and len(scan['data']) > 2:
                    scan_number.append(hf.keys()[i])
                    energy_array.append(scan['data']['Energy'][0:])
                    scaler_data[0] = scan['data']['TEY'][0:]
                    scaler_data[1] = scan['data']['I0'][0:]
                    scaler_data[2] = scan['data']['Diode'][0:]
                    scaler_array.append(scaler_data)
                    mca_data[0] = scan['data']['_mca1_'][0:]
                    mca_data[1] = scan['data']['_mca2_'][0:]
                    mca_data[2] = scan['data']['_mca3_'][0:]
                    mca_data[3] = scan['data']['_mca4_'][0:]
                    mca_array.append(mca_data)
        self.set_energy_array(energy_array)
        self.set_mca_array(mca_array)
        self.set_scaler_array(scaler_array)
        self.set_c_scan(scan_number)
        self.set_file_direct(file_directory)
        estimate_xas_process_para = self.estimate_roi(file_directory, scan_number)
        return estimate_xas_process_para

    def estimate_roi(self, file_directory, scan_number):
        with h5py.File(file_directory, 'r') as hf:
            scan = hf.get(scan_number[0])
            string =  scan['command'][0]
        split_str = string.split(" ")
        start_energy = int(split_str[2])
        end_energy = int(split_str[3])
        medium_energy = (start_energy + end_energy) / 2
        medium_roi = medium_energy / 10
        roi_start = medium_roi - 8
        roi_end = medium_roi + 8

        print "estimate energy range: ", start_energy, "-", end_energy
        print "estimate roi: ", roi_start, "-", roi_end
        print "default bin interval: 0.1\n"

        estimate_xas_process_para = XASProcessPara(start_energy, end_energy, roi_start, roi_end, 0.1)
        return estimate_xas_process_para

class HDF5SingleCScan(object):

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

    def read_hdf5_xas(self, file_directory, scan_number):
        energy_array = []
        scaler_array = []
        mca_array = []
        with h5py.File(file_directory,'r') as hf:
            scaler_data = [[], [], []]
            mca_data = [[], [], [], []]
            # print hf.keys()[i]
            scan = hf.get(scan_number)
            scan_name = check_scan_type(scan)
            print "scan ", scan_number, "is:", scan_name
            # exclude empty scan
            print len(scan['data'])
            if scan_name == "cscan" and len(scan['data']) > 2:
                #scan_number.append(hf.keys()[i])
                energy_array = scan['data']['Energy'][0:]
                scaler_data[0] = scan['data']['TEY'][0:]
                scaler_data[1] = scan['data']['I0'][0:]
                scaler_data[2] = scan['data']['Diode'][0:]
                scaler_array = scaler_data
                mca_data[0] = scan['data']['_mca1_'][0:]
                mca_data[1] = scan['data']['_mca2_'][0:]
                mca_data[2] = scan['data']['_mca3_'][0:]
                mca_data[3] = scan['data']['_mca4_'][0:]
                mca_array = mca_data

                self.energy_array = energy_array
                self.mca_array = mca_array
                self.scaler_array = scaler_array
                self.scan_num = scan_number
                self.file_direct = file_directory
            elif scan_name == "cscan" and len(scan['data']) == 2:
                return "It is an empty c scan"
            else:
                return "It is not a c scan."

class HDF5SingleCmesh(object):

    def __init__(self):
        self.hex_x = None
        self.hex_y = None
        self.mca_array = None
        self.scaler_array = None
        self.scan_num = None

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

    def read_hdf5_map(self, file_directory, scan_num):
        hex_x_array = []
        hex_y_array = []
        scaler_array = []
        mca_array = []
        with h5py.File(file_directory,'r') as hf:
            print hf.keys()
            scaler_data = [[], [], []]
            mca_data = [[], [], [], []]
            scan = hf.get(scan_num)
            scan_name = check_scan_type(scan)
            if scan_name == "cmesh" and len(scan['data']) > 2:
                hex_x_array = scan['data']['Hex_XP'][0:]
                hex_y_array = scan['data']['Hex_YP'][0:]
                scaler_data[0] = scan['data']['TEY'][0:]
                scaler_data[1] = scan['data']['I0'][0:]
                scaler_data[2] = scan['data']['Diode'][0:]
                scaler_array = scaler_data
                mca_data[0] = scan['data']['_mca1_'][0:]
                mca_data[1] = scan['data']['_mca2_'][0:]
                mca_data[2] = scan['data']['_mca3_'][0:]
                mca_data[3] = scan['data']['_mca4_'][0:]
                mca_array = mca_data
        self.hex_x = hex_x_array
        self.hex_y = hex_y_array
        self.mca_array = mca_array
        self.scaler_array = scaler_array
        self.scan_num = scan_num