#!/usr/bin/python3
# Imperialism remake
# Copyright (C) 2015 Spitaels <spitaelsantoine@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

import math
import unittest

from PyQt5.QtCore import QPointF

from lib.hexagon import QHexagon


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
        self.assertEqual(hexa.width(), math.sqrt(3) / 2)

    def test_width2(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 2 / math.sqrt(3), 0)
        self.assertEqual(hexa.width(), 1)

    def test_height0(self):
        center = QPointF(0.0, 0.0)
        hexa = QHexagon(center, 0, 0)
        self.assertEqual(hexa.height(), 0)

    def test_height1(self):
        center = QPointF(0.0, 0.0)
        hexa = QHexagon(center, 1, 0)
        self.assertEqual(hexa.height(), 3 / 4)

    def test_height2(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 4 / 3, 0)
        self.assertEqual(hexa.height(), 1)

    def test_init0(self):
        try:
            QHexagon(1, 4 / 3, 0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init1(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, center, 0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init2(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, -1, 0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init3(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, 0)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(False)

    def test_init4(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, -5)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init5(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, 5)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init6(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, 30.0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init7(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, 0.0)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init8(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, -30)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init9(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, center)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init10(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, 30)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(False)

    def test_init11(self):
        try:
            center = QPointF(1.0, 5.0)
            QHexagon(center, 1, 0)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(False)

    def test_eq0(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 1, 0)
        hexa2 = QHexagon(center, 1, 0)
        self.assertTrue(hexa == hexa2)

    def test_eq1(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 1, 0)
        hexa2 = QHexagon(center, 2, 0)
        self.assertFalse(hexa == hexa2)

    def test_eq2(self):
        center = QPointF(1.0, 5.0)
        center2 = QPointF(2.0, 5.0)
        hexa = QHexagon(center, 1, 0)
        hexa2 = QHexagon(center2, 1, 0)
        self.assertFalse(hexa == hexa2)

    def test_eq3(self):
        center = QPointF(1.0, 5.0)
        hexa = QHexagon(center, 1, 30)
        hexa2 = QHexagon(center, 1, 0)
        self.assertFalse(hexa == hexa2)

        # Ceci lance le testcase si on exécute le script


# directement.
if __name__ == '__main__':
    unittest.main()
