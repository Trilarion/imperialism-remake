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

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDesktopWidget

from prototypes.battle.source.base.constants import parse_resolution, LOG_FILENAME, LOG_PATTERN, MINIMUM_RESOLUTION
from prototypes.battle.source.config.configparserextended import ConfigParserExtended
from prototypes.battle.source.config.lang import Lang
from prototypes.battle.source.config.theme import Theme
from prototypes.battle.source.nation.nation import Nation
from prototypes.battle.source.unit.landUnitType import LandUnitType


MANDATORY_UNIT_OPTION = ['name', 'description', 'officier', 'level', 'attack', 'range', 'speed', 'creationcost',
                         'upkeep', 'pixmap.charge', 'pixmap.shoot', 'pixmap.stand']
MANDATORY_CONFIG_OPTION = ['fullscreen', 'resolution', 'theme', 'lang', 'log_level']
MANDATORY_PATH_OPTION = ['data', 'lang_config_file', 'unit_config_file', 'nation_config_file']
MANDATORY_BATTLE_OPTION = ['diameter_battlemap', 'diameter_battlecity']
MANDATORY_THEME_OPTION = ['name', 'description', 'coat_of_arms_graphics', 'flag_graphics', 'map_graphics',
                          'unit_graphics', 'background', 'end_button', 'autocombat_button', 'help_button',
                          'retreat_button', 'target_button', 'outside_city_pixmap', 'outside_city_color',
                          'city_pixmap', 'city_color', 'defeat_graphics', 'victory_graphics']
MANDATORY_NATION_OPTION = ['name', 'flag', 'coat_of_arms']


