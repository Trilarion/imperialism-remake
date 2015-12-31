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

import configparser
import os
import sys
from unit.landUnitType import LandUnitType
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from base.theme import Theme

CONFIG_FILE = 'config.ini'
DEFAULT_FULLSCREEN = 'yes'
DEFAULT_THEME = 'theme0'
DEFAULT_LANG = 'en'
DEFAULT_RESOLUTION = 'maximize'

MANDATORY_UNIT_OPTION = ['name', 'description', 'officier', 'level', 'attack', 'range', 'speed', 'creationcost',
                         'upkeep', 'pixmap.charge', 'pixmap.shoot', 'pixmap.stand']
MANDATORY_CONFIG_OPTION = ['fullscreen', 'resolution', 'theme', 'lang']
MANDATORY_PATH_OPTION = ['data', 'lang_config_file', 'unit_config_file']
MANDATORY_BATTLE_OPTION = []
MANDATORY_THEME_OPTION = ['name', 'description', 'coat_of_arms_graphics', 'flag_graphics', 'map_graphics',
                          'ui_graphics', 'unit_graphics']


class Config:
    def __init__(self):
        self.error_msg = ''
        self.data_folder = 'error'
        self.config = configparser.ConfigParser()
        self.config.read_file(open(CONFIG_FILE))
        self.check_options('config', MANDATORY_CONFIG_OPTION, CONFIG_FILE)
        self.check_options('path', MANDATORY_PATH_OPTION, CONFIG_FILE)
        self.check_options('battle', MANDATORY_BATTLE_OPTION, CONFIG_FILE)

        #
        # Config Option
        #

        # fullscreen option
        self.fullscreen = self.get_config('config', 'fullscreen', DEFAULT_FULLSCREEN, ['yes', 'no'])
        # resolution
        # TODO get list supported  resolution...
        self.resolution = self.get_config('config', 'resolution', DEFAULT_RESOLUTION, ['maximize'])
        # theme
        self.name_theme_selected = self.get_config('config', 'theme', DEFAULT_THEME, [])
        # lang
        self.lang_selected = self.get_config('config', 'lang', DEFAULT_LANG, [])

        #
        # Path config
        #

        # path file
        self.data_folder = self.get_config('path', 'data', '', [])
        # TODO remove / at the end of data path
        if not os.path.isdir(self.data_folder):
            self.error_msg += 'data folder ' + self.data_folder + ' doesn\'t exist\n'
            self.data_folder = 'error'
        # lang config file
        self.lang_config_file = self.get_config('path', 'lang_config_file', '', [])
        if not os.path.exists(self.lang_config_file):
            self.error_msg += 'lang config file ' + self.lang_config_file + ' doesn\'t exist\n'
            self.lang_config_file = 'error'
        # unit config file
        self.unit_config_file = self.get_config('path', 'unit_config_file', '', [])
        if not os.path.exists(self.unit_config_file):
            self.error_msg += 'unit config file ' + self.unit_config_file + ' doesn\'t exist\n'
            self.unit_config_file = 'error'

        #
        # Theme Config
        #
        self.unit_data_folder = 'error'
        self.available_theme = []
        self.theme_selected = None
        for section in self.config.sections():
            if section.startswith('theme'):
                if self.check_options(section, MANDATORY_THEME_OPTION, CONFIG_FILE):
                    name = self.get_config(section, 'name', '', [])
                    description = self.get_config(section, 'description', '', [])
                    coat_of_arms_graphics = self.get_config(section, 'coat_of_arms_graphics', '', [])
                    flag_graphics = self.get_config(section, 'flag_graphics', '', [])
                    map_graphics = self.get_config(section, 'map_graphics', '', [])
                    ui_graphics = self.get_config(section, 'ui_graphics', '', [])
                    unit_graphics = self.get_config(section, 'unit_graphics', '', [])
                    try:
                        theme = Theme(name, description, coat_of_arms_graphics, flag_graphics, map_graphics,
                                      ui_graphics,
                                      unit_graphics)
                        self.available_theme.append(theme)

                        if name == self.name_theme_selected:
                            self.theme_selected = theme
                    except ValueError as e:
                        self.error_msg += str(e) + '\n'
        if self.theme_selected is None:
            self.error_msg = 'Theme: ' + str(self.name_theme_selected) + ' not found\n'
        #
        # Unit config
        #
        self.list_unit_type = []
        print('here ' + self.unit_config_file + ' ' + str(self.theme_selected))
        if self.unit_config_file != 'error' and self.theme_selected is not None:

            self.config = configparser.ConfigParser()
            self.config.read_file(open(self.unit_config_file))
            for section in self.config.sections():
                if self.check_options(section, MANDATORY_UNIT_OPTION, self.unit_config_file):
                    try:
                        previous_error = self.error_msg
                        name = self.get_config(section, 'name', '', [])
                        evolution_level = int(self.get_config(section, 'level', '', []))
                        description = self.get_config(section, 'description', '', [])
                        officier = bool(self.get_config(section, 'officier', '', []))
                        attack_strength = int(self.get_config(section, 'attack', '', []))
                        fire_range = int(self.get_config(section, 'range', '', []))
                        speed = int(self.get_config(section, 'speed', '', []))
                        creation_cost = float(self.get_config(section, 'creationcost', '', []))
                        upkeep = float(self.get_config(section, 'upkeep', '', []))
                        graphic_charge = QPixmap(
                            self.theme_selected.unit_graphics + '/' + self.get_config(section, 'pixmap.charge', '',
                                                                                          []))
                        graphic_shoot = QPixmap(
                                self.theme_selected.unit_graphics + '/' + self.get_config(section, 'pixmap.shoot', '',
                                                                                          []))
                        graphic_stand = QPixmap(
                                self.theme_selected.unit_graphics + '/' + self.get_config(section, 'pixmap.stand', '',
                                                                                          []))
                        section = LandUnitType(name, evolution_level, description, officier, attack_strength,
                                               fire_range, speed, creation_cost, upkeep, graphic_charge,
                                               graphic_shoot, graphic_stand)
                        if previous_error == self.error_msg:
                            self.list_unit_type.append(section)
                    except ValueError as e:
                        self.error_msg += str(e) + '\n'



                        #    if section.startswith('theme'):
                        #        list_themes.append(section)
                        # TODO
                        # list_themes.size == 0 => error
                        # list_themes.size == 1 => DEFAULT_THEME = elem
                        # list_themes.size and DEFAULT_THEME not in => DEFAULT_THEME.elem 0
                        # self.theme = self.get_config('config', 'theme', DEFAULT_THEME, list_themes)
                        # if self.error_msg != '':
                        #    raise Exception('')

    def check_options(self, section, list_option, filename):
        retval = True
        for option in list_option:
            if not self.config.has_option(section, option):
                retval = False
                self.error_msg += 'In config file:' + str(
                        filename) + ' missing option ' + option + ' in section ' + section + '\n'
        for option in self.config.options(section):
            if option not in list_option:
                retval = False
                self.error_msg += 'In config file:' + str(
                        filename) + ' unknown option ' + option + ' in section ' + section + '\n'
        return retval

    def fullscreen(self):
        return self.fullscreen.lower() == 'yes'

    def maximize(self):
        return self.resolution.lower() == 'maximize'

    def get_unit_type_list(self):
        return self.list_unit_type

    def parsing_error(self):
        return self.error_msg == ''

    def get_error_msg(self):
        return self.error_msg

    def get_config(self, section, option, default, expected_value):
        try:
            retval = self.config.get(section, option)
            if len(expected_value) != 0 and retval.lower() not in expected_value:
                self.error_msg += 'Error : Bad value option ' + str(option) + ' expected ' + str(expected_value) + '\n'
            else:
                if self.data_folder != 'error':
                    retval = retval.replace('$data', self.data_folder)
                return retval
        except configparser.NoOptionError:
            self.error_msg += 'Error : Missing mandatory option ' + str(option) + '\n'

        except configparser.NoSectionError:
            self.error_msg += 'Error : Missing mandatory section ' + str(section) + '\n'
        return default

    def __str__(self):
        retval = 'Error : \n'
        retval += str(self.error_msg)
        retval += 'Config : \n'
        retval += 'Resolution:' + str(self.resolution) + '\n'
        retval += 'data folder:' + str(self.data_folder) + '\n'
        retval += 'lang config file:' + str(self.lang_config_file) + '\n'
        retval += 'unit config file:' + str(self.unit_config_file) + '\n'
        retval += 'unit type:\n'
        for utype in self.list_unit_type:
            retval += '\t-' + str(utype) + '\n'
        retval += 'theme:\n'
        for theme in self.available_theme:
            retval += '\t-' + str(theme) + '\n'

        return retval


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = Config()
    print(config)
