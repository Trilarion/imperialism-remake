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

from nation.nation import Nation
from unit.landUnitType import LandUnitType


class LandUnit:
    """Class LandUnit
    """

    # Constructor:
    def __init__(self,unit_strength,experience_level,unit_type,nation):
        """function __init__

        :param unit_strength: int range(0,100)
        :param experience_level: int range(1,5)
        :param unit_type: LandUnitType
        :param nation: Nation
        """
        if not isinstance(unit_strength, int) or unit_strength not in range(0,101):
            raise ValueError('unit_strength must be an int in range(0,100)')
        if not isinstance(experience_level, int) or experience_level not in range(1, 5):
            raise ValueError('experience_level must be an int in range(1,5)')
        if not isinstance(unit_type, LandUnitType) or unit_type is None:
            raise ValueError('unit_type must be a LandUnitType instance and not null')
        if not isinstance(nation, Nation) or nation is None:
            raise ValueError('nation must be a Nation instance and not null')
        self.unitStrength = unit_strength
        self.experienceLevel = experience_level
        self.unitType = unit_type
        self.nation = nation

    # Operations
    def increase_experience_level(self):
        """function increase_experience_level

        returns bool
        """
        raise NotImplementedError()

    def draw(self, nation, defending, status, scene, size):
        """function draw

        :param defending: boolean
        :param scene: QGraphicsScene
        :param size: QSize

        no return
        """
        self.unitType.draw(nation, defending, status, scene, size)