class Config(ConfigParserExtended):

    def __init__(self, main_config_file, version):
        self.version = version

        # load main option
        self.data_folder = 'error'
        ConfigParserExtended.__init__(self, main_config_file)
        self.check_options('config', MANDATORY_CONFIG_OPTION)
        self.check_options('path', MANDATORY_PATH_OPTION)
        self.check_options('battle', MANDATORY_BATTLE_OPTION)

        # set log level
        self.log_level = self.get_int('config', 'log_level', expected_values=[50, 40, 30, 20, 10])
        logging.basicConfig(level=self.log_level, filename=LOG_FILENAME, filemode='w', format=LOG_PATTERN)
        self.fullscreen = self.get_boolean('config', 'fullscreen')
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
        self.check_resolution()

        logging.info('[END] __init__(main_config_file=%s) => %s' % (main_config_file, str(self)))

    def load_themes_config(self):
        logging.debug('[ENTER] load_themes_config()')
        available_theme = []
        theme_selected = None
        for section in self.sections():
            logging.debug('[LOOP] load_themes_config(): section=%s' % section)
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
                    victory_pixmap = self.get_string(section, 'victory_graphics', pattern='^.*\.(png|PNG)$')
                    defeat_pixmap = self.get_string(section, 'defeat_graphics', pattern='^.*\.(png|PNG)$')
                    try:
                        theme = Theme(name, description, coat_of_arms_graphics, flag_graphics, map_graphics,
                                      unit_graphics, background, end_button, autocombat_button, help_button,
                                      retreat_button, target_button, outside_city_pixmap, outside_city_color,
                                      city_pixmap, city_color, victory_pixmap, defeat_pixmap)
                        available_theme.append(theme)

                        if name == self.name_theme_selected:
                            theme_selected = theme
                    except ValueError as e:
                        logging.error('[ERROR] load_themes_config() : %s' % str(e))
                        self.errors.append(str(e))
        if theme_selected is None:
            tmp = 'Theme \'%s\' not found (available theme: [' % self.name_theme_selected
            for t in available_theme:
                tmp += '\'%s\',' % t.name
            tmp += '])'
            tmp = tmp.replace(',]', ']')
            logging.error(tmp)
            self.errors.append(tmp)
        if len(available_theme) == 0:
            logging.error('No Theme available')
            self.errors.append('No Theme available')
        logging.debug('[EXIT] load_themes_config() => found %d themes, selected=%s' % (len(available_theme), theme_selected))
        return theme_selected, available_theme

    def load_units_config(self):
        logging.debug('[ENTER] load_units_config()')
        list_unit_type = []
        if self.unit_config_file != 'error' and self.theme_selected is not None:
            units_config = ConfigParserExtended(self.unit_config_file)
            for section in units_config.sections():
                logging.debug('[LOOP] load_units_config(): section=%s' % section)
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
                        logging.error('[ERROR] load_units_config() : %s' % str(e))
                        units_config.errors.append(str(e))
                    except ValueError as e:
                        logging.error('[ERROR] load_units_config() : %s' % str(e))
                        units_config.errors.append(str(e))
            self.errors.extend(units_config.errors)
            if len(units_config.errors) != 0:
                logging.error('[ERROR] load_units_config() : %s' % units_config.get_error_str())
        logging.debug('[EXIT] load_units_config() => found %d units type' % len(list_unit_type))
        return list_unit_type

    def load_langs_config(self):
        logging.debug('[ENTER] load_langs_config()')
        lang_selected = None
        available_lang = []
        if self.lang_config_file != 'error':
            langs_config = ConfigParserExtended(self.lang_config_file)
            for section in langs_config.sections():
                logging.debug('[LOOP] load_langs_config(), section %s' % section)
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
                    logging.error('[ERROR] load_langs_config() : %s' % str(e))
                    langs_config.errors.append(str(e))
            self.errors.extend(langs_config.errors)
            if len(langs_config.errors) != 0:
                logging.error('[ERROR] load_langs_config() : %s' % langs_config.get_error_str())
        if lang_selected is None:
            msg = 'Lang: \'%s\' not found' % self.name_lang_selected
            logging.error('[ERROR] load_langs_config() : %s' % msg)
            self.errors.append(msg)
        if len(available_lang) == 0:
            logging.error('[ERROR] load_langs_config() : No Lang available')
            self.errors.append('No Lang available')
        logging.debug('[EXIT] load_langs_config() => found %d langs, selected %s' % (len(available_lang), str(lang_selected)))
        return lang_selected, available_lang

    def load_nations_config(self):
        logging.debug('[ENTER] load_nations_config()')
        available_nation = []
        if self.nation_config_file != 'error' and self.theme_selected is not None:
            nations_config = ConfigParserExtended(self.nation_config_file)
            for section in nations_config.sections():
                try:
                    logging.debug('[LOOP] load_nations_config(), section %s' % section)
                    name = nations_config.get_string(section, 'name')
                    flag_filename = nations_config.get_string(section, 'flag', pattern='^.*\.(png|PNG)$')
                    flag = QPixmap(self.theme_selected.flag_graphics + '/' + flag_filename)
                    coat_of_arms_filename = nations_config.get_string(section, 'coat_of_arms',
                                                                      pattern='^.*\.(png|PNG)$')
                    coat_of_arms = QPixmap(self.theme_selected.coat_of_arms_graphics + '/' + coat_of_arms_filename)
                    nation = Nation(name, False, coat_of_arms, flag)
                    available_nation.append(nation)
                except AttributeError as e:
                    logging.error('[ERROR] load_nations_config() : %s' % str(e))
                    nations_config.errors.append(str(e))
                except ValueError as e:
                    logging.error('[ERROR] load_nations_config() : %s' % str(e))
                    nations_config.errors.append(str(e))
            self.errors.extend(nations_config.errors)
            if len(nations_config.errors) != 0:
                logging.error('[ERROR] load_nations_config() : %s' % nations_config.get_error_str())
        if len(available_nation) == 0 and self.theme_selected is not None:
            logging.error('[ERROR] load_nations_config() : No Nation available')
            self.errors.append('No Nation available')
        logging.debug('[EXIT] load_nations_config() => found %d' % len(available_nation))
        return available_nation

    def __str__(self):
        logging.debug('[ENTER] __str__()')
        themes = '\n'
        for t in self.available_theme:
            themes += '\t\tTheme \'%s\': %s' % (t.name, str(t).replace('\t\t', '\t\t\t'))
        units = '\n'
        for u in self.list_unit_type:
            units += '\t\tUnit Type \'%s\': %s' % (u.name, str(u).replace('\t', '\t\t\t'))
        nations = '\n'
        for n in self.available_nation:
            nations += '\t\tNation \'%s\': %s' % (n.name, str(n).replace('\t', '\t\t\t'))
        langs = ''
        for l in self.available_lang:
            langs += '\n\t\tLang \'%s\': %s' % (l.name, str(l).replace('\t\t', '\t\t\t'))
        logging.debug('[EXIT] __str__()')
        return '\n\tError: %s\n\tLog level: %d\n\tFullscreen: %r\n\tTheme: %s\n\tLang: %s\n\tResolution: %s\n\tBattle map diameter: %d\n' \
               '\tCity diameter: %d\n\tData folder: %s\n\tLang config file: %s\n\tUnit config file: %s\n\tNation config file: %s\n' \
               '\tTheme selected: %s\n\tLang Selected: %s\n\tAvailable Themes:%s\n\tAvailable Units: %s\n\tAvailable Nations: %s\n\t' \
               'Available langs: %s' \
               % (
                   self.get_error_str(), self.log_level, self.fullscreen, self.name_theme_selected,
                   self.name_lang_selected,
                   self.resolution, self.diameter_battlemap, self.diameter_battlecity, self.data_folder,
                   self.lang_config_file,
                   self.unit_config_file, self.nation_config_file, self.theme_selected, self.lang_selected, themes,
                   units,
                   nations, langs)

    def check_resolution(self):
        logging.debug('[ENTER] check_resolution(), resolution=%s' % self.resolution)
        # check resolution min, max...
        w, h = parse_resolution(self.resolution)
        if w != -1 and h != -1:
            minw, minh = MINIMUM_RESOLUTION
            screen = QDesktopWidget().screenGeometry()
            maxw, maxh = screen.width(), screen.height()
            logging.debug('check_resolution() => current width=%d, current_height=%d, min width=%d, '
                          'min height=%d, max width=%d, max height=%d' % (w, h, minw, minh, maxw, maxh))
            if w < minw or h < minh:
                msg = 'Bad resolution (width must be superior to %d and height must be superior to %d) (current %d x %d)' % (
                    minw, minh, w, h)
                self.errors.append(msg)
                logging.error(msg)
            if w > maxw or h > maxh:
                msg = 'Bad resolution (width must be inferior to screen width resolution %d and height must be inferior to screen height resolution %d) (current %d x %d)' % (
                    maxw, maxh, w, h)
                self.errors.append(msg)
                logging.error(msg)
        logging.debug('[EXIT] check_resolution(), resolution=%s' % self.fullscreen)

    #
    # Configuration getter
    #
    def show_fullscreen(self):
        logging.debug('[ENTER|EXIT] show_fullscreen() => return %r' % self.fullscreen)
        return self.fullscreen

    def maximize(self):
        logging.debug('[ENTER] maximize()')
        retval = self.resolution.lower() == 'maximize'
        logging.debug('[EXIT] maximize() return \'%r\'' % retval)
        return retval

    def get_unit_pixmap(self, file_name):
        """
        function get_unit_pixmap
        :param file_name: filename of the unit image
        :return: the QPixmap corresponding
        """
        logging.debug('[ENTER|EXIT] get_unit_pixmap(file_name=\'%s\')' % file_name)
        return self.theme_selected.get_unit_pixmap(file_name)

    def get_map_pixmap(self, file_name):
        """
        function get_map_pixmap
        :param file_name: filename of the map image
        :return: the QPixmap corresponding
        """
        logging.debug('[ENTER|EXIT] get_map_pixmap(file_name=\'%s\')' % file_name)
        return self.theme_selected.get_map_pixmap(file_name)

    def get_text(self, key):
        logging.debug('[ENTER] get_text(key=\'%s\')' % key)
        if not isinstance(key, str) or key == '':
            logging.error('[ERROR] get_text(key=\'%s\') : key must be a non empty string' % key)
            raise ValueError('key must be a non empty string')
        retval = self.lang_selected.get_string(key)
        logging.debug('[EXIT] get_text(key=\'%s\') return \'%s\'' % (key, retval))
        return retval

    def get_nation(self, name):
        logging.debug('[ENTER] get_nation(name=\'%s\')' % name)
        for nation in self.available_nation:
            if nation.name == name:
                logging.debug('[EXIT] get_nation(name=\'%s\') return None' % name)
                return nation
        logging.debug('[EXIT] get_nation(name=\'%s\') return None' % name)
        return None

    def get_unit_type(self, name):
        logging.debug('[ENTER] get_unit_type(name=\'%s\')' % name)
        for unit_type in self.list_unit_type:
            if unit_type.name == name:
                logging.debug('[EXIT] get_unit_type(name=\'%s\') return \'%s\'' % (name, name))
                return unit_type
        logging.debug('[EXIT] get_unit_type(name=\'%s\') return None' % name)
        return None
