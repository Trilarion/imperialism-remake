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

from unit.landUnitType import LandUnitType
from nation.nation import Nation
from PyQt5.QtGui import QPixmap


class LandUnit:
    """Class LandUnit
    """

    # Constructor:
    def __init__(self,unit_strength,experience_level,graphic_charge,graphic_shoot,graphic_stand,unit_type,nation):
        """function __init__

        :param unit_strength: int range(0,100)
        :param experience_level: int range(1,5)
        :param graphic_charge; QPixmap
        :param graphic_shoot: QPixmap
        :param graphic_stand: QPixmap
        :param unit_type: LandUnitType
        :param nation: Nation
        """
        if not isinstance(unit_strength, int) or unit_strength not in range(0,100):
            raise ValueError('unit_strength must be an int in range(0,100)')
        if not isinstance(experience_level, int) or experience_level not in range(1, 5):
            raise ValueError('experience_level must be an int in range(1,5)')

        if not isinstance(graphic_charge, QPixmap) or graphic_charge is None:
            raise ValueError('graphic_charge must be a QPixmap instance and not null')
        if not isinstance(graphic_shoot, QPixmap) or graphic_shoot is None:
            raise ValueError('graphic_shoot must be a QPixmap instance and not null')
        if not isinstance(graphic_stand, QPixmap) or graphic_stand is None:
            raise ValueError('graphic_stand must be a QPixmap instance and not null')
        if not isinstance(unit_type, LandUnitType) or unit_type is None:
            raise ValueError('unit_type must be a LandUnitType instance and not null')
        if not isinstance(nation, Nation) or nation is None:
            raise ValueError('nation must be a Nation instance and not null')
        self.unitStrength = unit_strength
        self.experienceLevel = experience_level
        self.graphicCharge = graphic_charge
        self.graphicShoot = graphic_shoot
        self.graphicStand = graphic_stand
        self.unitType = unit_type
        self.nation = nation

    # Operations
    def increase_experience_level(self):
        """function increase_experience_level

        returns bool
        """
        raise NotImplementedError()

    def draw(self, defending, scene, size):
        """function draw

        :param defending: boolean
        :param scene: QGraphicsScene
        :param size: QSize

        no return
        """
        raise NotImplementedError()
