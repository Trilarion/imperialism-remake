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


DEFAULT_STRING = 'default'


class ConfigLang:
    # Constructor
    def __init__(self, config_filename):
        self.config_filename = config_filename


class Lang:
    # Constructor
    def __init__(self, name, description):
        """constructor
        :param name: str
        :param description: str
        """
        if not isinstance(name, str) or name == '':
            raise ValueError('name must be a non empty string')
        if not isinstance(description, str) or description == '':
            raise ValueError('description must be a non empty string')
        self.name = name
        self.description = description
        self.strings = {DEFAULT_STRING: DEFAULT_STRING}

    # Operations
    def add_string(self, key, value):
        if not isinstance(key, str) or key == '':
            raise ValueError('key must be a non empty string')
        if not isinstance(value, str) or value == '':
            raise ValueError('value must be a non empty string')
        self.strings[key] = value

    def get_string(self, key):
        if not isinstance(key, str) or key == '':
            raise ValueError('key must be a non empty string')
        return self.strings.get(key, DEFAULT_STRING)
