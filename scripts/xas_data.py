class XASData(object):
    def __init__(self, data):
        self.energy_array = data[0]
        self.mca_array = data[1] 
        self.scaler_array = data[2]
        self.pfy_sdd = None
        
    def get_energy_array(self):
        return self.energy_array
    
    def get_mca_array(self):
        return self.mca_array
        
    def get_scaler_array(self):
        return self.scaler_array
    
    def set_pfy_sdd(self, pfy_sdd):
        self.pfy_sdd = pfy_sdd
        
    def get_pfy_sdd(self):
        return self.pfy_sdd