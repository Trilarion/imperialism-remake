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

from prototypes.battle.source.battle.landArmy import LandArmy
from prototypes.battle.source.battle.landBattleMap import LandBattleMap
from prototypes.battle.source.battle.landUnitInBattle import LandUnitInBattle
from prototypes.battle.source.config.config import Config


class LandBattle:
    """Class LandBattle
    """

    # Constructor:
    def __init__(self, config, auto_combat, turn, current_unit,
                 targetted_unit, defender, attacker):
        """
        constructor
        :param config: Config
        :param auto_combat: bool
        :param turn: int > 0
        :param current_unit: LandUnitInBattle
        :param targetted_unit: LandUnitInBattle
        :param defender: LandArmy
        :param attacker: LandArmy
        :return:
        """
        if not isinstance(config, Config) and config.error_msg != '':
            raise ValueError('size_screen_width must be a int instance')
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
        self.autoCombat = auto_combat
        self.turn = turn
        self.currentUnit = current_unit
        self.targettedUnit = targetted_unit
        self.config = config
        self.map = LandBattleMap(self.config)
        self.defender = defender
        self.attacker = attacker

    # Operations
    def draw_current_unit(self, defending, scene, size):
        """function draw_current_unit

        :param defending: bool
        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        if self.currentUnit is not None:
            self.currentUnit.draw(defending, self.currentUnit.status, scene, size)

    def draw_targetted_unit(self, defending, scene, size):
        """function draw_targetted_unit

        :param defending: bool
        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        if self.targettedUnit is not None:
            self.targettedUnit.draw(defending, self.targettedUnit.status, scene, size)

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

    def draw_coat_of_arms(self, scene, size):
        """function draw_coat_of_arms

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        for army in self.attacker, self.defender:
            if army is not None and not army.nation.computer:
                army.nation.draw_coat_of_arms(scene, size)
                return

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
