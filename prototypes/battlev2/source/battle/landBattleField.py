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
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSimpleTextItem
from PyQt5.QtGui import QBrush

class LandBattleField:
    """Class LandBattleField
    """

    # Constructor:
    def __init__(self, enable,position, sx, sy, occupied, field_type, hexa):
        """
        function __init__
        :param : QPointF
        :param sx: int
        :param sy: int
        :param occupied: bool
        :param field_type:LandBattleFieldType
        :param hexa: QHexagon
        :param enable: bool
        :return:
        """
        if not isinstance(enable, bool):
            raise ValueError('enable must be a boolean')
        if not isinstance(sx,int) or sx<0:
            raise ValueError('sx must be a int>0')
        if not isinstance(sy,int) or sy<0:
            raise ValueError('sy must be a int>0')
        if not isinstance(occupied, bool):
            raise ValueError('occupied must be a boolean')
        if not isinstance(position, QPointF) or position is None:
            raise ValueError('position must be a not null QPointF')
        if not isinstance(field_type, LandBattleFieldType) or field_type is None:
            raise ValueError('field_type must be a not null LandBattleFieldType')
        if not isinstance(hexa, QHexagon) or hexa is None:
            raise ValueError('hexa must be a not null QHexagon')
        self.position = position
        self.sx = sx
        self.sy = sy
        self.occupied = occupied
        self.fieldType = field_type
        self.hexa = hexa
        self.enable = enable

    # Operations
    def draw(self, scene):
        """function draw

        :param scene: QGraphicsScene

        no return
        """
        if self.enable:
            self.hexa.draw(scene,self.fieldType.color,self.fieldType.texture)
            text = '({},{})'.format(self.sx, self.sy)
            item = QGraphicsSimpleTextItem(text)
            item.setBrush(QBrush(Qt.black))
            item.setPos(self.position.x() - self.hexa.size,self.position.y() - self.hexa.size/2)
            item.setZValue(1001)
            scene.addItem(item)


    def distance(self, field):
        """function distance

        :param field: LandBattleField

        returns int
        """
        raise NotImplementedError()
