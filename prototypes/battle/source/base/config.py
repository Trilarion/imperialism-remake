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
import re
import logging

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from base.lang import Lang
from base.theme import Theme
from nation.nation import Nation
from unit.landUnitType import LandUnitType

DEFAULT_FULLSCREEN = 'yes'
DEFAULT_THEME = 'theme0'
DEFAULT_LANG = 'en'
DEFAULT_RESOLUTION = 'maximize'
MINIMUM_RESOLUTION = 800, 600
DEFAULT_DIAMETER_MAP = '20'
DEFAULT_DIAMETER_CITY = '5'
DEFAULT_LOGLEVEL ='50'
LOG_FILENAME ='game.log'

MANDATORY_UNIT_OPTION = ['name', 'description', 'officier', 'level', 'attack', 'range', 'speed', 'creationcost',
                         'upkeep', 'pixmap.charge', 'pixmap.shoot', 'pixmap.stand']
MANDATORY_CONFIG_OPTION = ['fullscreen', 'resolution', 'theme', 'lang', 'log_level']
MANDATORY_PATH_OPTION = ['data', 'lang_config_file', 'unit_config_file', 'nation_config_file']
MANDATORY_BATTLE_OPTION = ['diameter_battlemap', 'diameter_battlecity']
MANDATORY_THEME_OPTION = ['name', 'description', 'coat_of_arms_graphics', 'flag_graphics', 'map_graphics',
                          'unit_graphics', 'background', 'end_button', 'autocombat_button', 'help_button',
                          'retreat_button', 'target_button', 'outside_city_pixmap', 'outside_city_color',
                          'city_pixmap', 'city_color']
MANDATORY_NATION_OPTION = ['name', 'flag', 'coat_of_arms']


