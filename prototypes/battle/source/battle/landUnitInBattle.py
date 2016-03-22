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

from unit.landUnit import LandUnit


class LandUnitInBattle(LandUnit):
    """Class LandUnitInBattle
    """

    # Constructor:
    def __init__(self, dead, status, retreat, moral, unit_strength, experience_level, unit_type, nation):
        """function __init__
        :param dead: bool
        :param status: str {'Charge', 'Shoot', 'Stand'}
        :param retreat: bool
        :param moral: int range(0,100)
        :param unit_strength: int range(0,100)
        :param experience_level: int range(1,5)
        :param unit_type: LandUnitType
        :param nation: Nation
        """
        super().__init__(moral, unit_strength, experience_level, unit_type, nation)
        if not isinstance(dead, bool):
            raise ValueError('dead must be a boolean')
        if not isinstance(retreat, bool):
            raise ValueError('retreat must be a boolean')
        if not isinstance(status, str) or (status != 'Charge' and status != 'Shoot' and status != 'Stand'):
            raise ValueError('status must be a str in {\'Charge\', \'Shoot\', \'Stand\'}')
        self.dead = dead
        self.status = status
        self.retreat = retreat
        self.moveUsed = 0
        self.hasShoot = False

    # Operations
    def can_shoot(self, unit):
        """function can_shoot

        :param unit: LandUnit

        returns boolean
        """
        raise NotImplementedError()

    def shoot(self, unit):
        """function shoot

        :param unit: LandUnit

        returns boolean
        """
        raise NotImplementedError()

    def can_move_to(self, field):
        """function can_move_to

        :param field: LandBattleField

        returns boolean
        """
        raise NotImplementedError()

    def move_to(self, field):
        """function move_to

        :param field: LandBattleField

        returns boolean
        """
        raise NotImplementedError()

    def increase_moral(self):
        """function increase_moral

        returns boolean
        """
        raise NotImplementedError()

    def play_turn(self):
        """function play_turn

        returns
        """
        raise NotImplementedError()

    def __str__(self):
        """function __str__

        returns string
        """
        raise NotImplementedError()

    def print_to_text_edit(self, font, text_edit):
        """function print_to_text_edit

        :param font: QFont
        :param text_edit: QTextEdit

        returns
        """
        raise NotImplementedError()
