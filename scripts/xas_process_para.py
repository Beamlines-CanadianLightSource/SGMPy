class XASProcessPara:

    def __init__(self, energy_start, energy_end, roi_start, roi_end, bin_interval):
        self.energy_start = energy_start
        self.energy_end = energy_end
        self.roi_start = roi_start
        self.roi_end = roi_end
        self.bin_interval = bin_interval

    def get_energy_start(self):
        return self.energy_start

    def get_energy_end(self):
        return self.energy_end

    def get_roi_start(self):
        return self.roi_start

    def get_roi_end(self):
        return self.roi_end

    def get_bin_interval(self):
        return self.bin_interval
