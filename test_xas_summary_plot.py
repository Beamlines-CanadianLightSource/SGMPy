import unittest
from scripts.xas_summary_plot import *
from scripts.xas_binned import *
#from mock import patch
import os
import numpy as np


class TestXASSummaryPlot(unittest.TestCase):
        
	def test_generate_good_scan_array_case1(self):
		originalScanNum = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10']
		badScanNum = "4 , 7 , 10"
		expectedGoodScanNum = [1, 2, 3, 5, 6, 8, 9]
		self.assertEqual(generate_good_scan_index(originalScanNum, badScanNum), expectedGoodScanNum)
                         
	def test_generate_good_scan_array_case2(self):
		originalScanNum = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10']
		badScanNum = "  1 , 6 , 10   "
		expectedGoodScanNum = [2, 3, 4, 5, 7, 8, 9]
		self.assertEqual(generate_good_scan_index(originalScanNum, badScanNum), expectedGoodScanNum)                   
     
	# @patch is only for Travis CI automation testing
	#@patch("matplotlib.pyplot.show")
	def test_summary_plot(self):
		abs_file_path = get_abs_path = "data/spectra_example.dat"
		opened_file = open_spec_data_file(abs_file_path)
		energy_array, mca_array, scaler_array, scan_num = open_all_sgm_xas(opened_file)                   
		expected_array = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10']
		actual_array = summary_plot(energy_array, scaler_array, scan_num, "TEY")
		self.assertEqual(actual_array, expected_array)
                         
                         
if __name__ == '__main__':
	unittest.main()