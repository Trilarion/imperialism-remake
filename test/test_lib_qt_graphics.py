"""
    Tests lib/qt_graphics
"""

import unittest

import PyQt5.QtCore as QtCore

import lib.qt_graphics as qt_graphics

class TestRelativeLayout(unittest.TestCase):

    def test_calculate_constraints(self):

        parent = QtCore.QRect(10, 10, 1000, 500)
        size = QtCore.QSize(200, 100)

        constraint = qt_graphics.RelativeLayoutConstraint().south(10).west(20)
        x,y = qt_graphics.calculate_relative_position(parent, size, constraint)
        self.assertEqual((x,y), (30, 400))

        constraint = qt_graphics.RelativeLayoutConstraint().north(30).east(40)
        x, y = qt_graphics.calculate_relative_position(parent, size, constraint)
        self.assertEqual((x, y), (770, 40))

        constraint = qt_graphics.RelativeLayoutConstraint().center_horizontal().center_vertical()
        x1, y1 = qt_graphics.calculate_relative_position(parent, size, constraint)
        self.assertEqual((x1, y1), (410, 210))


class TestZStacking(unittest.TestCase):

    def test_z_stacking(self):

        manager = qt_graphics.ZStackingManager()

if __name__ == '__main__':
    unittest.main()