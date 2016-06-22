import os
import unittest
from scripts.open_spec import *


class TestOpenSpec(unittest.TestCase):

	def test_get_total_Scannum(self):
		expectedScanNum = 10
        
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)
		print abs_file_path
		opened_file = open_spec_data_file(abs_file_path)

		realScanNum = get_total_scan_num(opened_file)
		print realScanNum
		self.assertEqual(realScanNum, expectedScanNum)

	@unittest.skip("demonstrating skipping")
	def test_check_file_type_case1(self):
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)   
		self.assertEqual(checkFileType(abs_file_path), "This is the data file of spectra.")
   
	@unittest.skip("demonstrating skipping")
	def test_check_file_type_case2(self):
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/map_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)       
		self.assertEqual(checkFileType(abs_file_path), "This is a map data file.")
        
	def test_check_scan_variety_case1(self):
		abs_file_path = get_abs_path("data/spectra_example.dat")
		opened_file = open_spec_data_file(abs_file_path)
		scan_array = check_scan_variety(opened_file)
		expected_cscan_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		expected_ascan_array = []
		expected_cmesh_scan_array = []
		expected_mesh_scan_array = []
		self.assertEqual(scan_array[0], expected_cscan_array)
		self.assertEqual(scan_array[1], expected_ascan_array)
		self.assertEqual(scan_array[2], expected_cmesh_scan_array)
		self.assertEqual(scan_array[3], expected_mesh_scan_array)
        
	def test_check_scan_variety_case2(self):
		abs_file_path = get_abs_path("data/diffscan_example.dat")
		opened_file = open_spec_data_file(abs_file_path)
		scan_array = check_scan_variety(opened_file)
		expected_cscan_array = [4, 5, 6, 8, 9, 10]
		expected_ascan_array = [7]
		expected_cmesh_scan_array = [1, 2, 3]
		expected_mesh_scan_array = []
		self.assertEqual(scan_array[0], expected_cscan_array)
		self.assertEqual(scan_array[1], expected_ascan_array)
		self.assertEqual(scan_array[2], expected_cmesh_scan_array)
		self.assertEqual(scan_array[3], expected_mesh_scan_array)  
        
        
	def initialize():
		return MyTestCase

if __name__ == '__main__':
	unittest.main()