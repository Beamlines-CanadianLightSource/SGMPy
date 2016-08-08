import os
import unittest
from ..scripts.open_spec import *


class TestOpenSpec(unittest.TestCase):
    
#	def test_get_abs_path(self):
#		abs_file_path = get_abs_path("data/spectra_example.dat")
#		expect_abs_path =  "/home/travis/build/Beamlines-CanadianLightSource/SGMPy/spectra_example.dat"
#		self.assertEqual(abs_file_path, expect_abs_path)

        
    def test_get_diff_scan_case1(self):
        abs_file_path = get_abs_path("data/spectra_example.dat")
        scan_array = get_diff_scan(abs_file_path)
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
        scan_array = get_diff_scan(abs_file_path)
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
        cscan = get_c_scan(opened_file)
        expect_cscan = [u'5', u'6', u'8', u'9', u'10']
        self.assertEqual(cscan, expect_cscan)


if __name__ == '__main__':
    unittest.main()