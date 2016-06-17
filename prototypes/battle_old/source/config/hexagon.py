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

import math

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

def hexagonal_grid_offset_to_cube(col, row):
    x = col - (row + (row & 1)) / 2
    z = row
    y = -x - z
    return x, y, z


def distance(col1, row1, col2, row2):
    ax, ay, az = hexagonal_grid_offset_to_cube(col1, row1)
    bx, by, bz = hexagonal_grid_offset_to_cube(col2, row2)
    return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) / 2


def hex_corner(center, size, i, offset):
    """
        Computes
    """

    # check i = 0 1 2 3 4 5
    if (not isinstance(i, int)) or i < 0 or i > 5:
        raise ValueError('i must be a int instance and i must be in range [0,5]')

    angle_deg = 60 * i + offset
    angle_rad = math.pi / 180 * angle_deg
    return QtCore.QPointF(center.x() + size * math.cos(angle_rad),
                   center.y() + size * math.sin(angle_rad))


class QHexagon(QtGui.QPolygonF):
    """
        Hexagon
    """

    def __init__(self, center, size, rotation):
        """function __init__

        :param center: QPointF
        :param size: int>0
        :param rotation; int 0 or 30
        """

        # check center QPointF
        if not isinstance(center, QtCore.QPointF):
            raise ValueError('center must be a QPointF instance')

        # check offset angle 0 or 30
        if not isinstance(rotation, int) or (rotation != 0 and rotation != 30):
            raise ValueError('rotation must be a int instance and rotation must be equal to 0 or 30')

        # check size
        try:
            if size < 0:
                raise ValueError('size must be superior to 0')
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
        return self.size * math.sqrt(3) / 2

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
        if not isinstance(scene, QtWidgets.QGraphicsScene) or scene is None:
            raise ValueError('texture must be a non null QGraphicsScene instance')
        if not isinstance(texture, QtGui.QPixmap) and not texture.isNull():
            raise ValueError('texture must be a QPixmap instance or None')
        if color is None and (texture is None or texture.isNull()):
            raise ValueError('texture or color must be specified')

        tile = scene.addPolygon(self)
        tile.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.black), 1, QtCore.Qt.DotLine))  # dotted tile borders (TODO: ugly)

        if color is not None:
            tile.setBrush(QtGui.QBrush(color))
        if texture is not None and not texture.isNull():
            tile.setBrush(QtGui.QBrush(texture))

    def __eq__(self, other):
        if isinstance(other, QHexagon):
            return (self.size == other.size and
                    self.center.x() == other.center.x() and
                    self.center.y() == other.center.y() and
                    self.rotation == other.rotation)
        else:
            return False
