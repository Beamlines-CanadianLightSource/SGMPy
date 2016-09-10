# SGM Data view module

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class SingleXAS(object):

    def __init__(self, opened_one_cscan, data_type):
        self.energy_array = opened_one_cscan.get_energy_array()
        self.mca_array = opened_one_cscan.get_mca_array()
        self.scaler_array = opened_one_cscan.get_scaler_array()
        self.scan_num = opened_one_cscan.get_scan_num()
        self.file_direct = opened_one_cscan.get_file_direct()
        self.pfy_sdd_array = None
        self.data_type = data_type

    def get_energy_array(self):
        return self.energy_array

    def get_mca_array(self):
        return self.mca_array

    def get_scaler_array(self):
        return self.scaler_array

    def get_scan_num(self):
        return self.scan_num

    def get_pfy_sdd_array(self):
        return self.pfy_sdd_array

    def set_pfy_sdd_array(self, pfy_sdd_array):
        self.pfy_sdd_array = pfy_sdd_array

    def get_data_type(self):
        return self.data_type

    def get_file_direct(self):
        return self.file_direct

    def calculate_pfy(self, enStart, enStop):
        #print "Getting PFY ROIs"
        mca_array = self.get_mca_array()

        pfy1=[]
        pfy2=[]
        pfy3=[]
        pfy4=[]
        pfy=[[],[],[],[]]

        for i in range(0, len(mca_array[0])):
            pfy1.append(np.sum(mca_array[0][i][enStart:enStop]))
            pfy2.append(np.sum(mca_array[1][i][enStart:enStop]))
            pfy3.append(np.sum(mca_array[2][i][enStart:enStop]))
            pfy4.append(np.sum(mca_array[3][i][enStart:enStop]))

        pfy[0] = pfy1
        pfy[1] = pfy2
        pfy[2] = pfy3
        pfy[3] = pfy4
        self.set_pfy_sdd_array(pfy)


    def plot_xas(self, name):
        plt.close('all')
        if name == "TEY" or name == "I0" or name == "Diode":
            energy_data = self.get_energy_array()
            scaler_data = self.get_scaler_array()
            self.plot_xas_scaler(energy_data, scaler_data, name)
        elif name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
            energy_data = self.get_energy_array()
            pfy_data = self.get_pfy_sdd_array()
            self.plot_xas_pfy(energy_data, pfy_data, name)
        else:
            print "Errors with the name input"


    def plot_xas_pfy(self, energy_data, pfy_data, name):
        plt.close('all')
        print "Plotting", name, "Spectra"
        pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
        pfy_index = pfy_dict[name]
        sub_pfy_data = pfy_data[pfy_index]

        plt.plot(energy_data, sub_pfy_data)
        plt.xlabel("Energy (eV)")
        plt.ylabel(name)
        plt.show()


    def plot_xas_scaler(self, energy_data, scaler_data, name):
        plt.close('all')
        print "Plotting", name, "Spectra"
        scaler_dict = {'TEY': 0, 'I0': 1, 'Diode':2}
        scaler_index = scaler_dict[name]
        data = scaler_data[scaler_index]
        plt.plot(energy_data, data)
        plt.xlabel("Energy (eV)")
        plt.ylabel(name)
        plt.show()


    def plot_xas_all(self):
        plt.close('all')
        print "Plotting XAS."

        matplotlib.rcParams['figure.figsize'] = (12, 16)

        energy_data = self.get_energy_array()
        scaler_data = self.get_scaler_array()
        pfy_data = self.get_pfy_sdd_array()

        en = energy_data
        tey = scaler_data[0]
        i0 = scaler_data[1]
        diode = scaler_data[2]

        plt.figure(1)
        plt.subplot(4, 2, 1)
        plt.plot(en, tey)
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

    def plot_excitation_emission_matrix(self, name):

        matplotlib.rcParams['figure.figsize'] = (12, 10)
        plt.close('all')

        energy_array = self.get_energy_array()[0:]
        num_of_points = len(self.get_energy_array())
        num_of_emission_bins = len(self.get_mca_array()[0][0])

        bin_num_for_x = np.zeros(shape=(num_of_points, num_of_emission_bins))
        for i in range(num_of_points):
            bin_num_for_x[i].fill(energy_array[i])

        bin_num_for_y = np.zeros(shape=(num_of_points, num_of_emission_bins))
        bin_num_for_y[0:] = np.arange(10, (num_of_emission_bins + 1) * 10, 10)

        mca_dict = {'SDD1': 0, 'SDD2': 1, 'SDD3': 2, 'SDD4': 3}
        sub_mca_array_index = mca_dict[name]
        sub_mca_array = self.get_mca_array()[sub_mca_array_index]
        sub_mca_array = np.array(sub_mca_array)

        v_max = max(sub_mca_array[0])
        for i in range(1, num_of_points):
            temp_max = max(sub_mca_array[i])
            if temp_max > v_max:
                v_max = temp_max
        # print "v_max: ", v_max

        plt.scatter(bin_num_for_x, bin_num_for_y, c=sub_mca_array, s=7, linewidths=0, vmax=v_max, vmin=0)
        plt.yticks(np.arange(100, 2560, 100.0))
        plt.xlabel('Incident Energy (eV)')
        plt.ylabel('Emission Energy (eV)')
        plt.grid()
        plt.show()