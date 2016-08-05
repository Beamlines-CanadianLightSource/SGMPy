import unittest
from ..scripts.xas_process import XASProcess
from ..scripts.open_spec import OpenMultiCScan


class TestXASSummaryPlot(unittest.TestCase):
        
    def test_generate_good_scan_array_case1(self):
        xas_process = XASProcess("multiple")
        opened_xas_data = OpenMultiCScan()
        originalScanNum = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10']
        opened_xas_data.set_c_scan(originalScanNum)

        badScanNum = "4 , 7 , 10"
        expectedGoodScanNum = [1, 2, 3, 5, 6, 8, 9]
        self.assertEqual(xas_process.generate_good_scan_index(opened_xas_data, badScanNum), expectedGoodScanNum)
                         
    def test_generate_good_scan_array_case2(self):
        xas_process = XASProcess("multiple")
        opened_xas_data = OpenMultiCScan()
        originalScanNum = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'10']
        opened_xas_data.set_c_scan(originalScanNum)

        badScanNum = "  1 , 6 , 10   "
        expectedGoodScanNum = [2, 3, 4, 5, 7, 8, 9]
        self.assertEqual(xas_process.generate_good_scan_index(opened_xas_data, badScanNum), expectedGoodScanNum)
                        
                         
if __name__ == '__main__':
	unittest.main()