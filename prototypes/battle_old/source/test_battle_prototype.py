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
import sys
import unittest

from PyQt5.QtWidgets import QApplication

testmodules = [
    'testcase.configparserextendedTestCase',
    'testcase.configTestCase',
    'testcase.constantsTestCase',
    'testcase.hexagonTestCase',
    'testcase.landArmyTestCase',
    'testcase.landBattleFieldTestCase',
    'testcase.landBattleFieldTypeTestCase',
    'testcase.landBattleMapTestCase',
    'testcase.landBattleTestCase',
    'testcase.landBattleViewTestCase',
    'testcase.landUnitInBattleTestCase',
    'testcase.landUnitTestCase',
    'testcase.landUnitTypeTestCase',
    'testcase.langTestCase',
    'testcase.nationTestCase',
    'testcase.themeTestCase',
    'testcase.landBattleResultViewTestCase'
]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the testcase cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

# Launch the tests if the script is called directly.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.TextTestRunner().run(suite)
