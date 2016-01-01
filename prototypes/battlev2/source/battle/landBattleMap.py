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
from lib.hexagon import QHexagon
from PyQt5.QtCore import QPointF
from battle.landBattleFieldType import LandBattleFieldType
from PyQt5.QtCore import Qt
from base.config import Config
import math

class LandBattleMap:
    ROTATION_FIELD = 30
    ROTATION_CITY_AND_MAP = 0
    DEFAULT_FIELD_TYPE = LandBattleFieldType("default", Qt.green, None)
    DEFAULT_CITY_FIELD_TYPE = LandBattleFieldType("city", Qt.red, None)
    """Class LandBattleMap
    """

    # Constructor:
    def __init__(self, config, size_screen_width, size_screen_heigth):
        """
        function __init__
        :param config: Config
        :param size_screen_width: int
        :param size_screen_heigth: int
        :return:
        """
        if not isinstance(config, Config) and config.error_msg != '':
            raise ValueError('size_screen_width must be a int instance')
        if not isinstance(size_screen_width, int):
            raise ValueError('size_screen_width must be a int instance')
        if not isinstance(size_screen_heigth, int):
            raise ValueError('size_screen_heigth must be a int instance')
        self.config = config
        self.sizeScreenWidth = size_screen_width
        self.sizeScreenHeight = size_screen_heigth
        self.diameter = self.config.diameter_battlemap
        self.cityDiameter = self.config.diameter_battlecity
        self.fields = []
        self.create_fields()
        

    def resizeEvent(self, evt=None):
        print('TODO landBattleMap resize')


    # Operations
    def get_size_tile(self):
        """function get_size_tile

        returns
        """
        return min((self.sizeScreenHeight)/ ( (self.diameter - 1 ) * 3 / 4 + 1), (self.sizeScreenWidth)/ ( (self.diameter - 1 ) * math.sqrt(3) / 2 + 1)) * 0.5


    def get_center_screen(self):
        """function get_center_screen

        returns QPointF
        """
        column = round((self.diameter-1) /2)
        row = round((self.diameter-1) /2)
        posx, posy = LandBattleMap.scene_position(column, row)
        center = QPointF((posx + 0.5) * self.get_size_tile()*2, (posy + 0.5) * self.get_size_tile()*2) 
        return center

    def draw(self, scene):
        """function draw

        :param scene: QGraphicsScene

        no return
        """
        self.sizeScreenWidth = scene.width()
        self.sizeScreenHeight = scene.height()
        self.fields = []
        self.create_fields()
        for field in self.fields:
            field.draw(scene)

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
        return QHexagon(self.get_center_screen(), math.sqrt(3)/2 * self.get_size_tile() * (self.diameter -1),LandBattleMap.ROTATION_CITY_AND_MAP)

    def city_hexagon(self):
        """function city_hexagon

        returns QHexagon
        """
        return QHexagon(self.get_center_screen(),  0.90 * math.sqrt(3)/2 * self.get_size_tile() * (self.cityDiameter - 1),LandBattleMap.ROTATION_CITY_AND_MAP)

    def inside_map_hexagon(self, hexa):
        """function inside_map_hexagon: return true if hexa is inside the main hexagon
        :param hexa; QHexagon
        returns boolean
        """
        if not isinstance(hexa, QHexagon):
            raise ValueError('hexa must be a QHexagon instance')
        if hexa.intersected(self.map_hexagon()):
            return True
        else:
            return False

    def inside_city(self, hexa):
        """function inside_city: return true if hexe is inside the city hexagon
        :param hexa; QHexagon
        returns boolean
        """
        if not isinstance(hexa, QHexagon):
            raise ValueError('hexa must be a QHexagon instance')
        if hexa.intersected(self.city_hexagon()):
            return True
        else:
            return False


    @staticmethod
    def scene_position(column, row):
        """
            Converts a map position to a scene position
            :param column; int
            :param row: int
        """
        return math.sqrt(3) / 2 * (column + ((row + 1) % 2) / 2) , row * 3 / 4


    def create_fields(self):
        """function create_fields: create the fields list

        no return
        """                   
        for column in range(0, self.diameter):
            for row in range(0, self.diameter):
                posx, posy = LandBattleMap.scene_position(column, row)
                center = QPointF((posx + 0.5) * self.get_size_tile()*2, (posy + 0.5) * self.get_size_tile()*2)
                hexa = QHexagon(center, self.get_size_tile(), LandBattleMap.ROTATION_FIELD)
                enable = self.inside_map_hexagon(hexa)
                if self.inside_city(hexa):
                    field_type = LandBattleMap.DEFAULT_CITY_FIELD_TYPE
                else:
                    field_type = LandBattleMap.DEFAULT_FIELD_TYPE
                fields = LandBattleField(enable, hexa.center, column, row, False, field_type, hexa)
                self.fields.append(fields)

