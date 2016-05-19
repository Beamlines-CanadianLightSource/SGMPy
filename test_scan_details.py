import unittest
from scripts.scan_details import*
import os


class TestScanDetails(unittest.TestCase):

	def test_getTotalScanNum(self):
		expectedScanNum = 10
        
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)
        
		realScanNum = getTotalScanNum(abs_file_path)
		print realScanNum
		self.assertEqual(realScanNum, expectedScanNum)

        
	def test_checkFileType_case1(self):
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)   
		self.assertTrue(checkFileType(abs_file_path), "This is the data file of spectra.")
   

	def test_checkFileType_case2(self):
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/map_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)       
		self.assertTrue(checkFileType(abs_file_path), "This is a map data file.")
        
	def initialize():
		return MyTestCase

if __name__ == '__main__':
    unittest.main()