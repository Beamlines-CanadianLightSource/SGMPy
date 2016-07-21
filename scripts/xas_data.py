class XASData(object):
    def __init__(self, data):
        self.energy_array = data[0]
        self.sdd_array = data[1] 
        self.scaler_array = data[2]
        self.pfy_sdd_array = None
        
    def get_energy_array(self):
        return self.energy_array
    
    def get_sdd_array(self):
        return self.sdd_array
        
    def set_scaler_array(self, scaler_array):
        self.scaler_array = scaler_array
        
    def get_scaler_array(self):
        return self.scaler_array
    
    def set_pfy_sdd_array(self, pfy_sdd):
        self.pfy_sdd_array = pfy_sdd
        
    def get_pfy_sdd_array(self):
        return self.pfy_sdd_array
    
# subclass of XASData; it is the data type for normalized xas data    
class XASNormalizedData(XASData):

    def __init__(self, data):
        # energy_array is mean energy
        self.energy_array = data[0]
        self.assigned_data_array = data[1] 
        self.scaler_raw_array = data[2]
        self.empty_bin_front = data[3]
        self.empty_bin_back = data[4]
        self.sdd_binned_array = data[5]
        # scaler_array is averaged scaler
        self.scaler_array = None
        # pfy_sdd is averaged sdd
        self.pfy_sdd_array = None

    
    def get_assigned_data_array(self):
        return self.assigned_data_array 
    
    def get_empty_bin_front(self):
        return self.empty_bin_front
        
    def get_empty_bin_back(self):
        return self.empty_bin_back
    
    def get_scaler_raw_array(self):
        return self.scaler_raw_array
    
    def get_sdd_binned_array(self):
        return self.sdd_binned_array
    