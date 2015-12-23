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

class LandArmy:
    """Class LandArmy
    """
    # Attributes:
    retreat = None  # (boolean)

    # Operations
    def list_dead_unit(self):
        """function list_dead_unit

        returns List<LandUnit>
        """
        raise NotImplementedError()
        return None

    def list_alive_unit(self):
        """function list_alive_unit

        returns List<LandUnit>
        """
        raise NotImplementedError()
        return None

    def draw(self, scene, size):
        """function draw

        scene: QGraphicsScene
        size: QSize

        returns
        """
        raise NotImplementedError()
        return None

    def play_turn(self):
        """function play_turn

        returns
        """
        raise NotImplementedError()
        return None
