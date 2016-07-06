# SGM Data view module

import matplotlib.pyplot as plt
import numpy as np


def get_pfy(mca_array, enStart, enStop):

	print "Getting PFY ROIs"

	pfy1=[]
	pfy2=[]
	pfy3=[]
	pfy4=[]

	for i in range(0, len(mca_array[0])):
		pfy1.append(np.sum(mca_array[0][i][enStart:enStop]))
		pfy2.append(np.sum(mca_array[1][i][enStart:enStop]))
		pfy3.append(np.sum(mca_array[2][i][enStart:enStop]))
		pfy4.append(np.sum(mca_array[3][i][enStart:enStop]))
	
	return pfy1, pfy2, pfy3, pfy4
	print "Done!"


def plot_xas(energy_data, name, scaler_data=None, pfy_data=None):
	plt.close('all')
	if name == "TEY" or name == "I0" or name == "Diode" or name == "SDD1_OCR" or name == "SDD1_ICR" or name == "SDD2_OCR" or name == "SDD2_ICR" or name == "SDD3_OCR" or name == "SDD3_ICR" or name == "SDD4_OCR" or name == "SDD4_ICR":
		plot_xas_scaler(energy_data, scaler_data, name)
	elif name == "PFY_SDD1" or name == "PFY_SDD2" or name == "PFY_SDD3" or name == "PFY_SDD4":
		plot_xas_pfy(energy_data, pfy_data, name)
	else:
		print "Errors with the name input"


def plot_xas_pfy(energy_data, pfy_data, name):
	plt.close('all')
	print "Plotting", name, "Spectra"
	pfy_dict = {'PFY_SDD1': 0, 'PFY_SDD2': 1, 'PFY_SDD3': 2, 'PFY_SDD4': 3}
	pfy_index = pfy_dict[name]
	sub_pfy_data = pfy_data[pfy_index]

	plt.plot(energy_data, sub_pfy_data)
	plt.xlabel("Energy (eV)")
	plt.ylabel(name)
	plt.show()


def plot_xas_scaler(energy_data, scaler_data, name):
	plt.close('all')
	print "Plotting", name, "Spectra"
	scaler_dict = {'TEY': 0, 'I0': 1, 'Diode':2}
	scaler_index = scaler_dict[name]
	data = scaler_data[scaler_index]
	plt.plot(energy_data, data)
	plt.xlabel("Energy (eV)")
	plt.ylabel(name)
	plt.show()


def plot_xas_all(energy_data, scaler_data, pfy_data):
	plt.close('all')
	print "Plotting XAS."

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

