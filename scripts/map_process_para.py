class MapProcessPara:

    def __init__(self, x_start_energy, x_end_energy, x_bin_num, y_start_energy, y_end_energy, y_bin_num):
        self.x_start_energy = x_start_energy
        self.x_end_energy = x_end_energy
        self.x_bin_num = x_bin_num
        self.y_start_energy = y_start_energy
        self.y_end_energy = y_end_energy
        self.y_bin_num = y_bin_num

    def get_x_start_energy(self):
        return self.x_start_energy

    def get_x_end_energy(self):
        return self.x_end_energy

    def get_x_bin_num(self):
        return self.x_bin_num

    def get_y_start_energy(self):
        return self.y_start_energy

    def get_y_end_energy(self):
        return self.y_end_energy

    def get_y_bin_num(self):
        return self.y_bin_num
