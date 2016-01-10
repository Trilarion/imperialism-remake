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

import logging
import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDesktopWidget

from base.constants import parse_resolution, LOG_FILENAME, LOG_PATTERN, MINIMUM_RESOLUTION
from config.configparserextended import ConfigParserExtended
from config.lang import Lang
from config.theme import Theme
from nation.nation import Nation
from unit.landUnitType import LandUnitType

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


class Config(ConfigParserExtended):


    def load_themes_config(self):
        available_theme = []
        theme_selected = None
        for section in self.sections():
            if section.startswith('theme'):
                if self.check_options(section, MANDATORY_THEME_OPTION):
                    name = self.get_string(section, 'name')
                    description = self.get_string(section, 'description')
                    coat_of_arms_graphics = self.get_string(section, 'coat_of_arms_graphics')
                    flag_graphics = self.get_string(section, 'flag_graphics')
                    map_graphics = self.get_string(section, 'map_graphics')
                    unit_graphics = self.get_string(section, 'unit_graphics')
                    background = self.get_string(section, 'background')
                    end_button = self.get_string(section, 'end_button')
                    autocombat_button = self.get_string(section, 'autocombat_button')
                    help_button = self.get_string(section, 'help_button')
                    retreat_button = self.get_string(section, 'retreat_button')
                    target_button = self.get_string(section, 'target_button')
                    outside_city_pixmap = self.get_string(section, 'outside_city_pixmap')
                    outside_city_color = self.get_string(section, 'outside_city_color')
                    city_pixmap = self.get_string(section, 'city_pixmap')
                    city_color = self.get_string(section, 'city_color')
                    try:
                        theme = Theme(name, description, coat_of_arms_graphics, flag_graphics, map_graphics,
                                      unit_graphics, background, end_button, autocombat_button, help_button,
                                      retreat_button, target_button, outside_city_pixmap, outside_city_color,
                                      city_pixmap, city_color)
                        available_theme.append(theme)

                        if name == self.name_theme_selected:
                            theme_selected = theme
                    except ValueError as e:
                        self.errors.append(str(e))
        if theme_selected is None:
            tmp = 'Theme \'%s\' not found (available theme: [' % self.name_theme_selected
            for t in available_theme:
                tmp += '\'%s\',' % t.name
            tmp += '])'
            self.errors.append(tmp.replace(',]',']'))
        if len(available_theme) == 0:
            self.errors.append('No Theme available')
        return theme_selected, available_theme

    def load_units_config(self):
        list_unit_type = []
        if self.unit_config_file != 'error' and self.theme_selected is not None:
            units_config = ConfigParserExtended(self.unit_config_file)
            for section in units_config.sections():
                if units_config.check_options(section, MANDATORY_UNIT_OPTION):
                    try:
                        nb_error = len(units_config.errors)
                        name = units_config.get_string(section, 'name')
                        evolution_level = units_config.get_int(section, 'level')
                        description = units_config.get_string(section, 'description')
                        officier = units_config.get_boolean(section, 'officier')
                        attack_strength = units_config.get_int(section, 'attack')
                        fire_range = units_config.get_int(section, 'range')
                        speed = units_config.get_int(section, 'speed')
                        creation_cost = units_config.get_float(section, 'creationcost')
                        upkeep = units_config.get_float(section, 'upkeep')
                        graphic_charge_filename = units_config.get_string(section, 'pixmap.charge',
                                                                          pattern='^.*\.(png|PNG)$')
                        graphic_charge = QPixmap(self.theme_selected.unit_graphics + '/' + graphic_charge_filename)
                        graphic_shoot_filename = units_config.get_string(section, 'pixmap.shoot',
                                                                         pattern='^.*\.(png|PNG)$')
                        graphic_shoot = QPixmap(self.theme_selected.unit_graphics + '/' + graphic_shoot_filename)
                        graphic_stand_filename = units_config.get_string(section, 'pixmap.stand',
                                                                         pattern='^.*\.(png|PNG)$')
                        graphic_stand = QPixmap(self.theme_selected.unit_graphics + '/' + graphic_stand_filename)
                        unit_type = LandUnitType(name, evolution_level, description, officier, attack_strength,
                                                 fire_range, speed, creation_cost, upkeep, graphic_charge,
                                                 graphic_shoot, graphic_stand)
                        if nb_error == len(units_config.errors):
                            list_unit_type.append(unit_type)
                    except AttributeError as e:
                        units_config.errors.append(str(e))
                    except ValueError as e:
                        units_config.errors.append(str(e))
            self.errors.extend(units_config.errors)
        return list_unit_type

    def load_langs_config(self):
        lang_selected = None
        available_lang = []
        if self.lang_config_file != 'error':
            langs_config = ConfigParserExtended(self.lang_config_file)
            for section in langs_config.sections():
                try:
                    name = langs_config.get_string(section, 'name')
                    description = langs_config.get_string(section, 'description')
                    lang = Lang(name, description)
                    for option in langs_config.options(section):
                        lang.add_string(option, langs_config.get_string(section, option))
                    if name == self.name_lang_selected:
                        lang_selected = lang
                    available_lang.append(lang)
                except ValueError as e:
                    langs_config.errors.append(str(e))
            self.errors.extend(langs_config.errors)
        if lang_selected is None:
            self.errors.append('Lang: \'%s\' not found' % self.name_lang_selected)
        if len(available_lang) == 0:
            self.errors.append('No Lang available')

        return lang_selected, available_lang

    def load_nations_config(self):
        available_nation = []
        if self.nation_config_file != 'error' and self.theme_selected is not None:
            nations_config = ConfigParserExtended(self.nation_config_file)
            for section in nations_config.sections():
                try:
                    name = nations_config.get_string(section, 'name')
                    flag_filename = nations_config.get_string(section, 'flag', pattern='^.*\.(png|PNG)$')
                    flag = QPixmap(self.theme_selected.flag_graphics + '/' + flag_filename)
                    coat_of_arms_filename = nations_config.get_string(section, 'coat_of_arms',
                                                                      pattern='^.*\.(png|PNG)$')
                    coat_of_arms = QPixmap(self.theme_selected.coat_of_arms_graphics + '/' + coat_of_arms_filename)
                    nation = Nation(name, False, coat_of_arms, flag)
                    available_nation.append(nation)
                except AttributeError as e:
                    nations_config.errors.append(str(e))
                except ValueError as e:
                    nations_config.errors.append(str(e))
            self.errors.extend(nations_config.errors)
        if len(available_nation) == 0  and self.theme_selected is not None:
            self.errors.append('No Nation available')
        return available_nation

    def __init__(self, main_config_file):
        # load main option
        self.data_folder = 'error'
        ConfigParserExtended.__init__(self, main_config_file)
        self.check_options('config', MANDATORY_CONFIG_OPTION)
        self.check_options('path', MANDATORY_PATH_OPTION)
        self.check_options('battle', MANDATORY_BATTLE_OPTION)
        self.fullscreen = self.get_boolean('config', 'fullscreen')
        self.log_level = self.get_int('config', 'log_level', expected_values=[50, 40, 30, 20, 10])
        self.name_theme_selected = self.get_string('config', 'theme')
        self.name_lang_selected = self.get_string('config', 'lang')
        self.resolution = self.get_string('config', 'resolution', pattern='^(\d+)\s*x\s*(\d+)$|^maximize$')
        # load battle option
        self.diameter_battlemap = self.get_int('battle', 'diameter_battlemap', even=False)
        self.diameter_battlecity = self.get_int('battle', 'diameter_battlecity', even=False)
        # load path config
        self.data_folder = self.get_dirname('path', 'data')
        self.lang_config_file = self.get_filename('path', 'lang_config_file')
        self.unit_config_file = self.get_filename('path', 'unit_config_file')
        self.nation_config_file = self.get_filename('path', 'nation_config_file')
        # load theme config
        self.theme_selected, self.available_theme = self.load_themes_config()
        # load unit config
        self.list_unit_type = self.load_units_config()
        # load lang config
        self.lang_selected, self.available_lang = self.load_langs_config()
        # load nation config
        self.available_nation = self.load_nations_config()
        print('here: ' + self.get_error_str() + '\n\n')
        # check resolution min, max...
        w, h = parse_resolution(self.resolution)
        if w != -1 and h != -1:
            minw, minh = MINIMUM_RESOLUTION
            screen = QDesktopWidget().screenGeometry()
            maxw, maxh = screen.width(), screen.height()
            if w < minw or h < minh:
                self.errors.append('Bad resolution (width must be superior to %d and height must be superior to %d) (current %d x %d)' % (
                minw, minh, w, h))
            if w > maxw or h > maxh:
                self.errors.append('Bad resolution (width must be inferior to screen width resolution %d and height must be inferior to screen height resolution %d) (current %d x %d)' % (
                maxw, maxh, w, h))
        # set log level
        logging.basicConfig(level=self.log_level, filename=LOG_FILENAME, filemode='w', format=LOG_PATTERN)

    #
    # Overwrite class method
    #
    def __str__(self):
        retval = 'Error : \n'
        retval += self.get_error_str()
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
    # Configuration getter
    #
    def show_fullscreen(self):
        return self.fullscreen

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

    def get_text(self, key):
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

