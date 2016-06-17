import unittest
from scripts.xas_summary_plot import *
from mock import patch
import os
import numpy as np


class TestXASSummaryPlot(unittest.TestCase):

	def test_get_all_scan_num(self):
		expectedScanNum = list(range(1,11))
        
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)
		opened_file = open_spec_data_file(abs_file_path)
		realScanNum = get_all_scan_num(opened_file)
		self.assertEqual(realScanNum, expectedScanNum)

        
	def test_generate_good_scan_array_case1(self):
		originalScanNum = list(range(1,11))
		badScanNum = "4 , 7 , 10"
		expectedGoodScanNum = [1, 2, 3, 5, 6, 8, 9]
		self.assertEqual(generate_good_scan_array(originalScanNum, badScanNum), expectedGoodScanNum)
                         
	def test_generate_good_scan_array_case2(self):
		originalScanNum = list(range(1,11))
		badScanNum = "  1 , 6 , 10   "
		expectedGoodScanNum = [2, 3, 4, 5, 7, 8, 9]
		self.assertEqual(generate_good_scan_array(originalScanNum, badScanNum), expectedGoodScanNum)                   
     
	# @patch is only for Travis CI automation testing
    @patch("matplotlib.pyplot.show")
	def test_summary_plot(self, mock_show):
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)
		opened_file = open_spec_data_file(abs_file_path)
                               
		expected_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		actual_array = summary_plot(opened_file, "TEY")
		self.assertEqual(actual_array, expected_array)                   
                         
                         
if __name__ == '__main__':
	unittest.main()