import numpy as np

class MapProcess(object):

    def __init__(self, single_map, map_process_para):
        self.single_map = single_map
        self.map_process_para = map_process_para
        self.mean_energy_array = None
        self.averaged_tey = None
        self.averaged_i0 = None
        self.averaged_diode = None
        self.averaged_mca = None
        self.pfy_sdd = None

    def get_mean_energy_array(self):
        return self.mean_energy_array

    def get_averaged_tey(self):
        return self.averaged_tey

    def get_averaged_i0(self):
        return self.averaged_i0

    def get_averaged_diode(self):
        return self.averaged_diode

    def get_averaged_mca(self):
        return self.averaged_mca

    def get_pfy_sdd(self):
        return self.pfy_sdd

    def process_map(self):
        map_process_para = self.map_process_para
        single_map = self.single_map
        x_start_energy = map_process_para.get_x_start_energy()
        x_end_energy = map_process_para.get_x_end_energy()
        x_bin_num = map_process_para.get_x_bin_num()
        y_start_energy = map_process_para.get_y_start_energy()
        y_end_energy = map_process_para.get_y_end_energy()
        y_bin_num = map_process_para.get_y_bin_num()
        x_energy_array = single_map.get_hex_x()
        y_energy_array = single_map.get_hex_y()

        x_edges_array, y_edges_array, mean_energy_array = self.create_grid(x_start_energy, x_end_energy, x_bin_num, y_start_energy, y_end_energy, y_bin_num)
        grid_array = self.assign_data(x_edges_array, y_edges_array, x_energy_array, y_energy_array)
        averaged_tey, averaged_i0, averaged_diode, averaged_mca1, averaged_mca2, averaged_mca3, averaged_mca4 = self.calculation(single_map, x_bin_num, y_bin_num, grid_array)
        self.mean_energy_array = mean_energy_array
        self.averaged_tey = averaged_tey
        self.averaged_i0 = averaged_i0
        self.averaged_diode = averaged_diode
        self.averaged_mca = averaged_mca1, averaged_mca2, averaged_mca3, averaged_mca4

    def create_grid(self, x_start_energy, x_end_energy, x_num_of_bins, y_start_energy, y_end_energy, y_num_of_bins):
        print "Start creating grids"
        x_num_of_edges = x_num_of_bins + 1
        x_edges_array = np.linspace(x_start_energy, x_end_energy, x_num_of_edges)

        x_first_mean = (x_edges_array[1] + x_edges_array[0]) / 2
        x_bin_width = x_edges_array[1] - x_edges_array[0]

        y_num_of_edges = y_num_of_bins + 1
        y_edges_array = np.linspace(y_start_energy, y_end_energy, y_num_of_edges)

        y_first_mean = (y_edges_array[1] + y_edges_array[0]) / 2
        y_bin_width = y_edges_array[1] - y_edges_array[0]

        mean_energy_array = [[[] for j in range (y_num_of_bins)] for i in range(x_num_of_bins)]

        for i in range(0, x_num_of_bins):
            for j in range(0, y_num_of_bins):
                mean_energy_array[i][j].append([x_first_mean + x_bin_width * i, y_first_mean + y_bin_width * j])

        return x_edges_array, y_edges_array, mean_energy_array

    def assign_data(self, x_edges_array, y_edges_array, x_energy_array, y_energy_array):
        x_bin_num = 50
        y_bin_num = 50
        x_bin_width = x_edges_array[1] - x_edges_array[0]
        y_bin_width = y_edges_array[1] - y_edges_array[0]
        grid_array = [[[] for j in range(y_bin_num)] for i in range(x_bin_num)]

        for datapoint_index in range(0, len(x_energy_array)):
            # print "datapoint_index", datapoint_index
            if x_energy_array[datapoint_index] <= x_edges_array[-1] and y_energy_array[datapoint_index] <= y_edges_array[-1]:
                # print "in if branch"
                x = x_energy_array[datapoint_index] - x_edges_array[0]
                # print "x", x
                # print "bin_width", x_bin_width
                # print "x / bin_width", x / x_bin_width
                x_bin_assigned = int(x / x_bin_width) + 1
                # print x_bin_assigned

                y = y_energy_array[datapoint_index] - y_edges_array[0]
                # print "y", y
                # print "bin_width_y", y_bin_width
                # print "y / bin_width", y / y_bin_width
                y_bin_assigned = int(y / y_bin_width) + 1
                # print y_bin_assigned
                # print

                grid_array[x_bin_assigned - 1][y_bin_assigned - 1].append(datapoint_index)
        return grid_array

    def calculation(self, single_map, x_bin_num, y_bin_num, grid_array):

        mca_array = np.array(single_map.get_mca_array())
        scaler_array = np.array(single_map.get_scaler_array())
        averaged_mca1 = [[] for i in range(0, x_bin_num)]
        for i in range(0, x_bin_num):
            averaged_mca1[i] = np.zeros(shape=(y_bin_num, 256))

        averaged_mca2 = [[] for i in range(0, x_bin_num)]
        for i in range(0, x_bin_num):
            averaged_mca2[i] = np.zeros(shape=(y_bin_num, 256))

        averaged_mca3 = [[] for i in range(0, x_bin_num)]
        for i in range(0, x_bin_num):
            averaged_mca3[i] = np.zeros(shape=(y_bin_num, 256))

        averaged_mca4 = [[] for i in range(0, x_bin_num)]
        for i in range(0, x_bin_num):
            averaged_mca4[i] = np.zeros(shape=(y_bin_num, 256))

        averaged_tey = np.zeros((x_bin_num, y_bin_num))
        averaged_i0 = np.zeros((x_bin_num, y_bin_num))
        averaged_diode = np.zeros((x_bin_num, y_bin_num))

        for i in range(0, x_bin_num):
            for j in range(0, y_bin_num):
                if grid_array[i][j] != []:
                    print i, j, "is not empty"

                    counter = len(grid_array[i][j])
                    # print mca_array[0][grid_array[i][j][0:]]
                    for k in range(0, len(grid_array[i][j])):
                        # print "grid_array[i][j] ", grid_array[i][j]
                        # print averaged_mca1[i][j]

                        print averaged_tey[i][j]
                        averaged_tey[i][j] = averaged_tey[i][j] + scaler_array[0][grid_array[i][j][k]]
                        averaged_tey[i][j] = averaged_tey[i][j] / counter

                        averaged_i0[i][j] = averaged_i0[i][j] + scaler_array[1][grid_array[i][j][k]]
                        averaged_i0[i][j] = averaged_i0[i][j] / counter

                        averaged_diode[i][j] = averaged_diode[i][j] + scaler_array[2][grid_array[i][j][k]]
                        averaged_diode[i][j] = averaged_diode[i][j] / counter

                        averaged_mca1[i][j] = averaged_mca1[i][j] + mca_array[0][grid_array[i][j][k]]
                        averaged_mca1[i][j] = averaged_mca1[i][j] / counter

                        averaged_mca2[i][j] = averaged_mca2[i][j] + mca_array[1][grid_array[i][j][k]]
                        averaged_mca2[i][j] = averaged_mca2[i][j] / counter

                        averaged_mca3[i][j] = averaged_mca3[i][j] + mca_array[2][grid_array[i][j][k]]
                        averaged_mca3[i][j] = averaged_mca3[i][j] / counter

                        averaged_mca4[i][j] = averaged_mca4[i][j] + mca_array[3][grid_array[i][j][k]]
                        averaged_mca4[i][j] = averaged_mca4[i][j] / counter

        return  averaged_tey, averaged_i0, averaged_diode, averaged_mca1, averaged_mca2, averaged_mca3, averaged_mca4


    def calculate_pfy(self, enStart, enStop):
        # print "Getting PFY ROIs"
        mca_array = self.get_mca_array()

        pfy1 = []
        pfy2 = []
        pfy3 = []
        pfy4 = []
        pfy = [[], [], [], []]

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