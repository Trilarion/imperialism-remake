import unittest
from lib.QHexagon import QHexagon
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPolygonF
import math   


class QHexagonTestCase(unittest.TestCase):

    def test_0(self):
        self.assertTrue(True)
        
    def test_width0(self):
        center = QPointF(0.0, 0.0)
        hexa = QHexagon(center, 0, 0)
        self.assertEqual(hexa.width(), 0)

    def test_width1(self):
        center = QPointF(0.0, 0.0)
        hexa = QHexagon(center, 1, 0)
        self.assertEqual(hexa.width(), math.sqrt(3)/2)

    def test_width2(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 2/math.sqrt(3), 0)
        self.assertEqual(hexa.width(), 1)

    def test_height0(self):
        center = QPointF(0.0, 0.0)
        hexa = QHexagon(center, 0, 0)
        self.assertEqual(hexa.height(), 0)

    def test_height1(self):
        center = QPointF(0.0, 0.0)
        hexa = QHexagon(center, 1, 0)
        self.assertEqual(hexa.height(), 3/4)

    def test_height2(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 4/3, 0)
        self.assertEqual(hexa.height(), 1)

    def test_init0(self):
        try:
            hexa = QHexagon(1, 4/3, 0)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True) 

    def test_init1(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, center, 0)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True) 

    def test_init2(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, -1, 0)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True)             
 
    def test_init3(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, 0)
            self.assertTrue(True) 
        except ValueError:
            self.assertTrue(False)       

    def test_init4(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, -5)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True) 


    def test_init5(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, 5)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True)             
 
    def test_init6(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, 30.0)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True) 


    def test_init7(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, 0.0)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True)           

    def test_init8(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, -30)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True)   

    def test_init9(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, center)
            self.assertTrue(False) 
        except ValueError:
            self.assertTrue(True)   
            
    def test_init10(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, 30)
            self.assertTrue(True) 
        except ValueError:
            self.assertTrue(False)         
            
    def test_init11(self):
        try:
            center = QPointF(1.0, 5.0)
            hexa = QHexagon(center, 1, 0)
            self.assertTrue(True) 
        except ValueError:
            self.assertTrue(False)                

    def test_eq0(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 1, 0)
        hexa2 = QHexagon(center, 1, 0)
        self.assertTrue(hexa==hexa2) 

    def test_eq1(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 1, 0)
        hexa2 = QHexagon(center, 2, 0)
        self.assertFalse(hexa==hexa2)         
 
    def test_eq2(self):
        center = QPointF(1.0, 5.0)
        center2 = QPointF(2.0, 5.0)
        hexa = QHexagon(center, 1, 0)
        hexa2 = QHexagon(center2, 1, 0)
        self.assertFalse(hexa==hexa2) 
 
    def test_eq3(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 1, 30)
        hexa2 = QHexagon(center, 1, 0)
        self.assertFalse(hexa==hexa2)  
 
# Ceci lance le test si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()