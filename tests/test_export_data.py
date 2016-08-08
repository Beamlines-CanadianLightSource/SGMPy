import unittest
from ..scripts.export_data import ExportData
from ..scripts.open_spec import *

class TestExportData(unittest.TestCase):

    def test_get_date_time(self):
        data_set = None
        export = ExportData('user/data', data_set)

        abs_file_path = get_abs_path("data/spectra_example.dat")
        opened_file = open_spec_data_file(abs_file_path)

        actual_str = export.get_date_time(opened_file)
        expected_str = "May 15 11:19:51 2016"
        self.assertEqual(actual_str, expected_str)
        
    def test_get_comments(self):
        data_set = None
        export = ExportData('user/data', data_set)

        abs_file_path = get_abs_path("data/diffscan_example.dat")
        actual_comments = export.get_comments(abs_file_path)
        
        expected_comments = []
        expected_comments.append('#C spec  User = sgm\n')
        expected_comments.append('#C Fri May 20 13:58:04 2016.  Photon Energy: 1999.98, Grating: High Energy.\n')
        expected_comments.append('#C Fri May 20 13:58:04 2016.  Exit Slit: 9.98293, Stripe: Silicon.\n') 
        expected_comments.append('#C Fri May 20 13:58:04 2016.  Gain PD: 20 uA/V.\n')
        expected_comments.append('#C Fri May 20 13:58:04 2016.  Gain TEY: 20 pA/V.\n')
        expected_comments.append('#C Fri May 20 13:58:04 2016.  Gain I0: 1 nA/V.\n')
        expected_comments.append('#C Fri May 20 13:58:04 2016.  ROI1: 30 to 45.\n')
        expected_comments.append('#C Fri May 20 13:58:04 2016.  ROI2: 1 to 1023.\n')

        # print expected_comments
        # print actual_comments
        self.assertEqual(actual_comments, expected_comments)

        
    def test_get_grating_hdf5(self):
        data_set = None
        export = ExportData('user/data', data_set)

        comments = [ 'Fri May 20 14:03:45 2016.  Scan done. Turning off beam..\nFri May 20 14:27:39 2016.  Photon Energy: 1999.94, Grating: High Energy.\nFri May 20 14:27:39 2016.  Exit Slit: 30.0191, Stripe: Silicon.\nFri May 20 14:27:39 2016.  Gain PD: 20 uA/V.\nFri May 20 14:27:39 2016.  Gain TEY: 20 pA/V.\nFri May 20 14:27:39 2016.  Gain I0: 1 nA/V.\nFri May 20 14:27:39 2016.  ROI1: 165 to 185.\nFri May 20 14:27:39 2016.  ROI2: 190 to 220.']
        actual_grating = export.get_grating_hdf5(comments)
        expected_grating = "High Energy"
        self.assertEqual(actual_grating, expected_grating)
        
        
    def test_get_exit_slit_and_stripe(self):
        data_set = None
        export = ExportData('user/data', data_set)

        comments = [ 'Fri May 20 14:03:45 2016.  Scan done. Turning off beam..\nFri May 20 14:27:39 2016.  Photon Energy: 1999.94, Grating: High Energy.\nFri May 20 14:27:39 2016.  Exit Slit: 30.0191, Stripe: Silicon.\nFri May 20 14:27:39 2016.  Gain PD: 20 uA/V.\nFri May 20 14:27:39 2016.  Gain TEY: 20 pA/V.\nFri May 20 14:27:39 2016.  Gain I0: 1 nA/V.\nFri May 20 14:27:39 2016.  ROI1: 165 to 185.\nFri May 20 14:27:39 2016.  ROI2: 190 to 220.']
        actual_exit_slit, actual_stripe = export.get_exit_slit_and_stripe(comments)
        expected_exit_slit = "30.0191"
        expected_stripe = " Silicon"
        self.assertEqual(actual_exit_slit, expected_exit_slit)
        self.assertEqual(actual_stripe, expected_stripe)


if __name__ == '__main__':
    unittest.main()