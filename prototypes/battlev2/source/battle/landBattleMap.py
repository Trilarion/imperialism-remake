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

from lib.hexagon import QHexagon


class LandBattleMap:
    """Class LandBattleMap
    """
    # Attributes:
    diameter = None  # (int)
    sizeTile = None  # (int)
    cityDiameter = None  # (int)

    # Operations
    def draw(self, scene, size):
        """function draw

        scene: QGraphicsScene
        size: QSize

        returns
        """
        raise NotImplementedError()
        return None

    def resize(self, size):
        """function resize

        size: int, int

        returns
        """
        raise NotImplementedError()
        return None

    def position_to_grid_position(self, position):
        """function position_to_grid_position

        position: int, int

        returns int, int
        """
        raise NotImplementedError()
        return None

    def grid_position_to_position(self, gridposition):
        """function grid_position_to_position

        gridposition: int, int

        returns int, int
        """
        raise NotImplementedError()
        return None

    def map_hexagon(self):
        """function map_hexagon

        returns QHexagon
        """
        raise NotImplementedError()
        return None

    def city_hexagon(self):
        """function city_hexagon

        returns QHexagon
        """
        raise NotImplementedError()
        return None

    def inside_map_hexagon(self):
        """function inside_map_hexagon

        returns boolean
        """
        raise NotImplementedError()
        return None

    def inside_city(self):
        """function inside_city

        returns boolean
        """
        raise NotImplementedError()
        return None
