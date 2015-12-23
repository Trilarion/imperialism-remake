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

from battle.landBattleField import LandBattleField
from unit.LandUnit import LandUnit


class LandUnitInBattle(LandUnit):
    """Class LandUnitInBattle
    """
    # Attributes:
    dead = None  # (boolean)
    status = {Charge, Shoot, Stand}  # (enum)
    retreat = None  # (boolean)
    morale = [0, 100]  # (int)
    moveUsed = None  # (int)
    hasShoot = None  # (boolean)

    # Operations
    def can_shoot(self, unit):
        """function can_shoot

        unit: LandUnit

        returns boolean
        """
        raise NotImplementedError()
        return None

    def shoot(self, unit):
        """function shoot

        unit: LandUnit

        returns boolean
        """
        raise NotImplementedError()
        return None

    def can_move_to(self, field):
        """function can_move_to

        field: LandBattleField

        returns boolean
        """
        raise NotImplementedError()
        return None

    def move_to(self, field):
        """function move_to

        field: LandBattleField

        returns boolean
        """
        raise NotImplementedError()
        return None

    def increase_moral(self):
        """function increase_moral

        returns boolean
        """
        return None  # should raise NotImplementedError()

    def play_turn(self):
        """function play_turn

        returns
        """
        raise NotImplementedError()
        return None

    def __str__(self):
        """function __str__

        returns string
        """
        raise NotImplementedError()
        return None

    def print_to_text_edit(self, font, text_edit):
        """function print_to_text_edit

        font: QFont
        textEdit: QTextEdit

        returns
        """
        raise NotImplementedError()
        return None
