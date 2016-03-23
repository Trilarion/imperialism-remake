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

import unittest

from prototypes.battle.source.battle.land.landBattleFieldType import LandBattleFieldType


class LandBattleFieldTypeTestCase(unittest.TestCase):
    """Class LandBattleFieldTypeTestCase
    """

    def test_init0(self):
        try:
            LandBattleFieldType("testcase", None, None)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init1(self):
        try:
            LandBattleFieldType("testcase", '#0000FF', None)
            self.assertTrue(True)
        except ValueError:
            self.assertTrue(False)

    def test_init2(self):
        try:
            LandBattleFieldType("testcase", None, 1)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)

    def test_init3(self):
        try:
            LandBattleFieldType("", '#00FFFF', None)
            self.assertTrue(False)
        except ValueError:
            self.assertTrue(True)


# Ceci lance le testcase si on exécute le script
# directement.
if __name__ == '__main__':
    unittest.main()
