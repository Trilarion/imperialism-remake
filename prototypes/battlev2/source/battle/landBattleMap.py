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


class LandBattleMap:
    """Class LandBattleMap
    """

    # Constructor:
    def __init__(self, diameter, size_tile, city_diameter, fields):
        """
        function __init__
        :param diameter:int >0
        :param size_tile: float >0
        :param city_diameter:int >0
        :param fields: List<LandBattleField>
        :return:
        """
        if not isinstance(diameter, int) or diameter < 0:
            raise ValueError('diameter must be a int>0')
        if not isinstance(city_diameter, int) or city_diameter < 0:
            raise ValueError('cityDiameter must be a int>0')
        if city_diameter >= diameter:
            raise ValueError('city_diameter must be inferior to diameter')
        try:
            if size_tile < 0:
                raise ValueError('size_tile must be superior to 0')
        except TypeError:
            raise ValueError('size_tile type must be an unorderable type')
        if all(isinstance(f, LandBattleField) for f in fields):
            raise ValueError('fields must be a list of LandBattleField')
        self.diameter = diameter
        self.sizeTile = size_tile
        self.cityDiameter = city_diameter
        self.fields = fields

    # Operations
    def draw(self, scene, size):
        """function draw

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        raise NotImplementedError()

    def resize(self, size):
        """function resize

        :param size: int, int

        returns
        """
        raise NotImplementedError()

    def position_to_grid_position(self, position):
        """function position_to_grid_position

        :param position: int, int

        returns int, int
        """
        raise NotImplementedError()

    def grid_position_to_position(self, gridposition):
        """function grid_position_to_position

        :param gridposition: int, int

        returns int, int
        """
        raise NotImplementedError()

    def map_hexagon(self):
        """function map_hexagon

        returns QHexagon
        """
        raise NotImplementedError()

    def city_hexagon(self):
        """function city_hexagon

        returns QHexagon
        """
        raise NotImplementedError()

    def inside_map_hexagon(self):
        """function inside_map_hexagon

        returns boolean
        """
        raise NotImplementedError()

    def inside_city(self):
        """function inside_city

        returns boolean
        """
        raise NotImplementedError()
