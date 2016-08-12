import numpy as np

def create_grid(x_start_energy, x_end_energy, x_num_of_bins, y_start_energy, y_end_energy, y_num_of_bins):
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
