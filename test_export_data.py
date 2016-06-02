import os
import unittest
from scripts.export_data import *


class TestExportData(unittest.TestCase):

	def test_get_header(self):
        
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)

		headers = get_header(abs_file_path)
		actual_array_lengh = len(headers)
		print actual_array_lengh
		expected_array_lengh = 19
		self.assertEqual(actual_array_lengh, expected_array_lengh)
            
	def test_get_date_time(self):
        
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)

		headers = get_header(abs_file_path)
		actual_str = get_date_time(headers)
		expected_str = "Sun May 15 11:19:51 2016\n"
		self.assertEqual(actual_str, expected_str)

        
	def initialize():
		return MyTestCase

if __name__ == '__main__':
	unittest.main()