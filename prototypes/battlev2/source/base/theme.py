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


class Theme:
    def __init__(self, name, description, coat_of_arms_graphics, flag_graphics, map_graphics, ui_graphics,
                 unit_graphics):
        # TODO check input
        # TODO remove / at the end of the path
        self.name = name
        self.description = description
        self.coat_of_arms_graphics = coat_of_arms_graphics
        self.flag_graphics = flag_graphics
        self.map_graphics = map_graphics
        self.ui_graphics = ui_graphics
        self.unit_graphics = unit_graphics
        # TODO check ressource in each folder...


    def __str__(self):
        retval = 'name:' + self.name + ',description:' + self.description + ',coat_of_arms_graphics:' + \
                 self.coat_of_arms_graphics + ',flag_graphics:' + self.flag_graphics + ',map_graphics:' + \
                 self.map_graphics + ',ui_graphics:' + self.ui_graphics + ',unit_graphics:' + self.unit_graphics
        return retval
