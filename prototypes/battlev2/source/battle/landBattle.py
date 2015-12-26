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

from battle.landArmy import LandArmy
from battle.landBattleMap import LandBattleMap
from battle.landUnitInBattle import LandUnitInBattle


class LandBattle:
    """Class LandBattle
    """

    # Constructor:
    def __init__(self, size_screen_width, size_screen_heigth, diameter, city_diameter, auto_combat, turn, current_unit,
                 targetted_unit, defender,attacker):
        """
        :param size_screen_width: int
        :param size_screen_heigth: int
        :param diameter:int >0
        :param city_diameter:int >0
        :param auto_combat: bool
        :param turn: int > 0
        :param current_unit: LandUnitInBattle
        :param targetted_unit: LandUnitInBattle
        :param defender: LandArmy
        :param attacker: LandArmy
        :return:
        """
        if not isinstance(size_screen_width, int):
            raise ValueError('size_screen_width must be a int instance')
        if not isinstance(size_screen_heigth, int):
            raise ValueError('size_screen_heigth must be a int instance')
        if not isinstance(auto_combat, bool):
            raise ValueError('auto_combat must be a boolean')
        if not isinstance(turn, int) or turn < 0:
            raise ValueError('turn must be an int>0')
        if not isinstance(current_unit, LandUnitInBattle) and current_unit is not None:
            raise ValueError('current_unit must be a not null LandUnitInBattle')
        if not isinstance(targetted_unit, LandUnitInBattle) and targetted_unit is not None:
            raise ValueError('targetted_unit must be a not null LandUnitInBattle')
        if not isinstance(defender, LandArmy) or defender is None:
            raise ValueError('defender must be a not null LandArmy')
        if not isinstance(attacker, LandArmy) or attacker is None:
            raise ValueError('attacker must be a not null LandArmy')
        if not isinstance(diameter, int) or diameter < 0:
            raise ValueError('diameter must be a int>0')
        if not isinstance(city_diameter, int) or city_diameter < 0:
            raise ValueError('cityDiameter must be a int>0')
        if city_diameter >= diameter:
            raise ValueError('city_diameter must be inferior to diameter')
        self.autoCombat = auto_combat
        self.turn = turn
        self.currentUnit = current_unit
        self.targettedUnit = targetted_unit
        self.map = LandBattleMap(size_screen_width, size_screen_heigth, diameter, city_diameter)
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

    def draw_battle_map(self, scene):
        """function draw_battle_map

        :param scene: QGraphicsScene

        returns
        """
        self.map.draw(scene)

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