class Config:
    def get_resolution_qsize(self):
        logging.debug('[ENTER] get_resolution_qsize()')
        w, h = self.get_resolution()
        logging.debug('[EXIT] get_resolution_qsize() => return ' + str(w) + ',' + str(h))
        return QSize(w, h)

    @staticmethod
    def get_min_resolution_qsize():
        logging.debug('[ENTER] get_min_resolution_qsize()')
        w, h = MINIMUM_RESOLUTION
        logging.debug('[EXIT] get_min_resolution_qsize() => return ' + str(w) + ',' + str(h))
        return QSize(w, h)

    def get_resolution(self):
        logging.debug('[ENTER] get_resolution()')
        try:
            m = re.search('^(\d+)\s*x\s*(\d+)$', self.resolution.lower())
            w, h = int(m.group(1)), int(m.group(2))
            logging.debug('[EXIT] get_resolution() => return ' + str(w) + ',' + str(h))
            return w, h
        except AttributeError:
            logging.debug('[EXIT] get_resolution() => return -1,-1')
            return -1, -1

    def __init__(self, main_config_file):
        self.error_msg = ''
        self.data_folder = 'error'
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.config.read_file(open(main_config_file))
        self.check_options('config', MANDATORY_CONFIG_OPTION, main_config_file)
        self.check_options('path', MANDATORY_PATH_OPTION, main_config_file)
        self.check_options('battle', MANDATORY_BATTLE_OPTION, main_config_file)

        #
        # Config Option
        #

        # fullscreen option
        self.fullscreen = self.get_config('config', 'fullscreen', DEFAULT_FULLSCREEN, ['yes', 'no'])
        # log level option
        log_level = int(self.get_config('config', 'log_level', DEFAULT_LOGLEVEL, ['50', '40', '30', '20', '10']))
        logging.basicConfig(level=log_level, filename=LOG_FILENAME, filemode='w', format='%(asctime)s %(module)s:%(filename)s:%(funcName)s:%(lineno)d   %(levelname)s:%(message)s')
        # resolution
        # TODO get list supported  resolution...
        self.resolution = self.get_config('config', 'resolution')
        if 'maximize' and re.match('^(\d+)\s*x\s*(\d+)$|^maximize$', self.resolution.lower()):
            self.resolution = self.resolution.lower()
            w, h = self.get_resolution()
            if w != -1 and h != -1:
                minw, minh = MINIMUM_RESOLUTION
                screen = QDesktopWidget().screenGeometry()
                if w < minw or h < minh:
                    self.error_msg = 'Error : Bad resolution (width must be superior to ' + str(
                        minw) + ' and height must be superior to ' + str(minh) + ')'
                if w > screen.width() or h > screen.height():
                    self.error_msg = 'Error : Bad resolution (width must be inferior to screen width resolution ' + str(
                        screen.width()) + ' and height must be inferior to screen height resolution ' + str(
                        screen.height()) + ')'
        else:
            self.error_msg = 'Error : Bad value option resolution (format maxize or 800 x 600)'
        # theme
        self.name_theme_selected = self.get_config('config', 'theme', DEFAULT_THEME)
        # lang
        self.name_lang_selected = self.get_config('config', 'lang', DEFAULT_LANG)

        #
        # Battle option
        #
        try:
            self.diameter_battlemap = int(self.get_config('battle', 'diameter_battlemap', DEFAULT_DIAMETER_MAP))
            if self.diameter_battlemap <= 0:
                self.error_msg += 'diameter_battlemap must be a int>0'
            if self.diameter_battlemap % 2 == 0:
                self.error_msg += 'diameter_battlemap must be a odd number'
        except ValueError:
            self.error_msg += 'diameter_battlemap must be a int'
        try:
            self.diameter_battlecity = int(self.get_config('battle', 'diameter_battlecity', DEFAULT_DIAMETER_CITY))
            if self.diameter_battlecity <= 0:
                self.error_msg += 'diameter_battlecity must be a int>0'
            if self.diameter_battlecity % 2 == 0:
                self.error_msg += 'diameter_battlecity must be a odd number'
        except ValueError:
            self.error_msg += 'diameter_battlecity must be a int'
        #
        # Path config
        #

        # data path folder
        self.data_folder = self.get_config('path', 'data')
        if not os.path.isdir(self.data_folder):
            self.error_msg += 'data folder ' + self.data_folder + ' doesn\'t exist\n'
            self.data_folder = 'error'
        # lang config file
        self.lang_config_file = self.get_config('path', 'lang_config_file')
        if not os.path.exists(self.lang_config_file):
            self.error_msg += 'lang config file ' + self.lang_config_file + ' doesn\'t exist\n'
            self.lang_config_file = 'error'
        # unit config file
        self.unit_config_file = self.get_config('path', 'unit_config_file')
        if not os.path.exists(self.unit_config_file):
            self.error_msg += 'unit config file ' + self.unit_config_file + ' doesn\'t exist\n'
            self.unit_config_file = 'error'
        # nation config file
        self.nation_config_file = self.get_config('path', 'nation_config_file')
        if not os.path.exists(self.nation_config_file):
            self.error_msg += 'nation config file ' + self.nation_config_file + ' doesn\'t exist\n'
            self.nation_config_file = 'error'
        #
        # Theme Config
        #
        self.unit_data_folder = 'error'
        self.available_theme = []
        self.theme_selected = None
        for section in self.config.sections():
            if section.startswith('theme'):
                if self.check_options(section, MANDATORY_THEME_OPTION, main_config_file):
                    name = self.get_config(section, 'name')
                    description = self.get_config(section, 'description')
                    coat_of_arms_graphics = self.get_config(section, 'coat_of_arms_graphics')
                    flag_graphics = self.get_config(section, 'flag_graphics')
                    map_graphics = self.get_config(section, 'map_graphics')
                    unit_graphics = self.get_config(section, 'unit_graphics')
                    background = self.get_config(section, 'background')
                    end_button = self.get_config(section, 'end_button')
                    autocombat_button = self.get_config(section, 'autocombat_button')
                    help_button = self.get_config(section, 'help_button')
                    retreat_button = self.get_config(section, 'retreat_button')
                    target_button = self.get_config(section, 'target_button')
                    outside_city_pixmap= self.get_config(section, 'outside_city_pixmap')
                    outside_city_color= self.get_config(section, 'outside_city_color')
                    city_pixmap= self.get_config(section, 'city_pixmap')
                    city_color= self.get_config(section, 'city_color')
                    try:
                        theme = Theme(name, description, coat_of_arms_graphics, flag_graphics, map_graphics,
                                      unit_graphics, background, end_button, autocombat_button, help_button,
                                      retreat_button, target_button, outside_city_pixmap, outside_city_color,
                                      city_pixmap, city_color)
                        self.available_theme.append(theme)

                        if name == self.name_theme_selected:
                            self.theme_selected = theme
                    except ValueError as e:
                        self.error_msg += str(e) + '\n'
        if self.theme_selected is None:
            self.error_msg += 'Theme: ' + str(self.name_theme_selected) + ' not found\n'
        if len(self.available_theme) == 0:
            self.error_msg += 'No Theme available\n'
        #
        # Unit config
        #
        self.list_unit_type = []
        if self.unit_config_file != 'error':

            self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            self.config.read_file(open(self.unit_config_file))
            for section in self.config.sections():
                if self.check_options(section, MANDATORY_UNIT_OPTION, self.unit_config_file):
                    try:
                        previous_error = self.error_msg
                        name = self.get_config(section, 'name')
                        evolution_level = int(self.get_config(section, 'level'))
                        description = self.get_config(section, 'description')
                        officier = bool(self.get_config(section, 'officier'))
                        attack_strength = int(self.get_config(section, 'attack'))
                        fire_range = int(self.get_config(section, 'range'))
                        speed = int(self.get_config(section, 'speed'))
                        creation_cost = float(self.get_config(section, 'creationcost'))
                        upkeep = float(self.get_config(section, 'upkeep'))
                        graphic_charge_filename = self.get_config(section, 'pixmap.charge')
                        if not graphic_charge_filename.lower().endswith('.png'):
                            raise ValueError('pixmap.charge must be a png file')
                        graphic_charge = QPixmap(self.theme_selected.unit_graphics + '/' + graphic_charge_filename)
                        graphic_shoot_filename = self.get_config(section, 'pixmap.shoot')
                        if not graphic_shoot_filename.lower().endswith('.png'):
                            raise ValueError('pixmap.shoot must be a png file')
                        graphic_shoot = QPixmap(self.theme_selected.unit_graphics + '/' + graphic_shoot_filename)
                        graphic_stand_filename = self.get_config(section, 'pixmap.stand')
                        if not graphic_stand_filename.lower().endswith('.png'):
                            raise ValueError('pixmap.stand must be a png file')
                        graphic_stand = QPixmap(self.theme_selected.unit_graphics + '/' + graphic_stand_filename)
                        unit_type = LandUnitType(name, evolution_level, description, officier, attack_strength,
                                                 fire_range, speed, creation_cost, upkeep, graphic_charge,
                                                 graphic_shoot, graphic_stand)
                        if previous_error == self.error_msg:
                            self.list_unit_type.append(unit_type)
                    except AttributeError as e:
                        self.error_msg += str(e) + '\n'
                    except ValueError as e:
                        self.error_msg += str(e) + '\n'
        #
        # lang config
        #
        self.lang_selected = 'error'
        self.available_lang = []
        if self.lang_config_file != 'error':
            self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation()
                                                    )
            self.config.read_file(open(self.lang_config_file))
            for section in self.config.sections():
                try:
                    name = self.get_config(section, 'name')
                    description = self.get_config(section, 'description')
                    lang = Lang(name, description)
                    for option in self.config.options(section):
                        lang.add_string(option, self.get_config(section, option))
                    if name == self.name_lang_selected:
                        self.lang_selected = lang
                    self.available_lang.append(lang)
                except ValueError as e:
                    self.error_msg += str(e) + '\n'
        if self.lang_selected is None:
            self.error_msg += 'Lang: ' + str(self.lang_selected) + ' not found\n'
        if len(self.available_lang) == 0:
            self.error_msg += 'No Lang available\n'

        #
        # nation config
        #
        self.available_nation = []
        if self.nation_config_file != 'error':
            self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
            self.config.read_file(open(self.nation_config_file))
            for section in self.config.sections():
                try:
                    name = self.get_config(section, 'name')
                    flag_filename = self.get_config(section, 'flag')
                    if not flag_filename.lower().endswith('.png'):
                        raise ValueError('flag must be a png file')
                    flag = QPixmap(self.theme_selected.flag_graphics + '/' + flag_filename)
                    coat_of_arms_filename = self.get_config(section, 'coat_of_arms')
                    if not coat_of_arms_filename.lower().endswith('.png'):
                        raise ValueError('coat of arms must be a png file')
                    coat_of_arms = QPixmap(self.theme_selected.coat_of_arms_graphics + '/' + coat_of_arms_filename)

                    nation = Nation(name, False, coat_of_arms, flag)
                    for option in self.config.options(section):
                        lang.add_string(option, self.get_config(section, option))
                    if name == self.name_lang_selected:
                        self.lang_seleted = lang
                    self.available_nation.append(nation)
                except AttributeError as e:
                    self.error_msg += str(e) + '\n'
                except ValueError as e:
                    self.error_msg += str(e) + '\n'
        if len(self.available_nation) == 0:
            self.error_msg += 'No Nation available\n'

    #
    # Overwrite class method
    #
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
        retval += 'nation:\n'
        for nation in self.available_nation:
            retval += '\t-' + str(nation) + '\n'
        return retval

    #
    # Operation to simplify config parsing
    #
    def get_config(self, section, option, default='', expected_value=None):
        if expected_value is None:
            expected_value = []
        try:
            retval = self.config.get(section, option)
            if len(expected_value) != 0 and retval.lower() not in expected_value:
                self.error_msg += 'Error : Bad value option ' + str(option) + ' expected ' + str(expected_value) + '\n'
            else:
                return retval
        except configparser.NoOptionError:
            self.error_msg += 'Error : Missing mandatory option ' + str(option) + '\n'

        except configparser.NoSectionError:
            self.error_msg += 'Error : Missing mandatory section ' + str(section) + '\n'
        return default

    def check_options(self, section, list_option, filename):
        retval = True
        for option in list_option:
            if not self.config.has_option(section, option):
                retval = False
                self.error_msg += 'In ' + str(
                        filename) + ' missing option ' + option + ' in section ' + section + '\n'
        for option in self.config.options(section):
            if option not in list_option:
                retval = False
                self.error_msg += 'In ' + str(
                        filename) + ' unknown option ' + option + ' in section ' + section + '\n'
        return retval

    #
    # Configuration getter
    #
    def show_fullscreen(self):
        return self.fullscreen.lower() == 'yes'

    def maximize(self):
        return self.resolution.lower() == 'maximize'

    def get_unit_pixmap(self, file_name):
        """
        function get_unit_pixmap
        :param file_name: filename of the unit image
        :return: the QPixmap corresponding
        """
        return self.theme_selected.get_unit_pixmap(file_name)

    def get_map_pixmap(self, file_name):
        """
        function get_map_pixmap
        :param file_name: filename of the map image
        :return: the QPixmap corresponding
        """
        return self.theme_selected.get_map_pixmap(file_name)

    def get_string(self, key):
        if not isinstance(key, str) or key == '':
            raise ValueError('key must be a non empty string')
        return self.lang_selected.get_string(key)

    def get_nation(self, name):
        for nation in self.available_nation:
            if nation.name == name:
                return nation
        return None

    def get_unit_type(self, name):
        for unit_type in self.list_unit_type:
            if unit_type.name == name:
                return unit_type
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    config = Config()
    print(config)
