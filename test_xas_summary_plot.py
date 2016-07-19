import unittest
from scripts.xas_summary_plot import *
from scripts.xas_binned import *


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
                        
                         
if __name__ == '__main__':
	unittest.main()