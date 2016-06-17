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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import QGraphicsRectItem

from prototypes.battle.source.nation.nation import Nation
from prototypes.battle.source.unit.landUnitType import LandUnitType


class LandUnit:
    """Class LandUnit
    """

    # Constructor:
    def __init__(self, moral, unit_strength, experience_level, unit_type, nation):
        """function __init__

        :param unit_strength: int range(0,100)
        :param experience_level: int range(1,5)
        :param unit_type: LandUnitType
        :param nation: Nation
        """
        if not isinstance(unit_strength, int) or unit_strength not in range(0, 101):
            raise ValueError('unit_strength must be an int in range(0,100)')
        if not isinstance(experience_level, int) or experience_level not in range(1, 5):
            raise ValueError('experience_level must be an int in range(1,5)')
        if not isinstance(unit_type, LandUnitType) or unit_type is None:
            raise ValueError('unit_type must be a LandUnitType instance and not null')
        if not isinstance(nation, Nation) or nation is None:
            raise ValueError('nation must be a Nation instance and not null')
        if not isinstance(moral, int) or moral not in range(0, 101):
            raise ValueError('moral must be an int in range(0,100)')
        self.unitStrength = unit_strength
        self.experienceLevel = experience_level
        self.unitType = unit_type
        self.nation = nation
        self.moral = moral  # [0, 100]  # (int)

    # Operations
    def increase_experience_level(self):
        """function increase_experience_level

        returns bool
        """
        raise NotImplementedError()

    def draw(self, defending, status, scene, size):
        """function draw

        :param defending: bool
        :param status: str {'Charge', 'Shoot', 'Stand'}
        :param scene: QGraphicsScene
        :param size: QSize

        no return
        """
        if not isinstance(defending, bool):
            raise ValueError('defending must be a boolean')
        if not isinstance(status, str) or (status != 'Charge' and status != 'Shoot' and status != 'Stand'):
            raise ValueError('status must be a str in {\'Charge\', \'Shoot\', \'Stand\'}')

        self.unitType.draw(defending, status, scene, size)
        flag_width = self.nation.flag.width() * 10 / self.nation.flag.height()
        item = scene.addPixmap(self.nation.flag.scaled(flag_width, 10))
        item.setPos(size.width() - 5 - flag_width, 0)
        # life bar
        item1 = QGraphicsRectItem(0, size.height() - 10, size.width() - 5, 5)
        item1.setBrush(QBrush(Qt.white))
        item2 = QGraphicsRectItem(0, size.height() - 10, self.unitStrength / 100 * (size.width() - 5), 5)
        item2.setBrush(QBrush(Qt.green))
        # moral bar
        item3 = QGraphicsRectItem(0, size.height() - 15, size.width() - 5, 5)
        item3.setBrush(QBrush(Qt.white))
        item4 = QGraphicsRectItem(0, size.height() - 15, self.moral / 100 * (size.width() - 5), 5)
        item4.setBrush(QBrush(Qt.blue))
        scene.addItem(item1)
        scene.addItem(item2)
        scene.addItem(item3)
        scene.addItem(item4)

    def __str__(self):
        """function __str__

        returns string
        """
        return "{type} [{exp}/5] of {nation}".format(type=self.unitType, exp=self.experienceLevel, nation=self.nation)
