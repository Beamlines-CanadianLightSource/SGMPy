# Present summary for multiple c scans

import matplotlib.pyplot as plt
import numpy as np
import time

def summary_plot(xas_data, name, xas_process_para = None):
    """
    The functions is to plot a summary plot py invoking either generate_summary_plot_with_pfy or generate_summary_plot_with_scaler
    :param xas_data: the original data set consists of energy, sdd and the other scalers
    :param name: a string of sdd (mca) name
    :param xas_process_para: a XASProcessPara type object has parameters including roi and energy range
    :return: None
    """
    # start_time = time.time()
    plt.close('all')
    if name == "TEY" or name == "I0" or name == "Diode":
        energy_data = xas_data.get_energy_array()
        scaler_data = xas_data.get_scaler_array()
        scan_num = xas_data.get_c_scan()
        if scan_num is None:
            print ("Cannot process xas data without a qualified cscan")
        else:
            generate_summary_plot_with_scaler(energy_data, scaler_data, scan_num, name)
    elif name == "PFY_SDD1" or "PFY_SDD2" or "PFY_SDD3" or "PFY_SDD4" or "SDD1" or "SDD2" or "SDD3" or "SDD4":
        if name == "PFY_SDD1":
            name = "SDD1"
        elif name == "PFY_SDD2":
            name = "SDD2"
        elif name == "PFY_SDD3":
            name = "SDD3"
        elif name == "PFY_SDD4":
            name = "SDD4"
        energy_data = xas_data.get_energy_array()
        mca_data = xas_data.get_mca_array()
        scan_num = xas_data.get_c_scan()
        if (xas_process_para == None):
            print ("Cannot process xas data without a valid ROI range")
            return None
        else:
            start_roi = xas_process_para.get_roi_start()
            stop_roi = xas_process_para.get_roi_end()
        if scan_num is None:
            print ("Cannot process xas data without a qualified cscan")
            return None
        else:
            generate_summary_plot_with_pfy(energy_data, mca_data, scan_num, name, start_roi, stop_roi)
    else:
        print ("Errors with the name input")
    # print("--- %s seconds ---" % (time.time() - start_time))


def generate_summary_plot_with_pfy(energy_data, mca_data, scan_nums, pfy_name, start_roi, stop_roi):
    """
    Generate a specific summary plot with pfy_sdd with original data
    :param energy_data: the energy data from original data file
    :param mca_data: the mca data from original data file
    :param scan_nums: a list of index for c-scans
    :param pfy_name: a string of pfy_sdd name
    :param start_roi: the start range for region of interest
    :param stop_roi: the stop range for region of interest
    :return: None
    """

    print ("Start plotting summary plot of", pfy_name, "...")

    # MCA is SDD; after getting PFY of ROI then it becomes PFY_SDD
    pfy_dict = {'SDD1': 'MCA1', 'SDD2': 'MCA2', 'SDD3': 'MCA3', 'SDD4': 'MCA4'}
    # mca_dict = {'MCA1': 0, 'MCA2': 1, 'MCA3': 2, 'MCA4': 3}
    mca_name = pfy_dict[pfy_name]

    total_cscan_num = len(scan_nums)
    y_tick = []
    total_pfy = get_one_pfy_from_all_scan(mca_data, mca_name, start_roi, stop_roi)

    for index in range (0, total_cscan_num):

        scan_num_list = np.empty(len(energy_data[index]))
        scan_num_list.fill(index+1)

        # real scan number from the data file
        cscan_number = scan_nums[index]
        
        # print len(energy_data[index])
        # print len(scan_num_list)
        # print len(total_pfy[index])
        
        # print "Generating plot for scan No.", cscan_number, "real scan number:", real_cscan_number
        plt.scatter(energy_data[index], scan_num_list, c=total_pfy[index],  s=140, linewidths=0, marker='s')
        y_tick.append( str(index+1) + "(" + str(cscan_number) + ")" )
        # print "Generated plot for No.", index+1, "in c scan array.  Real scan number is:", cscan_number

    # setup the y-axis ticks
    plt.yticks(np.arange(0+1, total_cscan_num+1, 1.0), y_tick)
    # add lable for x and y axis
    plt.xlabel('Incident Energy (eV)')
    plt.ylabel('Scan Index (Scan Number)')
    plt.colorbar()
    plt.title("Summary Plot (Intensity: %s)" %(pfy_name))
    y_axis_height = total_cscan_num * 0.25
    # change the figure configuration
    fig = plt.gcf()
    fig.set_size_inches(16, y_axis_height)
    plt.grid()
    # show the plot
    print ("Plot generating complete")
    plt.show()


