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


class Nation:
    """Class Nation
    """

    # Constructor:
    def __init__(self, name, computer, coat_of_arms, flag):
        """function __init__

        :param name: str (not empty)
        :param computer: bool
        :param coat_of_arms: QPixmap (not null)
        :param flag: QPixmap (not null)
        """
        if not isinstance(name, str) or name == '':
            raise ValueError('name must be a non empty string')
        if not isinstance(computer, bool):
            raise ValueError('computer must be a boolean')
        if not isinstance(coat_of_arms, QPixmap) or coat_of_arms is None or coat_of_arms.isNull():
            raise ValueError('coatOfArms must be a not null pixmap')
        if not isinstance(flag, QPixmap) or flag is None or flag.isNull():
            raise ValueError('flag must be a not null pixmap')
        self.name = name
        self.computer = computer
        self.coatOfArms = coat_of_arms
        self.flag = flag

    # Operations
    def draw_flag(self, scene, size):
        """function draw_flag

        :param scene: QGraphicsScene
        :param size: QSize

        no return
        """
        raise NotImplementedError()

    def draw_coat_of_arms(self, scene, size):
        """function draw_coat_of_arms

        :param scene: QGraphicsScene
        :param size: QSize

        no return
        """
        raise NotImplementedError()

    def __str__(self):
        return self.name
