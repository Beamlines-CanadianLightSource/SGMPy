import os
from xas_process_para import XASProcessPara
from praxes.io import spec


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

    # open all scans of spectra
    def open_all_xas(self, file_directory):
        sgm_file = open_spec_data_file(file_directory)
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
            scaler_array[j][0] = scan[j]['TEY']
            scaler_array[j][1] = scan[j]['I0']
            scaler_array[j][2] = scan[j]['Diode']
            mcadata = scan[j]['@A1']

            counter += 1

            # print "Parsing MCAs"

            for i in range(0,len(scan[j]['Energy'])):
                mca_array[j][0].append(mcadata[i*4])
                mca_array[j][1].append(mcadata[i*4 + 1])
                mca_array[j][2].append(mcadata[i*4 + 2])
                mca_array[j][3].append(mcadata[i*4 + 3])

        print "Opened ", counter, " c-scans.\n"
        self.set_energy_array(energy_array)
        self.set_mca_array(mca_array)
        self.set_scaler_array(scaler_array)
        self.set_c_scan(c_scan_num)
        estimate_xas_process_para = self.estimate_roi(file_directory, c_scan_num)
        return estimate_xas_process_para

    def estimate_roi(self, file_directory, scan_num):
        opened_file = open_spec_data_file(file_directory)
        string = opened_file[scan_num[0]].attrs['command']
        split_str = string.split(" ")
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

    def get_energy_array(self):
        return self.energy_array

    def get_mca_array(self):
        return self.mca_array

    def get_scaler_array(self):
        return self.scaler_array

    def get_scan_num(self):
        return self.scan_num

    # open a single scan of spectrum
    def open_single_xas(self, sgm_file, scan_num):

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
        self.energy_array = energy_array
        self.mca_array = mca_array
        self.scaler_array = scaler_array
        self.scan_num = scan_num


class OpenSingleCMesh(object):

    def __init__(self):
        self.hex_x = None
        self.hex_y = None
        self.mca_array = None
        self.scaler_array = None
        self.scan_num = None
        self.scan_header = [None] * 10
        self.file_header = [None] * 5

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

    def get_scan_header(self):
        return self.scan_header

    def get_file_header(self):
        return self.file_header

    # open one scan of map
    def open_sgm_map(self, sgm_file, scan_num):

        print "Opening scan", str(scan_num)
        print "in", sgm_file

        f = spec.open(sgm_file)
        scan=f[str(scan_num)]

        self.scan_header[0] = scan.attrs["command"]
        self.scan_header[1] = scan.attrs["date"]
        duration = scan.attrs["duration"]
        self.scan_header[2] = str(duration[1]) + "  (" + str(duration[0]) + ")"
        orientations = scan.attrs["orientations"]
        self.scan_header[3] = str(orientations[0][0])
        self.scan_header[4] = str(orientations[1][0])
        self.scan_header[5] = str(orientations[2][0])
        self.scan_header[6] = str(orientations[3][0])
        hkl = scan.attrs["hkl"]
        self.scan_header[7] = str(hkl[0]) + " " + str(hkl[1]) + " " + str(hkl[2])
        positions = scan.attrs["positions"]
        print positions

        self.file_header[0] = scan.attrs["file_origin"]
        self.file_header[1] = str(scan.attrs["epoch_offset"])
        self.file_header[2] = scan.attrs["file_date"]
        self.file_header[3] = scan.attrs["program"]
        self.file_header[4] = scan.attrs["user"]

        self.scan_header[8] = str(positions['Hex_X']) + " " + str(positions['Hex_Y']) + " " + str(positions['Hex_Z']) + " " + str(positions['Hex_XP']) + " " + str(positions['Hex_YP']) + " " + str(positions['Hex_ZP']) + " " + str(positions['Energy']) + " " + " " + str(positions['XPS_Y'])

        self.scan_header[9] = str(positions['XPS_X']) + " " + str(positions['XPS_Z']) + " " + str(positions['XPS_R'])


        print scan.attrs["command"]
        print scan.attrs["date"]
        print scan.attrs["duration"]
        print scan.attrs["user"]
        print scan.attrs["hkl"]
        print scan.attrs["orientations"]

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
        self.hex_x = hex_x
        self.hex_y = hex_y
        self.mca_array = mca_array
        self.scaler_array = scaler_array
        self.scan_num = scan_num


# # open all c mesh scan in a data file
# def open_all_sgm_map(opened_file):
#
#     cmesh_scan = get_cmesh_scan(opened_file)
#     total_scan_num = len(cmesh_scan)
#
#     scan=[]
#     mca1=[[] for a in range(total_scan_num)]
#     mca2=[[] for a in range(total_scan_num)]
#     mca3=[[] for a in range(total_scan_num)]
#     mca4=[[] for a in range(total_scan_num)]
#
#     for j in range (0, total_scan_num):
#         scan.append(opened_file[ cmesh_scan[j] ])
#
#         hex_x = scan[j]['Hex_XP']
#         mcadata = scan[j]['@A1']
#
#         for i in range(0,len(hex_x)):
#             mca1[j].append(mcadata[i*4])
#             mca2[j].append(mcadata[i*4 + 1])
#             mca3[j].append(mcadata[i*4 + 2])
#             mca4[j].append(mcadata[i*4 + 3])
#
#     print "Done!"
#     return scan, mca1, mca2, mca3, mca4
