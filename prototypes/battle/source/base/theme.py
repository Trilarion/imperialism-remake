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

import os

from PyQt5.QtGui import QPixmap


class Theme:
    # constructor
    def __init__(self, name, description, coat_of_arms_graphics, flag_graphics, map_graphics,
                 unit_graphics, background, end_button, autocombat_button, help_button,
                 retreat_button, target_button):
        """constructor
        :param name: str
        :param description: str
        :param coat_of_arms_graphics: str
        :param flag_graphics: str
        :param map_graphics: str
        :param unit_graphics: str
        :param background: str
        :param end_button: str
        :param autocombat_button; str
        :param help_button: str
        :param retreat_button: str
        :param target_button; str
        """
        if not isinstance(name, str) or name == '':
            raise ValueError('name must be a non empty string')
        if not isinstance(description, str) or description == '':
            raise ValueError('description must be a non empty string')
        if not isinstance(coat_of_arms_graphics, str) or coat_of_arms_graphics == '' or not os.path.isdir(
                coat_of_arms_graphics):
            raise ValueError(
                    'coat_of_arms_graphics must be a non empty string, corresponding to the path of a existing directory')
        if not isinstance(flag_graphics, str) or flag_graphics == '' or not os.path.isdir(flag_graphics):
            raise ValueError(
                    'flag_graphics must be a non empty string, corresponding to the path of a existing directory')
        if not isinstance(map_graphics, str) or map_graphics == '' or not os.path.isdir(map_graphics):
            raise ValueError(
                    'map_graphics must be a non empty string, corresponding to the path of a existing directory')
        if not isinstance(unit_graphics, str) or unit_graphics == '' or not os.path.isdir(unit_graphics):
            raise ValueError(
                    'unit_graphics must be a non empty string, corresponding to the path of a existing directory')
        if not isinstance(background, str) or background == '' or not os.path.exists(background):
            raise ValueError('background must be a non empty string, corresponding to the path of a existing file')
        if not isinstance(end_button, str) or end_button == '' or not os.path.exists(end_button):
            raise ValueError('end_button must be a non empty string, corresponding to the path of a existing file')
        if not isinstance(autocombat_button, str) or autocombat_button == '' or not os.path.exists(autocombat_button):
            raise ValueError(
                    'autocombat_button must be a non empty string, corresponding to the path of a existing file')
        if not isinstance(help_button, str) or help_button == '' or not os.path.exists(help_button):
            raise ValueError('help_button must be a non empty string, corresponding to the path of a existing file')
        if not isinstance(retreat_button, str) or retreat_button == '' or not os.path.exists(retreat_button):
            raise ValueError('retreat_button must be a non empty string, corresponding to the path of a existing file')
        if not isinstance(target_button, str) or target_button == '' or not os.path.exists(target_button):
            raise ValueError('target_button must be a non empty string, corresponding to the path of a existing file')
        self.name = name
        self.description = description
        self.coat_of_arms_graphics = coat_of_arms_graphics
        self.flag_graphics = flag_graphics
        self.map_graphics = map_graphics
        self.background = background
        self.unit_graphics = unit_graphics
        self.end_button = end_button
        self.autocombat_button = autocombat_button
        self.help_button = help_button
        self.retreat_button = retreat_button
        self.target_button = target_button

    # Operator
    def __str__(self):
        """
            function __str__
        :return: string describing the theme
        """
        retval = 'name:' + self.name + ',description:' + self.description + ',coat_of_arms_graphics:' + \
                 self.coat_of_arms_graphics + ',flag_graphics:' + self.flag_graphics + ',map_graphics:' + \
                 self.map_graphics + ',unit_graphics:' + self.unit_graphics
        return retval

    def get_unit_pixmap(self, file_name):
        """
        function get_unit_pixmap
        :param file_name: filename of the unit image
        :return: the QPixmap corresponding
        """
        path = (self.unit_graphics + '/' + file_name).replace('//', '/')
        return QPixmap(path)

    def get_map_pixmap(self, file_name):
        """
        function get_map_pixmap
        :param file_name: filename of the map image
        :return: the QPixmap corresponding
        """
        path = (self.map_graphics + '/' + file_name).replace('//', '/')
        return QPixmap(path)

    def get_background_pixmap(self):
        """
        function get_background_pixmap
        :return: the QPixmap corresponding to the background
        """
        return QPixmap(self.background)

    def get_end_button_pixmap(self):
        """
        function get_end_button_pixmap
        :return: the QPixmap corresponding to the end button
        """
        return QPixmap(self.end_button)

    def get_autocombat_button_pixmap(self):
        """
        function get_autocombat_button_pixmap
        :return: the QPixmap corresponding to the autocombat button
        """
        return QPixmap(self.autocombat_button)

    def get_help_button_pixmap(self):
        """
        function get_help_button_pixmap
        :return: the QPixmap corresponding to the help button
        """
        return QPixmap(self.help_button)

    def get_retreat_button_pixmap(self):
        """
        function get_retreat_button_pixmap
        :return: the QPixmap corresponding to the retreat button
        """
        return QPixmap(self.retreat_button)

    def get_target_button_pixmap(self):
        """
        function get_target_button_pixmap
        :return: the QPixmap corresponding to the target button
        """
        return QPixmap(self.target_button)
