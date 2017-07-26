# Imperialism remake
# Copyright (C) 2016 Trilarion
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

"""
Tests lib/qt
"""

import unittest
from PyQt5 import QtCore
from imperialism_remake.lib import qt

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