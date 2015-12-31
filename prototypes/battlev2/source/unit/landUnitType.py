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


class LandUnitType:
    """Class LandUnitType
    """




    # Construtor
    def __init__(self,ini_file,section):
        """function __init__

        :param ini_file:str path to ini file
        :param section; section of the ini file
        :return:
        """
        # TODO

    def __init__(self, name, evolution_level, description, officier, attack_strength, fire_range, speed, creation_cost,
                 upkeep):
        """function __init__

        :param name: str (not empty)
        :param evolution_level: int range(0,3)
        :param description; str (not empty)
        :param officier: bool
        :param attack_strength: int range(0,20)
        :param fire_range: int range(2,8)
        :param speed: int range(2,10)
        :param creation_cost: int > 0
        """
        if not isinstance(name, str) or name == '':
            raise ValueError('name must be a non empty string')
        if not isinstance(evolution_level, int) or evolution_level not in range(0, 3):
            raise ValueError('evolution_level must be an int in range(0,3)')
        if not isinstance(description, str) or description == '':
            raise ValueError('description must be a non empty string')
        if not isinstance(officier, bool):
            raise ValueError('officier must be a boolean')
        if not isinstance(attack_strength, int) or attack_strength not in range(0, 20):
            raise ValueError('attack_strength must be an int in range(0,20)')
        if not isinstance(fire_range, int) or fire_range not in range(2, 8):
            raise ValueError('fire_range must be an int in range(2,8)')
        if not isinstance(speed, int) or speed not in range(2, 10):
            raise ValueError('speed must be an int in range(2,10)')
        if not isinstance(creation_cost, int) or creation_cost < 0:
            raise ValueError('creation_cost must be an int>0')
        if not isinstance(upkeep, int) or upkeep < 0:
            raise ValueError('upkeep must be an int>0')
        self.name = name
        self.evolutionLevel = evolution_level
        self.description = description
        self.officier = officier
        self.attackStrength = attack_strength
        self.fireRange = fire_range
        self.speed = speed
        self.creationCost = creation_cost
        self.upkeep = upkeep
