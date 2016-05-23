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


from PyQt5.QtGui import QTransform, QPixmap


def miror_pixmap(pixmap):
    transform = QTransform()
    transform.scale(-1, 1)
    return QPixmap(pixmap.transformed(transform))


UNIT_WIDTH = 400
UNIT_HEIGHT = 400


class LandUnitType:
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
        if graphic_charge.width() != UNIT_WIDTH or graphic_charge.height() != UNIT_HEIGHT:
            raise ValueError('graphic_charge must have the dimension ' + str(UNIT_WIDTH) + 'x' + str(UNIT_HEIGHT))
        if graphic_shoot.width() != UNIT_WIDTH or graphic_shoot.height() != UNIT_HEIGHT:
            raise ValueError('graphic_shoot must have the dimension ' + str(UNIT_WIDTH) + 'x' + str(UNIT_HEIGHT))
        if graphic_stand.width() != UNIT_WIDTH or graphic_stand.height() != UNIT_HEIGHT:
            raise ValueError('graphic_stand must have the dimension ' + str(UNIT_WIDTH) + 'x' + str(UNIT_HEIGHT))
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
        return self.name

    def __repr__(self):
        # TODO - blurgh!
        return 'Name: %s\n\tEvolution level: %d\n\tDescription: %s\n\tOfficer: %r\n\t' \
               'Attacks: %d\n\tSpeed: %d\n\tRange: %d\n\tCreation Cost: %f\n\tUpkeep: %d\n' \
               % (self.name, self.evolutionLevel, self.description, self.officier, self.attackStrength,
                  self.speed, self.fireRange, self.creationCost, self.upkeep)

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

    def draw(self, defending, status, scene, size):
        """function draw

        :param defending: boolean
        :param status: str {'Charge', 'Shoot', 'Stand'}
        :param scene: QGraphicsScene
        :param size: QSize

        no return
        """
        pix = QPixmap('')
        pix.width()

        unit_pixmap = self.get_pixmap(status).scaled(size.width() * 80 / 100, size.height() * 80 / 100)
        if defending:
            unit_pixmap = miror_pixmap(unit_pixmap)
        scene.addPixmap(unit_pixmap)
