import os
import unittest
from scripts.open_spec import *


class TestOpenSpec(unittest.TestCase):
    
#	def test_get_abs_path(self):
#		abs_file_path = get_abs_path("data/spectra_example.dat")
#		expect_abs_path =  "/home/travis/build/Beamlines-CanadianLightSource/SGM-Beamline/spectra_example.dat"
#		self.assertEqual(abs_file_path, expect_abs_path)

	def test_get_total_scannum(self):
		expected_scan_num = 10
        
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)
		print abs_file_path
		opened_file = open_spec_data_file(abs_file_path)

		real_scan_num = get_total_scan_num(opened_file)
		print real_scan_num
		self.assertEqual(real_scan_num, expected_scan_num)

        
	def test_get_diff_scan_case1(self):
		abs_file_path = get_abs_path("data/spectra_example.dat")
		opened_file = open_spec_data_file(abs_file_path)
		scan_array = get_diff_scan(opened_file)
		expected_cscan_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
		expected_ascan_array = []
		expected_cmesh_scan_array = []
		expected_mesh_scan_array = []
		self.assertEqual(scan_array[0], expected_cscan_array)
		self.assertEqual(scan_array[1], expected_ascan_array)
		self.assertEqual(scan_array[2], expected_cmesh_scan_array)
		self.assertEqual(scan_array[3], expected_mesh_scan_array)
        
	def test_get_diff_scan_case2(self):
		abs_file_path = get_abs_path("data/diffscan_example.dat")
		opened_file = open_spec_data_file(abs_file_path)
		scan_array = get_diff_scan(opened_file)
		expected_cscan_array = [4, 5, 6, 8, 9, 10]
		expected_ascan_array = [7]
		expected_cmesh_scan_array = [1, 2, 3]
		expected_mesh_scan_array = []
		self.assertEqual(scan_array[0], expected_cscan_array)
		self.assertEqual(scan_array[1], expected_ascan_array)
		self.assertEqual(scan_array[2], expected_cmesh_scan_array)
		self.assertEqual(scan_array[3], expected_mesh_scan_array)
        
	def test_get_cmesh_scan(self):
		abs_file_path = get_abs_path("data/diffscan_example.dat")
		opened_file = open_spec_data_file(abs_file_path)
		cmesh_scan = get_cmesh_scan(opened_file)
		expect_cmesh_scan = ['1', '2', '3']
		self.assertEqual(cmesh_scan, expect_cmesh_scan)
        
	def test_get_c_scan(self):
		abs_file_path = get_abs_path("data/diffscan_example.dat")
		opened_file = open_spec_data_file(abs_file_path)
		cmesh_scan = get_c_scan(opened_file)
		expect_cmesh_scan = [u'5', u'6', u'8', u'9', u'10']
		self.assertEqual(cmesh_scan, expect_cmesh_scan)
        
        
	def initialize():
		return MyTestCase

if __name__ == '__main__':
	unittest.main()