def generate_summary_plot_with_scaler(energy_data, scaler_data, scan_nums, scaler_name):
    """
    Generate a specific summary plot with scalers with original data
    :param energy_data: the energy data from original data file
    :param scaler_data: the scaler data from original data file
    :param scan_nums: a list of index for c-scans
    :param scaler_name: a string of scaler name
    :return: None
    """
    print ("Start plotting summary plot of", scaler_name, "...")

    scaler_dict = {'TEY': 0, 'I0': 1, 'Diode':2}
    scaler_index = scaler_dict[scaler_name]

    str_scaler_name = scaler_name
    total_cscan_num = len(scan_nums)
    y_tick = []

    for index in range (0, total_cscan_num):

        scan_num_list=np.empty(len(energy_data[index]))
        # create a list including all the scan number
        scan_num_list.fill(index+1)
        
        # real scan number from the data file
        cscan_number = scan_nums[index]
        
        # print len(energy_data[index])
        # print len(scan_num_list)
        # print len(scaler_data[index][scaler_index])
        
        # print "Generating plot for scan No.", cscan_number
        plt.scatter(energy_data[index], scan_num_list, c=scaler_data[index][scaler_index],  s=140, linewidths=0, marker='s')
        y_tick.append( str(index+1) + "(" + str(cscan_number) + ")" )
        # print "Generated plot for No.", index+1, "in c scan array.  Real scan number is:", cscan_number
        
    # setup the y-axis ticks
    plt.yticks(np.arange(0+1, total_cscan_num+1, 1.0), y_tick)
    # add lable for x and y axis
    plt.xlabel('Incident Energy (eV)')
    plt.ylabel('Scan Index (Scan Number)')
    plt.colorbar()
    plt.title("Summary Plot (Intensity: %s)"%(str_scaler_name))
    y_axis_height = total_cscan_num * 0.25
    # change the figure configuration
    fig = plt.gcf()
    fig.set_size_inches(16, y_axis_height)
    plt.grid()
    # show the plot
    print ("Plot generating complete")
    plt.show()


def get_one_pfy_from_all_scan(mca_data, mca_name, enStart, enStop):

    """
    Get one of 4 pfy_sdd from all c-scans opened
    :param mca_data:
    :param mca_name:
    :param enStart: the start range for region of interest
    :param enStop: the end range for region of interest
    :return: a 2D list consists 4 pfy_sdd sub-list
    """

    if mca_name == "MCA1":
        mca = 0
    elif mca_name == "MCA2":
        mca = 1
    elif mca_name == "MCA3":
        mca = 2
    elif mca_name == "MCA4":
        mca = 3
    else:
        print "Error!!!"

    # print "Getting PFY ROIs for", mca_name

    pfy=[[] for i in range(len(mca_data) )]
    # print "length of mca_data", len(mca_data)
    for i in range(0, len(mca_data)):
        for j in range(0, len(mca_data[i][mca])):
            pfy[i].append(np.sum(mca_data[i][mca][j][enStart:enStop]))
        # print "Length of PFY:", len(pfy[i])
    # print "Done!"
    # print "pfy length: ", len(pfy)
    return pfy