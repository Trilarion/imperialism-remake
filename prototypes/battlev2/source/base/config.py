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

CONFIG_FILE = 'config.ini'
DEFAULT_FULLSCREEN = 'yes'
DEFAULT_THEME = 'theme0'
DEFAULT_RESOLUTION = 'maximize'


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read_file(open(CONFIG_FILE))
        self.error_msg = ''
        # fullscreen option
        self.fullscreen = self.get_config('config', 'fullscreen', DEFAULT_FULLSCREEN, ['yes', 'no'])
        # resolution
        # TODO get list supported  resolution...
        self.resolution =  self.get_config('config', 'maximize', DEFAULT_RESOLUTION, ['maximize'])
        #path file
        self.data = self.get_config('path', 'data', '', [])
        if not os.path.isdir(self.data):
            self.error_msg += 'data folder ' + self.data + ' doesn\'t exist\n'
            self.data = 'error'
        # theme config file
        self.theme_config_file = self.get_config('path', 'theme_config_file', '', []).replace('$data',self.data)
        if not os.path.exists(self.theme_config_file):
            self.error_msg += 'theme config file ' + self.theme_config_file + ' doesn\'t exist\n'
            self.theme_config_file = 'error'
        # lang config file
        self.lang_config_file = self.get_config('path', 'lang_config_file', '', []).replace('$data',self.data)
        if not os.path.exists(self.lang_config_file):
            self.error_msg += 'lang config file ' + self.lang_config_file + ' doesn\'t exist\n'
            self.lang_config_file = 'error'
        # unit config file
        self.unit_config_file = self.get_config('path', 'unit_config_file', '', []).replace('$data',self.data)
        if not os.path.exists(self.unit_config_file):
            self.error_msg += 'unit config file ' + self.unit_config_file + ' doesn\'t exist\n'
            self.unit_config_file = 'error'
        # battle config file
        self.battle_config_file = self.get_config('path', 'battle_config_file', '', []).replace('$data',self.data)
        if not os.path.exists(self.battle_config_file):
            self.error_msg += 'battle config file ' + self.battle_config_file + ' doesn\'t exist\n'
            self.battle_config_file = 'error'



        # theme
        #list_themes = []
        #for section in self.config.sections():
        #    if section.startswith('theme'):
        #        list_themes.append(section)
        # TODO
        # list_themes.size == 0 => error
        # list_themes.size == 1 => DEFAULT_THEME = elem
        # list_themes.size and DEFAULT_THEME not in => DEFAULT_THEME.elem 0
        #self.theme = self.get_config('config', 'theme', DEFAULT_THEME, list_themes)
        #if self.error_msg != '':
        #    raise Exception('')

    def fullscreen(self):
        return self.fullscreen == 'yes'

    def maximize(self):
        return self.resolution == 'maximize'




    def get_config(self, section, option, default, expected_value):
        try:
            retval = self.config.get(section, option)
            if len(expected_value) != 0 and retval.lower() not in expected_value:
                self.error_msg += 'Error : Bad value option ' + str(option) + ' expected ' + str(expected_value) + '\n'
            else:
                return retval.lower()
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
        retval += 'data folder:' + str(self.data) + '\n'
        retval += 'theme config file:' + str(self.theme_config_file) + '\n'
        retval += 'lang config file:' + str(self.lang_config_file) + '\n'
        retval += 'unit config file:' + str(self.unit_config_file) + '\n'
        retval += 'battle config file:' + str(self.battle_config_file) + '\n'
        return retval


if __name__ == '__main__':
    config = Config()
    print(config)
