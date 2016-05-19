import unittest
from scripts.summary_plot import *
import os
import numpy as np


class TestSummaryPlot(unittest.TestCase):

	def test_getAllScanNum(self):
		expectedScanNum = list(range(1,11))
        
		script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
		rel_path = "data/spectra_example.dat"
		abs_file_path = os.path.join(script_dir, rel_path)
        
		realScanNum = getAllScanNum(abs_file_path)
		self.assertEqual(realScanNum, expectedScanNum)

        
	def test_generateGoodScanArray(self):
		originalScanNum = list(range(1,11))
		badScanNum = "4 , 7 , 10"
		expectedGoodScanNum = [1, 2, 3, 5, 6, 8, 9]
		self.assertEqual(generateGoodScanArray(originalScanNum, badScanNum), expectedGoodScanNum)

if __name__ == '__main__':
	unittest.main()