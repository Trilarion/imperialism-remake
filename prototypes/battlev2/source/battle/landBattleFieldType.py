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

from PyQt5.QtGui import QPixmap


class LandBattleFieldType:
    """Class LandBattleFieldType
    """

    def __init__(self, name, color, texture):
        if not isinstance(name, str) or name == '':
            raise ValueError('name must be a non empty string')
        if not isinstance(texture, QPixmap) and texture is not None:
            raise ValueError('texture must be a QPixmap instance or None')
        if color is None and texture is None:
            raise ValueError('texture or color must be specified')
        self.name = name
        self.color = color
        self.texture = texture






