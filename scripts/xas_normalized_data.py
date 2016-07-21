class XASNormalizedData(XASData):

    def __init__(self, data):
        self.energy_array = data[0]
        self.assigned_data_array = data[1] 
        self.scaler_array = data[2]
        self.empty_bin_front = data[3]
        self.empty_bin_back = data[4]
        self.sdd_bin_data = data[5]
        self.scaler_bin_data = None
        self.pfy_bin_data = None

    def set_scaler_bin_data(self, scaler_bin_data):
        self.scaler_bin_data = scaler_bin_data
         
    def get_scaler_bin_data(self):
        return self.scaler_bin_data
    
    def set_pfy_bin_data(self, pfy_bin_data):
        self.pfy_bin_data = pfy_bin_data
        
    def get_pfy_bin_data(self):
        return self.pfy_bin_data
            
    def get_mean_energy(self):
        return self.mean_energy_array
    
    def get_assigned_data_array(self):
        return self.assigned_data_array 
        
    def get_scaler_array(self):
        return self.scaler_array
    
    def get_empty_bin_front(self):
        return self.empty_bin_front
        
    def get_empty_bin_back(self):
        return self.empty_bin_back
    
    def get_sdd_bin_data(self):
        return self.sdd_bin_data