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

from battle.landBattleMap import LandBattleMap
from battle.landArmy import LandArmy
from unit.LandUnit import LandUnit


class LandBattle:
    """Class LandBattle
    """
    # Attributes:
    autoCombat = None  # (boolean)
    turn = None  # (int)
    currentUnit = None  # (LandUnit)
    targettedUnit = None  # (LandUnit)

    # Operations
    def draw_current_unit(self, scene, size):
        """function draw_current_unit

        scene: QGraphicsScene
        size: QSize

        returns
        """
        raise NotImplementedError()
        return None

    def draw_targetted_unit(self, scene, size):
        """function draw_targetted_unit

        scene: QGraphicsScene
        size: QSize

        returns
        """
        raise NotImplementedError()
        return None

    def draw_battle_map(self, scene, size):
        """function draw_battle_map

        scene: QGraphicsScene
        size: QSize

        returns
        """
        raise NotImplementedError()
        return None

    def draw_defender(self, scene, size):
        """function draw_defender

        scene: QGraphicsScene
        size: QSize

        returns
        """
        raise NotImplementedError()
        return None

    def draw_attacker(self, scene, size):
        """function draw_attacker

        scene: QGraphicsScene
        size: QSize

        returns
        """
        raise NotImplementedError()
        return None

    def play_turn(self):
        """function play_turn

        returns
        """
        raise NotImplementedError()
        return None
