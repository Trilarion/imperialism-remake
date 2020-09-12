# Imperialism remake
# Copyright (C) 2020 amtyurin
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

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget

from imperialism_remake.base import constants


def put_pixmap_in_tile_center(scene: QtWidgets.QGraphicsScene, pixmap: QtGui.QPixmap, row: int, column: int, z_value: int) -> None:
    x = (row + 0.5) * constants.TILE_SIZE - pixmap.width() / 2
    y = (column + 0.5) * constants.TILE_SIZE - pixmap.height() / 2
    item = scene.addPixmap(pixmap)
    item.setOffset(x, y)
    item.setZValue(z_value)


def put_widget_in_tile_center(widget: QWidget, row: int, column: int) -> None:
    column, row = scene_position(column, row)
    y = (row + 0.5) * constants.TILE_SIZE - widget.width() / 2
    x = (column + 0.5) * constants.TILE_SIZE - widget.height() / 2

    widget.move(x, y)


def scene_position(column: int, row: int) -> (int, int):
    """
        Converts a map position to a scene position.

        A scene position is the the normalized (by the tile size) position of the upper, left corner of a map tile
        at position (column, row) in the map.

        Our convention for this is that each second row is shifted right (positive) by one half, starting with the
        second. Columns and rows start at zero. To not mix this up with other possible ways all the knowledge about
        the shift of the stagger is in this class in methods scene_position() and map_position().
    """
    return column + (row % 2) / 2, row
