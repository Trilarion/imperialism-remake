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

from battle.landUnitInBattle import LandUnitInBattle


class LandArmy:
    """Class LandArmy
    """
    # Constructor
    def __init__(self, retreat,land_units):
        """function __init__

        :param retreat: bool
        :param land_units: LandUnitInBattle
        """
        if not isinstance(retreat, bool):
            raise ValueError('retreat must be a boolean')
        if not isinstance(land_units, LandUnitInBattle) or land_units is None:
            raise ValueError('land_units must be a not null LandUnitInBattle instance')
        self.retreat = retreat
        self.landUnits = land_units

    # Operations
    def list_dead_unit(self):
        """function list_dead_unit

        returns List<LandUnit>
        """
        raise NotImplementedError()

    def list_alive_unit(self):
        """function list_alive_unit

        returns List<LandUnit>
        """
        raise NotImplementedError()

    def draw(self, scene, size):
        """function draw

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
