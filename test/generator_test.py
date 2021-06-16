"""
Test Class
Citations:
Muller, David. "How To Use unittest to Write a Test Case for a Function in Python." 
    Digital Ocean, 30 Sept. 2020, www.digitalocean.com/community/tutorials/
    how-to-use-unittest-to-write-a-test-case-for-a-function-in-python. 
    
"""
import os
import unittest
import random
import math
from src.spectra_generator import generator

class TestDataset(unittest.TestCase):
    def setUp(self):
        rmf_list = ['rmf_arf/Extracted_From_Calb/swxpc0to12s0_20010101v010.rmf', 'rmf_arf/Extracted_From_Calb/swxpc0to12s6_20010101v010.rmf']
        arf_list = ['ESO242G008','Mkn1044','Mkn1048','MRk335','MS0117-28','QSO005636', 'RXJ0100.4-5113', 'RXJ0105.6-1416','RXJ0117.5-3826'
               ,'RXJ0128.1-1848','RXJ0134.2-4258','RXJ0136.9-3510','RXJ0148.3-2758','RXJ0152.4-2319','TonS180']
        self.spectra_generator = generator(rmf_list, arf_list)
##    
##    def tearDown(self):
##        #https://careerkarma.com/blog/python-check-if-file-exists/
##        file_exist = os.path.isfile(".\\test\\clean_fake_data.csv")
##        if file_exist:
##            os.remove(".\\test\\clean_fake_data.csv")
##        
    def test_rmf_picker_success(self):
        random.seed(1)
        actual = self.spectra_generator._generator__rmf_picker()
        expected = ('rmf_arf/Extracted_From_Calb/swxpc0to12s0_20010101v010.rmf', 0)
        self.assertEqual(actual, expected)

    def test_arf_picker_success(self):
        random.seed(1)
        actual = self.spectra_generator._generator__arf_picker()
        expected = ('rmf_arf/Mkn1048/Mkn1048pc.arf', 2)
        self.assertEqual(actual, expected)

    def test_param_selector_success(self):
        random.seed(1)
        actual = self.spectra_generator._generator__param_selector()
        expected = (70*10**6,4727,0.07876482335195467,0.8803597602503538,math.cos(math.radians(26)),0.04291779017385818,16728, self.spectra_generator._generator__normalizer(70*10**6,4727,0.07876482335195467,0.8803597602503538,math.cos(math.radians(26)),0.04291779017385818))
        self.assertEqual(actual, expected)

    def test_normalizer_success(self):
        mass = 10*10**6
        dist = 74
        logmdot = -1.5
        astar = 0.4
        cosi = math.cos(math.radians(11))
        redshift = 0.03
        actual = self.spectra_generator._generator__normalizer(mass, dist, logmdot, astar, cosi, redshift)
        mass_n = (mass - 2*10**6)/(450*10**6-2*10**6)
        dist_n = (dist - 65)/(6000-65)
        logmdot_n = (logmdot + 1.65)/(0.39+1.65)
        astar_n = (astar - 0.5)/(0.998-0.5)
        cosi_n = (cosi - math.cos(math.radians(50)))/(math.cos(math.radians(10))-math.cos(math.radians(50)))
        redshift_n = (redshift - 0.002)/(0.349-0.002)
        self.assertEqual(actual, [mass_n, dist_n, logmdot_n, astar_n, cosi_n, redshift_n])
        
        
        
