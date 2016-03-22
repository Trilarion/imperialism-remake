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
import re
import sys


class ConfigParserExtended(configparser.ConfigParser):
    def __init__(self, file_name):
        self.errors = []
        configparser.ConfigParser.__init__(self, interpolation=configparser.ExtendedInterpolation())
        self.read_file(open(file_name))
        self.file_name = file_name

    def check_options(self, section, list_option):
        for option in list_option:
            if not self.has_option(section, option):
                self.errors.append(
                        'In \'%s\' missing option \'%s\' in section \'%s\'' % (self.file_name, option, section))
                return False
        for option in self.options(section):
            if option not in list_option:
                self.errors.append(
                        'In \'%s\' unknown option \'%s\' in section \'%s\'' % (self.file_name, option, section))
                return False
        return True

    def get_string(self, section, option, default='', pattern=None):
        nb_error = len(self.errors)
        try:
            retval = self.get(section, option)
            if pattern is not None and not re.match(pattern, retval):
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad syntax option \'%s\', expected syntax \'%s\' (current \'%s\')' % (
                            self.file_name, section, option, pattern, retval))
            if len(self.errors) == nb_error:
                return retval
        except configparser.NoOptionError:
            self.errors.append('In file \'%s\' and section \'%s\' : Missing mandatory option \'%s\'' % (
                self.file_name, section, option))
        except configparser.NoSectionError:
            self.errors.append('In file \'%s\' : Missing mandatory section \'%s\'' % (
                self.file_name, section))
        return default

    def get_int(self, section, option, default=0, int_min=-sys.maxsize + 1, int_max=sys.maxsize, even=True, odd=True,
                expected_values=None):
        nb_error = len(self.errors)
        try:
            retval = self.getint(section, option)
            if retval < int_min:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be inferior to %d (current:%d)' % (
                            self.file_name, section, option, int_min, retval))
            if retval > int_max:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be superior to %d (current:%d)' % (
                            self.file_name, section, option, int_max, retval))
            if retval % 2 == 0 and not even:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be a even number (current:%d)' % (
                            self.file_name, section, option, retval))
            if retval % 2 == 1 and not odd:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be a odd number (current:%d)' % (
                            self.file_name, section, option, retval))
            if expected_values is not None and retval not in expected_values:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be in \'%s\' (current:%d)' % (
                            self.file_name, section, option, str(expected_values), retval))
            if len(self.errors) == nb_error:
                return retval
        except configparser.NoOptionError:
            self.errors.append('In file \'%s\' and section \'%s\' : Missing mandatory option \'%s\'' % (
                self.file_name, section, option))
        except configparser.NoSectionError:
            self.errors.append('In file \'%s\' : Missing mandatory section \'%s\'' % (self.file_name, section))
        except ValueError as e:
            self.errors.append(
                    'In file \'%s\' in section \'%s\', option \'%s\' : \'%s\'' % (
                        self.file_name, section, option, str(e)))
        return default

    def get_float(self, section, option, default=0, float_min=-sys.maxsize + 1, float_max=sys.maxsize,
                  expected_values=None):
        nb_error = len(self.errors)
        try:
            retval = self.getfloat(section, option)
            if retval < float_min:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be inferior to %d (current:%d)' % (
                            self.file_name, section, option, float_min, retval))
            if retval > float_max:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be superior to %d (current:%d)' % (
                            self.file_name, section, option, float_max, retval))
            if expected_values is not None and retval not in expected_values:
                self.errors.append(
                        'In file \'%s\' and section \'%s\' : Bad option \'%s\' should be in \'%s\' (current:%d)' % (
                            self.file_name, section, option, str(expected_values), retval))
            if len(self.errors) == nb_error:
                return retval
        except configparser.NoOptionError:
            self.errors.append('In file \'%s\' and section \'%s\' : Missing mandatory option \'%s\'' % (
                self.file_name, section, option))
        except configparser.NoSectionError:
            self.errors.append('In file \'%s\' : Missing mandatory section \'%s\'' % (self.file_name, section))
        except ValueError as e:
            self.errors.append(
                    'In file \'%s\' in section \'%s\', option \'%s\' : \'%s\'' % (
                        self.file_name, section, option, str(e)))
        return default

    def get_boolean(self, section, option, default=False):
        try:
            retval = self.getboolean(section, option)
            return retval
        except configparser.NoOptionError:
            self.errors.append('In file \'%s\' and section \'%s\' : Missing mandatory option \'%s\'' % (
                self.file_name, section, option))
        except configparser.NoSectionError:
            self.errors.append('In file \'%s\' : Missing mandatory section \'%s\'' % (self.file_name, section))
        except ValueError as e:
            self.errors.append(
                    'In file \'%s\' in section \'%s\', option \'%s\' : \'%s\'' % (
                        self.file_name, section, option, str(e)))
        return default

    def get_dirname(self, section, option, default=''):
        retval = self.get_string(section, option, default='')
        if not os.path.isdir(retval):
            self.errors.append('In file \'%s\' and section \'%s\' : Option \'%s\' must be a existing directory name' % (
                self.file_name, section, option))
            return default
        return retval

    def get_filename(self, section, option, default=''):
        retval = self.get_string(section, option, default='')
        if not os.path.exists(retval):
            self.errors.append('In file \'%s\' and section \'%s\' : Option \'%s\' must be a existing file name' % (
                self.file_name, section, option))
            return default
        return retval

    def get_error_str(self):
        retval = ''
        for e in self.errors:
            retval += '%s\n' % e
        return retval
