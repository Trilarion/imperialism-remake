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

from math import sqrt, pi, cos, sin

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF, QPixmap, QBrush, QPen, QColor
from PyQt5.QtWidgets import QGraphicsScene


def hexgrid_offset_to_cube(col, row):
    x = col - (row + (row & 1)) / 2
    z = row
    y = -x - z
    return x, y, z


def distance(col1, row1, col2, row2):
    ax, ay, az = hexgrid_offset_to_cube(col1, row1)
    bx, by, bz = hexgrid_offset_to_cube(col2, row2)
    return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2


def hex_corner(center, size, i, offset):
    # check center QPointF
    if not isinstance(center, QPointF):
        raise ValueError('center must be a QPointF instance')
    # check i = 0 1 2 3 4 5
    if (not isinstance(i, int)) or i < 0 or i > 5:
        raise ValueError('i must be a int instance and i must be in range [0,5]')
    # check offset angle 0 or 30
    if (not isinstance(offset, int)) or (offset != 0 and offset != 30):
        raise ValueError('offset must be a int instance and offset must be equal to 0 or 30')
        # check size
    try:
        if size < 0:
            raise ValueError('size must be supperior to 0')
    except TypeError:
        raise ValueError('size type must be an unorderable type')
    angle_deg = 60 * i + offset
    angle_rad = pi / 180 * angle_deg
    return QPointF(center.x() + size * cos(angle_rad),
                   center.y() + size * sin(angle_rad))


class QHexagon(QPolygonF):
    """Class QHexagon
    """

    def __init__(self, center, size, rotation):
        """function __init__

        :param center: QPointF
        :param size: int>0
        :param rotation; int 0 or 30
        """
        # check center QPointF
        if not isinstance(center, QPointF):
            raise ValueError('center must be a QPointF instance')
        # check offset angle 0 or 30
        if (not isinstance(rotation, int)) or (rotation != 0 and rotation != 30):
            raise ValueError('rotation must be a int instance and rotation must be equal to 0 or 30')
        # check size
        try:
            if size < 0:
                raise ValueError('size must be supperior to 0')
        except TypeError:
            raise ValueError('size type must be an unorderable type')
        self.center = center
        self.size = size
        self.rotation = rotation
        self.corners = []
        for i in range(0, 6):
            self.corners.append(hex_corner(self.center, self.size, i, self.rotation))
        # init QPolygonF
        super(self.__class__, self).__init__(self.corners)

    # Operations
    def width(self):
        """function width

        returns int
        """
        return self.size * sqrt(3) / 2

    def height(self):
        """function height

        returns int
        """
        return self.size * 3 / 4

    def draw(self, scene, color, texture):
        """function draw

        :param texture: QPixmap
        :param scene: QGraphicsScene
        :param color: QColor
        """
        if not isinstance(scene, QGraphicsScene) or scene is None:
            raise ValueError('texture must be a non null QGraphicsScene instance')
        if not isinstance(texture, QPixmap) and not texture.isNull():
            raise ValueError('texture must be a QPixmap instance or None')
        if color is None and (texture is None or texture.isNull()):
            raise ValueError('texture or color must be specified')
        item = scene.addPolygon(self)
        # hide outline
        item.setPen(QPen(QColor(0xFF, 0xFF, 0xFF, 0x00)))
        if color is not None:
            item.setBrush(QBrush(color))
        if texture is not None and not texture.isNull():
            print('here')
            item.setBrush(QBrush(texture))



    def __eq__(self, other):
        if isinstance(other, QHexagon):
            return (self.size == other.size and
                    self.center.x() == other.center.x() and
                    self.center.y() == other.center.y() and
                    self.rotation == other.rotation)
        else:
            return False
