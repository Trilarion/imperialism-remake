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

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QTransform, QPixmap, QBrush
from PyQt5.QtWidgets import QGraphicsRectItem
def miror_pixmap(pixmap):
    transform = QTransform()
    transform.scale(-1, 1)
    return QPixmap(pixmap.transformed(transform))


class LandUnitType:
    """Class LandUnitType
    """

    # Construtor
    def __init__(self, name, evolution_level, description, officier, attack_strength, fire_range, speed, creation_cost,
                 upkeep, graphic_charge, graphic_shoot, graphic_stand):
        """function __init__

        :param name: str (not empty)
        :param evolution_level: int range(0,3)
        :param description; str (not empty)
        :param officier: bool
        :param attack_strength: int range(0,20)
        :param fire_range: int range(2,8)
        :param speed: int range(2,10)
        :param creation_cost: float > 0
        :param upkeep: float > 0
        :param graphic_charge; QPixmap
        :param graphic_shoot: QPixmap
        :param graphic_stand: QPixmap
        """
        if not isinstance(graphic_charge, QPixmap) or graphic_charge is None or graphic_charge.isNull():
            raise ValueError('graphic_charge must be a QPixmap instance and not null')
        if not isinstance(graphic_shoot, QPixmap) or graphic_shoot is None or graphic_shoot.isNull():
            raise ValueError('graphic_shoot must be a QPixmap instance and not null')
        if not isinstance(graphic_stand, QPixmap) or graphic_stand is None or graphic_stand.isNull():
            raise ValueError('graphic_stand must be a QPixmap instance and not null')
        if not isinstance(name, str) or name == '':
            raise ValueError('name must be a non empty string')
        if not isinstance(evolution_level, int) or evolution_level not in range(1, 4):
            raise ValueError('evolution_level must be an int in  {1,2,3}')
        if not isinstance(description, str) or description == '':
            raise ValueError('description must be a non empty string')
        if not isinstance(officier, bool):
            raise ValueError('officier must be a boolean')
        if not isinstance(attack_strength, int) or attack_strength not in range(0, 21):
            raise ValueError('attack_strength must be an int in range(0,20)')
        if (not isinstance(fire_range, int) or fire_range not in range(2, 9)) and not officier:
            raise ValueError('fire_range must be an int in range(2,8)')
        if not isinstance(speed, int) or speed not in range(2, 11):
            raise ValueError('speed must be an int in range(2,10)')
        if not isinstance(creation_cost, float) or creation_cost < 0:
            raise ValueError('creation_cost must be an float>0 ' + str(creation_cost))
        if not isinstance(upkeep, float) or upkeep < 0:
            raise ValueError('upkeep must be an float>0')
        self.name = name
        self.evolutionLevel = evolution_level
        self.description = description
        self.officier = officier
        self.attackStrength = attack_strength
        self.fireRange = fire_range
        self.speed = speed
        self.creationCost = creation_cost
        self.upkeep = upkeep
        self.graphicCharge = graphic_charge
        self.graphicShoot = graphic_shoot
        self.graphicStand = graphic_stand

    # Operations
    def __str__(self):
        retval = 'name:' + self.name + ',evolutionLevel:' + str(
            self.evolutionLevel) + ',description:' + self.description + ',officier:' + str(
            self.officier) + ',attack: ' + str(self.attackStrength) + ',range:' + str(self.fireRange) + ',speed:' + str(
            self.speed) + ',creationCost:' + str(self.creationCost) + ',upkeep:' + str(self.upkeep)
        return retval

    def to_html_table_row(self):
        """function to_html_table_row

        :return a row table describing the landUnit
        """
        # TODO
        raise NotImplementedError()

    def get_pixmap(self, status):
        if status == 'Charge':
            return self.graphicCharge
        elif status == 'Shoot':
            return self.graphicShoot
        return self.graphicStand

    def draw(self, nation, defending, status, scene, size):
        """function draw

        :param defending: boolean
        :param scene: QGraphicsScene
        :param size: QSize

        no return
        """
        pix =QPixmap('')
        pix.width()


        unit_pixmap = self.get_pixmap(status).scaled(size.width() * 80 / 100, size.height() * 80 / 100)
        if defending:
            unit_pixmap = miror_pixmap(unit_pixmap)
        scene.addPixmap(unit_pixmap)
        flag_width = nation.flag.width() * 10 / nation.flag.height()
        item = scene.addPixmap(nation.flag.scaled(flag_width, 10))
        item.setPos(size.width() - 5 - flag_width, 0)
        item1 = QGraphicsRectItem(0, size.height() - 10, size.width() - 5, 5)
        item1.setBrush(QBrush(Qt.green))
        #item1.setPos(size.width() * 25 / 100, 81 / 100 * size.height())
        scene.addItem(item1)