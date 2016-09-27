# binning, averaging and plotting

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from cStringIO import StringIO
from open_hdf5 import *
import time


class XASProcess(object):

    def __init__(self, data_type):
        self.mean_energy_array = None
        self.sdd_binned_array = None
        self.scaler_averaged_array = None
        self.pfy_sdd_averaged_array = None
        self.normalized_array = None
        self.file_direct = None
        self.data_type = data_type

    def set_mean_energy_array(self, mean_energy_array):
        self.mean_energy_array = mean_energy_array

    def get_mean_energy_array(self):
        """Return the energy array which is the mid-point of bins"""
        return self.mean_energy_array

    def set_sdd_binned_array(self, sdd_binned_array):
        self.sdd_binned_array = sdd_binned_array

    def get_sdd_binned_array(self):
        """Return binned sdd array"""
        return self.sdd_binned_array

    def set_scaler_averaged_array(self, scaler_averaged_array):
        self.scaler_averaged_array = scaler_averaged_array

    def get_scaler_averaged_array(self):
        """Return averaged scaler array"""
        return self.scaler_averaged_array

    def set_pfy_sdd_averaged_array(self, pfy_sdd_averaged_array):
        self.pfy_sdd_averaged_array = pfy_sdd_averaged_array

    def get_pfy_sdd_averaged_array(self):
        """Return averaged pfy_sdd array"""
        return self.pfy_sdd_averaged_array

    def set_normalized_array(self, normalized_array):
        self.normalized_array = normalized_array

    def get_file_direct(self):
        """Return the original data file directory."""
        return self.file_direct

    def set_file_direct(self, file_direct):
        self.file_direct = file_direct

    def get_normalized_array(self):
        """Return a specific normalized data array."""
        return self.normalized_array

    def get_data_type(self):
        """Returns single scan or multiple scans."""
        return self.data_type

    def generate_good_scan_index(self, opened_xas_data, bad_scan_index_str):
        """
        This method to generate good scan index and eliminate bad scans by passing in bad scan index
        :param opened_xas_data: a OpenMultiCScan type object contains all original info of multiple c-scans
        :param bad_scan_index_str: str conatains index of bad scans that need to be eliminate
        :return: a list of good scan index (index may not as sams as the original scan numbers)

        """

        scan_num_index = opened_xas_data.get_c_scan()
        length = len(scan_num_index)
        # if badScanStr is null, then return original arrays
        if bad_scan_index_str == '':
            # print "In if"
            good_scan_index = range(1, length+1, 1)
        # to get good scan numbers
        else:
            # print "In else"
            # split the array based on comma symbol
            bad_scan_index = [x.strip() for x in bad_scan_index_str.split(',')]
            good_scan_index = range(1, length+1, 1)
            # print "Original scan", scan_num_index
            for i in range(0, length):
                for j in range (0, len(bad_scan_index)):
                    # print "i=", i
                    # print "j=", j
                    # print scan_num_index[i]
                    # print bad_scan_index[j]
                    if scan_num_index[i] == bad_scan_index[j]:
                        print "removed", bad_scan_index[j], ", real scan number is",  scan_num_index[int(bad_scan_index[j])-1]
                        good_scan_index.remove(int(bad_scan_index[j]))
        print ""
        return good_scan_index

    def process_xas(self, good_scan_index, opened_xas_data, xas_process_para):
        """
        The method is to execute all the related binning and averaging calculation and get binned and averaged data
        :param good_scan_index: a list contains all the good scan index
        :param opened_xas_data: a OpenMultiCScan type object contains all original info of multiple c-scans
        :param xas_process_para:  a XASProcessPara type object has parameters including roi and energy range
        :return: None
        """
        
        energy_data = opened_xas_data.get_energy_array()
        mca_data = opened_xas_data.get_mca_array()
        scaler_data = opened_xas_data.get_scaler_array()
        file_direct = opened_xas_data.get_file_direct()

        start_energy = xas_process_para.get_energy_start()
        end_energy = xas_process_para.get_energy_end()
        roi_start = xas_process_para.get_roi_start()
        roi_end = xas_process_para.get_roi_end()
        bin_interval = xas_process_para.get_bin_interval()

        num_of_bins = int((end_energy - start_energy) / bin_interval)
        print "numb_of_bins after calculation", num_of_bins

        # get all data of good scans
        energy_array, mca_array, scaler_array = self.get_good_datapoint(good_scan_index, energy_data, mca_data, scaler_data)

        # create bins and assign bins
        edges_array, bins_mean_array = self.create_bins(start_energy, end_energy, num_of_bins)
        assigned_data_array = self.assign_data(energy_array , edges_array, num_of_bins)
        
        # calculate mca
        calculate_bin_mca_result = self.calculate_bin_mca(assigned_data_array, mca_array)
        bin_mca = calculate_bin_mca_result[:-2]
        empty_bin_front = calculate_bin_mca_result[-2]
        empty_bin_back = calculate_bin_mca_result[-1]

        # calculate scalers (I0, TEY, Diode)
        averaged_scaler = self.calculate_bin_scalers(assigned_data_array, scaler_array, empty_bin_front, empty_bin_back)
        # calculate pfy of mca
        averaged_pfy_sdd = self.get_pfy_bin(bin_mca, roi_start, roi_end)

        #remove empty bins in mean_energy_array
        if empty_bin_front == 0 and empty_bin_back == 0:
            self.set_mean_energy_array(bins_mean_array)
        elif empty_bin_front != 0 and empty_bin_back == 0:
            self.set_mean_energy_array(bins_mean_array[empty_bin_front:])
        elif empty_bin_front == 0 and empty_bin_back != 0:
            self.set_mean_energy_array(bins_mean_array[:-empty_bin_back])
        else:
            self.set_mean_energy_array(bins_mean_array[empty_bin_front:num_of_bins-empty_bin_back])

        self.set_sdd_binned_array(bin_mca)
        self.set_scaler_averaged_array(averaged_scaler)
        self.set_pfy_sdd_averaged_array(averaged_pfy_sdd)
        self.set_file_direct(file_direct)

    def get_good_datapoint(self, good_scan_index, energy_data, mca_data, scaler_data):
        """
        Removed all the bad scans from the originla data set
        :param good_scan_index: a list contains all good scan index
        :param energy_data: original energy data
        :param mca_data: original mca (sdd) data
        :param scaler_data: originla scalers data (TEY, I0, Diode)
        :return: energy_array, mca_array and scaler_array with no data pointsre
        """
        good_scan_index_length = len(good_scan_index)
        print "Total good scan numbers:", good_scan_index_length

        energy_array = []
        scaler_array = [[[],[],[]] for i in range(good_scan_index_length)]
        mca_array=[[[],[],[],[]] for i in range(good_scan_index_length)]
        for i in range (0, len(good_scan_index)):
            # scan number is start from 1
            # print "This is the scan number: ", goodScanArray[i]
            # array index is start from 0
            # get all MCAs of good scans from original scans' array
            energy_array.append(energy_data[good_scan_index[i]-1])
            scaler_array[i][0] = scaler_data[good_scan_index[i]-1][0]
            scaler_array[i][1] = scaler_data[good_scan_index[i]-1][1]
            scaler_array[i][2] = scaler_data[good_scan_index[i]-1][2]
            # get all MCA1 of good scans from original scans
            mca_array[i][0] = mca_data[good_scan_index[i]-1][0]
            # get all MCA2 of good scans from original scans
            mca_array[i][1] = mca_data[good_scan_index[i]-1][1]
            # get all MCA3 of good scans from original scans
            mca_array[i][2] = mca_data[good_scan_index[i]-1][2]
            # get all MCA4 of good scans from original scans
            mca_array[i][3] = mca_data[good_scan_index[i]-1][3]
        return energy_array, mca_array, scaler_array


    def create_bins(self, start_energy, end_energy, num_of_bins):
        """
        Generate bins and get boundary of bins and mean energy of bins
        :param start_energy: this is an int number of beginning energy for c-scans
        :param end_energy: this is an int number of stopping energy for c-scans
        :param num_of_bins: total number of bins that the mehod will crate
        :return:
                edges of bins as an list
                and return mid-point of bins in a list"
        :examples: create_bins (startEnergy = 690, endEnergy = 750, numberOfBins = 600)
        """
        print "Start creating bins" 
        num_of_edges = num_of_bins + 1
        # print "Number of Bins:", num_of_bins
        # print "Number of Edges:", num_of_edges
        print "Energy range is: ", start_energy,"-", end_energy
        edges_array = np.linspace(start_energy, end_energy, num_of_edges)

        # generate mean of bins  
        mean_energy_array = []
        first_mean = (edges_array[1] + edges_array[0]) / 2
        bin_width = edges_array[1] - edges_array[0]
        for i in range (0, num_of_bins):
            mean_energy_array.append(first_mean + bin_width * i)
        # print "Mean of energy bins: ", mean_energy_array
        print "created bins completed.\n"
        # print ""
        return  edges_array, mean_energy_array

    def assign_data (self, energy_array, edges, bin_num):
        """
        Iteration and assign data points from different c-scans into desired bins
        :param energy_array: a list contains mean energy of bins
        :param edges: a list contains edges of bins
        :param bin_num: total number of bins were created in the previous steps
        :return: a 2D list contains distribution information of scan number and associate data points for each bin
        """
        bin_array = [[] for i in range(bin_num)]
        bin_width = (edges[-1] - edges[0]) / bin_num
        # print "The width of a bin is:", bin_width

        # interation to assign data into bins
        print "Start assigning data points into bins" 
        for scan_index in range (0, len(energy_array)):
            for datapoint_index in range (0, len(energy_array[scan_index]) ):
                if energy_array[scan_index][datapoint_index] <= edges[-1]:
                    x = energy_array[scan_index][datapoint_index] - edges[0]
                    # get integer part and plus 1
                    assign_bin_num = int(x / bin_width) + 1
                    # print assign_bin_num
                    bin_array[assign_bin_num-1].append([scan_index, datapoint_index])
        print "Assign data points completed\n"
        return bin_array

    def calculate_bin_mca(self, bin_array, mca_array):
        """
        Averaged the average mca(sdd)
        :param bin_array: a 2D list contains distribution information of scan number and associate data points for each bin
        :param mca_array: a array has 4 mca (sdd) without bad scan.
        :return: 4 binned and averaged pfy_mca
        """

        bin_num = len(bin_array)
        empty_bins = 0
        # Initial 4 arrays for 4 average of MCAs
        # Added 256 of zero into each sub array, so that it could calculate summary and then get the average
        mca1_bin_array = np.zeros(shape=(bin_num,256))
        mca2_bin_array = np.zeros(shape=(bin_num,256))
        mca3_bin_array = np.zeros(shape=(bin_num,256))
        mca4_bin_array = np.zeros(shape=(bin_num,256))

        print "Start calcualting average of SDD1(MCA1), SDD2(MCA2), SDD3(MCA3) & SDD4(MCA4)..."

        for index1 in range (0, bin_num):
            # get the total number of data points in a particular bin
            total_data_point = len(bin_array[index1])

            for index2 in range (0, total_data_point):
                # get index of scans
                index_of_scan = bin_array[index1][index2][0]
                # get index of data points
                index_of_data_point = bin_array[index1][index2][1]

                # print "index_of_scan: ", index_of_scan, "  ;  ", "index_of_data_point: ", index_of_data_point

                # calculate the sum of MCA1
                mca1_bin_array[index1] = mca1_bin_array[index1] + mca_array[index_of_scan][0][index_of_data_point]
                # calculate the sum of MCA2
                mca2_bin_array[index1] = mca2_bin_array[index1] + mca_array[index_of_scan][1][index_of_data_point]
                # calculate the sum of MCA3
                mca3_bin_array[index1] = mca3_bin_array[index1] + mca_array[index_of_scan][2][index_of_data_point]
                # calculate the sum of MCA4
                mca4_bin_array[index1] = mca4_bin_array[index1] + mca_array[index_of_scan][3][index_of_data_point]

            # print "Bin No.", index1+1, "; it contains ", total_data_point, "data points"

            if total_data_point == 0:
                empty_bins = empty_bins + 1
                print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
            else:
                # calculate the average of MCAs
                # print "Calculating Average of MCA1."
                mca1_bin_array[index1] = mca1_bin_array[index1] / total_data_point
                # print "Calculation Average of MCA1 is completed."
                # print "Calculating Average of MCA2."
                mca2_bin_array[index1] = mca2_bin_array[index1] / total_data_point
                # print "Calculation Average of MCA2 is completed."
                # print "Calculating Average of MCA3."
                mca3_bin_array[index1] = mca3_bin_array[index1] / total_data_point
                # print "Calculation Average of MCA3 is completed."
                # print "Calculating Average of MCA4."
                mca4_bin_array[index1] = mca4_bin_array[index1] / total_data_point
                # print "Calculation Average of MCA4 is completed."

        print "Calculation completed.\n"

        # remove empty bins in the front or at the end
        if empty_bins == 0:
            return mca1_bin_array, mca2_bin_array, mca3_bin_array, mca4_bin_array, 0, 0
        elif mca1_bin_array[0].any() == 0 :
            index = 1
            while mca1_bin_array[index].any() == 0:
                index = index+1
            # calculate how many bins are there in the front or at the end 
            empty_bin_front = index
            empty_bin_back = empty_bins - empty_bin_front
            last_bin = bin_num - empty_bin_back
            # print last_bin
            if empty_bin_back != 0:
                return mca1_bin_array[empty_bin_front:last_bin], mca2_bin_array[empty_bin_front:last_bin], mca3_bin_array[empty_bin_front:last_bin], mca4_bin_array[empty_bin_front:last_bin], empty_bin_front, empty_bin_back
            else:
                return mca1_bin_array[empty_bin_front:], mca2_bin_array[empty_bin_front:] , mca3_bin_array[empty_bin_front:] , mca4_bin_array[empty_bin_front:], empty_bin_front, 0
        else:
            return mca1_bin_array[:-empty_bins], mca2_bin_array[:-empty_bins], mca3_bin_array[:-empty_bins], mca4_bin_array[:-empty_bins], 0, empty_bins

    def calculate_bin_scalers(self, bin_array, scaler_array, empty_bin_front, empty_bin_back):
        """

        :param bin_array: a 2D array contains distribution information of scan number and associate data points for each bin
        :param scaler_array: a array has 3 different mca (sdd) without bad scan
        :param empty_bin_front: a integer show the number of empty bins in the front
        :param empty_bin_back:  a integer show the number of empty bins in the back
        :return:
        """

        # start_time = time.time()

        bin_num = len(bin_array)
        # empty_bins = 0
        tey_bin_array = np.zeros(bin_num)
        i0_bin_array = np.zeros(bin_num)
        diode_bin_array = np.zeros(bin_num)

        print "Start calcualting Average of I0, TEY & Diode..."

        for index1 in range (0, bin_num):
            # get the total number of data points in a particular bins
            total_data_point = len(bin_array[index1])

            for index2 in range (0, total_data_point):
                # get index of scans
                index_of_scan = bin_array[index1][index2][0]
                # print index_of_scan
                # get index of data points
                index_of_data_point = bin_array[index1][index2][1]
                # print index_of_data_point

                # calculate the sum of data (TEY, I0, Diode)
                tey_bin_array[index1] = tey_bin_array[index1] + scaler_array[index_of_scan][0][index_of_data_point]
                i0_bin_array[index1] = i0_bin_array[index1] + scaler_array[index_of_scan][1][index_of_data_point]
                diode_bin_array[index1] = diode_bin_array[index1] + scaler_array[index_of_scan][2][index_of_data_point]

                # print "Bin No.", index1+1, "; it contains ", total_data_point, "data point"

            if total_data_point == 0:
                # empty_bins = empty_bins + 1
                print "No data point is in Bin No.", index1+1, ". Average calculation is not necessary"
            else:
                # print total_data_point
                # calculate the average of data (TEY, I0, Diode)
                # print "Calculating Average of TEY."
                tey_bin_array[index1] = tey_bin_array[index1] / total_data_point
                # print "Calculation Average of TEY is completed."
                # print "Calculating Average of I0."
                i0_bin_array[index1] = i0_bin_array[index1] / total_data_point
                # print "Calculation Average of I0 is completed."
                # print "Calculating Average of Diode."
                diode_bin_array[index1] = diode_bin_array[index1] / total_data_point
                # print "Calculation Average of Diode is completed."
                # print "Index of bins:", index1, "   Average of TEY:", tey_bin_array[index1]
                # print "Index of bins:", index1, "   Average of I0:", i0_bin_array[index1]
                # print "Index of bins:", index1, "   Average of Diode:", diode_bin_array[index1]
                # print
        print "Calculation completed."
        # print("--- %s seconds ---" % (time.time() - start_time))
        print
        # remove empty bins in the front or at the end
        last_bin = bin_num - empty_bin_back
        # if there is no empty bins
        if empty_bin_front == 0 and empty_bin_back == 0:
            return tey_bin_array, i0_bin_array, diode_bin_array
        # if there are empty bins in the front
        elif empty_bin_front != 0 and empty_bin_back == 0:
            return tey_bin_array[empty_bin_front:], i0_bin_array[empty_bin_front:], diode_bin_array[empty_bin_front:]
        # if there are empty bins in the back
        elif empty_bin_front == 0 and empty_bin_back != 0:
            return tey_bin_array[:-empty_bin_back], i0_bin_array[:-empty_bin_back], diode_bin_array[:-empty_bin_back]
        # if there are empty bin in the front and bak
        else:
            return tey_bin_array[empty_bin_front:last_bin], i0_bin_array[empty_bin_front:last_bin], diode_bin_array[empty_bin_front:last_bin]

    def plot_excitation_emission_matrix(self, name):
        """
        Generate Excitation Emission Matrix for identify Region of Interest
        :param name: a string of mca (sdd) name
        :return: None
        """

        matplotlib.rcParams['figure.figsize'] = (12, 10)

        print "Plotting incident v emission energy coordinate based on average of SDD(MCA)"
        bins_mean_array = self.get_mean_energy_array()
        bin_mca = self.get_sdd_binned_array()
        plt.close('all')
        # MCA is SDD and SDD is MCA
        mca_dict = {'SDD1': 0, 'SDD2': 1, 'SDD3': 2, 'SDD4': 3}
        sub_mca_array_index = mca_dict[name]
        sub_mca_array = bin_mca[sub_mca_array_index]
        sub_mca_array = np.array(sub_mca_array)

        num_of_bin = len (bins_mean_array)
        num_of_emission_bins = len(sub_mca_array[0])

        bin_num_for_x = [[]for i in range(num_of_bin)]
        for bin in range (0, num_of_bin):
            bin_num_for_x[bin] = np.empty(num_of_emission_bins)
            # fill energy into the array
            bin_num_for_x[bin].fill(bins_mean_array[bin])

        # generate a list of number to present 1 - 256 bins for emission energy
        bin_num_for_y = np.zeros(shape=(num_of_bin, num_of_emission_bins))
        bin_num_for_y[0:] = np.arange(10, (num_of_emission_bins + 1) * 10, 10)
        
        v_max = max(sub_mca_array[0])
        for i in range(1, num_of_bin):
            temp_max = max(sub_mca_array[i])
            if temp_max > v_max:
                v_max = temp_max
        print "v_max: ", v_max

        plt.scatter(bin_num_for_x, bin_num_for_y, c= sub_mca_array, s=7, linewidths=0, vmax=v_max, vmin=0)

        plt.yticks(np.arange(100, 2560, 100.0))
        plt.xlabel('Incident Energy (eV)')
        plt.ylabel('Emission Energy (eV)')
        plt.title("Excitation Emission Matrix")
        plt.grid()
        plt.show()
        print "Incident Energy range:", bin_num_for_x[0][0], "-", bin_num_for_x[-1][0]
        print "Emission Energy range:", bin_num_for_y[0][0], "-", bin_num_for_y[0][-1]

    def get_pfy_bin(self, mca_bin_array, start_energy, stop_energy):
        """
        Use a specific Region of Interest to calculate pyf_sdd
        :param mca_bin_array: averaged and binned eneryg aray
        :param start_energy: this is an int number of beginning energy of scans
        :param stop_energy: this is an int number of stopping energy
        :return: 4 lists of pfy_sdd
        """

        # print "Getting PFY ROIs"

        pfy1=[]
        pfy2=[]
        pfy3=[]
        pfy4=[]

        for i in range(0, len(mca_bin_array[0])):
            pfy1.append(np.sum(mca_bin_array[0][i][start_energy:stop_energy]))
            pfy2.append(np.sum(mca_bin_array[1][i][start_energy:stop_energy]))
            pfy3.append(np.sum(mca_bin_array[2][i][start_energy:stop_energy]))
            pfy4.append(np.sum(mca_bin_array[3][i][start_energy:stop_energy]))

        return pfy1, pfy2, pfy3, pfy4

    # plot a specific one of the averaged scalers
    def plot_avg_xas(self, name):
        """
        Generate a single averaged plot, it can distinguish pfy_sdd and the other scalers
        :param name: a string of scaler's name (eg. SDD1, SDD2, TEY, IO)
        :return: None
        """
        plt.close('all')
        matplotlib.rcParams['figure.figsize'] = (12, 10)

        if name == "TEY" or name == "I0" or name == "Diode":
            mean_energy_array = self.get_mean_energy_array()
            scaler_data = self.get_scaler_averaged_array()
            self.plot_avg_xas_scaler(mean_energy_array, scaler_data, name)
        elif name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
            mean_energy_array = self.get_mean_energy_array()
            pfy_data = self.get_pfy_sdd_averaged_array()
            self.plot_avg_xas_pfy(mean_energy_array, pfy_data, name)
        else:
            print "Errors with the name input"

    def plot_avg_xas_scaler(self, mean_energy_array, scaler_data, name):
        """
        Generate TEY, I0 or Diode plot (matplotlib figure)
        :param mean_energy_array: mean energy of bins (x-axis)
        :param scaler_data: averaged scaler data (y-axis)
        :param name: the string of scaler name
        :return: None
        """

        scaler_dict = {'TEY': 0, 'I0': 1, 'Diode':2}
        scaler_index = scaler_dict[name]
        plt.plot(mean_energy_array, scaler_data[scaler_index])
        plt.xlabel('Energy (eV)')
        plt.ylabel(name)
        plt.show()
    
    def plot_avg_xas_pfy(self, mean_energy_array, pfy_data, name):
        """
        Generate a specific pfy_sdd plot (matplotlib figure)
        :param mean_energy_array: mean energy of bins (x-axis)
        :param pfy_data: averaged pfy_sdd data (y-axis)
        :param name: the string of pfy_sdd name
        :return: None
        """

        pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
        pfy_index = pfy_dict[name]
        plt.plot(mean_energy_array, pfy_data[pfy_index])
        plt.xlabel('Energy (eV)')
        plt.ylabel(name)
        plt.show()

    def plot_avg_xas_all(self):
        """
        Generate all plots (matplotlib figures) for averaged data at once
        :return: None
        """
        print "Plotting average XAS."    
        plt.close('all')

        matplotlib.rcParams['figure.figsize'] = (14, 20)

        en = self.get_mean_energy_array()
        scaler_array = self.get_scaler_averaged_array()
        pfy_data = self.get_pfy_sdd_averaged_array()

        tey = scaler_array[0]
        i0 = scaler_array[1]
        diode = scaler_array[2]

        plt.figure(1)
        plt.subplot(4, 2, 1)
        plt.plot(en, tey)
        # add lable for x and y axis
        plt.xlabel('Energy (eV)')
        plt.ylabel('TEY')

        plt.subplot(4, 2, 2)
        plt.plot(en, i0)
        plt.xlabel('Energy (eV)')
        plt.ylabel('I0')

        plt.subplot(4, 2, 3)
        plt.plot(en, diode)
        plt.xlabel('Energy (eV)')
        plt.ylabel('Diode')

        plt.subplot(4, 2, 5)
        plt.plot(en, pfy_data[0])
        plt.xlabel('Energy (eV)')
        plt.ylabel('PFY_SDD1')

        plt.subplot(4, 2, 6)
        plt.plot(en, pfy_data[1])
        plt.xlabel('Energy (eV)')
        plt.ylabel('PFY_SDD2')

        plt.subplot(4, 2, 7)
        plt.plot(en, pfy_data[2])
        plt.xlabel('Energy (eV)')
        plt.ylabel('PFY_SDD3')

        plt.subplot(4, 2, 8)
        plt.plot(en, pfy_data[3])
        plt.xlabel('Energy (eV)')
        plt.ylabel('PFY_SDD4')

        plt.show()

    def division(self, pfy_data, dividend, divisor, scaler_data = None):
        """
        Normalization process without carbon.
        :param pfy_data: averaged pfy data array
        :param dividend: dividend of the normalization cul
        :param divisor: divisor of the normalization cul
        :param scaler_data: averaged scaler data array
        :return: a normalized data array
        """
        # initial new_mca_array
        # division_pfy_array = np.empty(len(pfy_data[0]))
        # initial a dictionary for 4 SDD(MCA) name
        pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
        scaler_dict = {'TEY': 0, 'I0': 1, 'Diode': 2}
        if dividend == divisor:
            print "Cannot division same SDD(MCA)"
        # calculate division
        else:
            if divisor == "I0" or divisor == "TEY" or divisor =="Diode":
                dividend_index = pfy_dict[dividend]
                divisor_index = scaler_dict[divisor]
                division_array = np.array(pfy_data[dividend_index]) / np.array(scaler_data[divisor_index])
            else:
                dividend_index = pfy_dict[dividend]
                divisor_index = pfy_dict[divisor]
                division_array = np.array(pfy_data[dividend_index]) / np.array(pfy_data[divisor_index])
            return division_array

    def plot_division(self, dividend, divisor):
        """
        Plot the normalized data (not including carbon)
        :param dividend: string of dividend name
        :param divisor:  string of divisor name
        :return: None
        """

        print "Plotting disivion SDD."
        plt.close('all')
        matplotlib.rcParams['figure.figsize'] = (13, 10)

        bins_mean_array = self.get_mean_energy_array()
        pfy_data = self.get_pfy_sdd_averaged_array()
        scaler_data = self.get_scaler_averaged_array()

        division_array = self.division(pfy_data, dividend, divisor, scaler_data)
        plt.plot(bins_mean_array, division_array)
        plt.xlabel('Energy (eV)')
        str_y_axis = StringIO()
        str_y_axis.write(dividend + ' / ' + divisor)
        plt.ylabel(str_y_axis.getvalue())
        plt.title("averaged %s / average %s"%(dividend, divisor))
        plt.show()
        self.set_normalized_array(division_array)


class XASProcessCarbon(object):

    def __init__(self, xas_process_data, blank_xas_process_data):
        self.xas_process_data = xas_process_data
        self.blank_xas_process_data = blank_xas_process_data

    def get_xas_process_data(self):
        return self.xas_process_data

    def get_blank_xas_process_data(self):
        return self.blank_xas_process_data

    def carbon_normalize(self):
        plt.close("all")
        matplotlib.rcParams['figure.figsize'] = (12, 10)

        xas_process_data = self.get_xas_process_data()
        blank_xas_process_data = self.get_blank_xas_process_data()
        pfy_sdd_normalized = np.array(xas_process_data.get_pfy_sdd_averaged_array()[2]) / np.array(blank_xas_process_data.get_pfy_sdd_averaged_array()[0])
        plt.close('all')
        plt.plot(xas_process_data.get_mean_energy_array(), pfy_sdd_normalized)
        plt.show()
