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
from battle.landUnitInBattle import LandUnitInBattle


class LandBattle:
    """Class LandBattle
    """

    # Constructor:
    def __init__(self, auto_combat, turn, current_unit, targetted_unit, map_battle, defender, attacker):
        """

        :param auto_combat: bool
        :param turn: int > 0
        :param current_unit: LandUnitInBattle
        :param targetted_unit: LandUnitInBattle
        :param map_battle: LandBattleMap
        :param defender: LandArmy
        :param attacker: LandArmy
        :return:
        """
        if not isinstance(auto_combat, bool):
            raise ValueError('auto_combat must be a boolean')
        if not isinstance(turn, int) or turn < 0:
            raise ValueError('turn must be an int>0')
        if not isinstance(current_unit, LandUnitInBattle) or current_unit is None:
            raise ValueError('current_unit must be a not null pixmap')
        if not isinstance(targetted_unit, LandUnitInBattle) or targetted_unit is None:
            raise ValueError('targetted_unit must be a not null pixmap')
        if not isinstance(map, LandBattleMap) or map is None:
            raise ValueError('map must be a not null LandBattleMap')
        if not isinstance(defender, LandArmy) or defender is None:
            raise ValueError('defender must be a not null LandArmy')
        if not isinstance(attacker, LandArmy) or map is None:
            raise ValueError('attacker must be a not null LandArmy')
        self.autoCombat = auto_combat
        self.turn = turn
        self.currentUnit = current_unit
        self.targettedUnit = targetted_unit
        self.map = map_battle
        self.defender = defender
        self.attacker = attacker

    # Operations
    def draw_current_unit(self, scene, size):
        """function draw_current_unit

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        raise NotImplementedError()

    def draw_targetted_unit(self, scene, size):
        """function draw_targetted_unit

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        raise NotImplementedError()

    def draw_battle_map(self, scene, size):
        """function draw_battle_map

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        raise NotImplementedError()

    def draw_defender(self, scene, size):
        """function draw_defender

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        raise NotImplementedError()

    def draw_attacker(self, scene, size):
        """function draw_attacker

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        raise NotImplementedError()

    def play_turn(self):
        """function play_turn

        returns
        """
        raise NotImplementedError()
