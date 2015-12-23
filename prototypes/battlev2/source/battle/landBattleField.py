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
from battle.landBattleFieldType import LandBattleFieldType
from PyQt5.QtCore import QPointF


class LandBattleField:
    """Class LandBattleField
    """

    # Constructor:
    def __init__(self, position, grid_position, occupied, field_type, hexa):
        """
        function __init__
        :param position: QPointF
        :param grid_position: (int, int)
        :param occupied: bool
        :param field_type:LandBattleFieldType
        :param hexa: QHexagon
        :return:
        """
        if not isinstance(grid_position, (int, int)) or grid_position is None:
            raise ValueError('grid_position must be a (int,int)')
        if not isinstance(occupied, bool):
            raise ValueError('occupied must be a boolean')
        if not isinstance(position, QPointF) or position is None:
            raise ValueError('position must be a not null QPointF')
        if not isinstance(field_type, LandBattleFieldType) or field_type is None:
            raise ValueError('field_type must be a not null LandBattleFieldType')
        if not isinstance(hexa, QHexagon) or hexa is None:
            raise ValueError('hexa must be a not null QHexagon')
        self.position = position
        self.gridPosition = grid_position  # (int, int)
        self.occupied = occupied  # (boolean)
        self.fieldType = field_type
        self.hexa = hexa

    # Operations
    def draw(self, scene, size):
        """function draw

        :param scene: QGraphicsScene
        :param size: QSize

        returns
        """
        raise NotImplementedError()

    def distance(self, field):
        """function distance

        :param field: LandBattleField

        returns int
        """
        raise NotImplementedError()
