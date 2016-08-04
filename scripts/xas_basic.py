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

