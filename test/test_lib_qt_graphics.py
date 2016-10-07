"""
    Tests lib/qt
"""

import unittest

import PyQt5.QtCore as QtCore

import lib.qt as qt

class TestRelativeLayout(unittest.TestCase):

    def test_calculate_constraints(self):

        parent = QtCore.QRect(10, 10, 1000, 500)
        size = QtCore.QSize(200, 100)

        constraint = qt.RelativeLayoutConstraint().south(10).west(20)
        x,y = qt.calculate_relative_position(parent, size, constraint)
        self.assertEqual((x,y), (30, 400))

        constraint = qt.RelativeLayoutConstraint().north(30).east(40)
        x, y = qt.calculate_relative_position(parent, size, constraint)
        self.assertEqual((x, y), (770, 40))

        constraint = qt.RelativeLayoutConstraint().center_horizontal().center_vertical()
        x1, y1 = qt.calculate_relative_position(parent, size, constraint)
        self.assertEqual((x1, y1), (410, 210))


class TestZStacking(unittest.TestCase):

    def test_z_stacking(self):

        manager = qt.ZStackingManager()

if __name__ == '__main__':
    unittest.main()