# Imperialism remake
# Copyright (C) 2014 Trilarion
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

import sys
import datetime

from PySide import QtGui, QtCore

from lib.utils import read_as_yaml, write_as_yaml
from base import constants as c


"""
    Non-specific independent helper functions. Do not depend on any other part of the project except on the constants.
"""


def load_ui_icon(name):
    """
        Load an icon from a base icon path.
    """
    file_name = c.extend(c.Graphics_UI_Folder, name)
    return QtGui.QIcon(file_name)


def log_info(text):
    """
        Prints a INFO message to stdout.
    """
    log_write_entry(sys.stdout, "INFO", text)


def log_warning(text):
    """
        Prints a WARNING message to stdout.
    """
    log_write_entry(sys.stdout, "WARNING", text)


def log_error(text, exception=None):
    """
        Prints a ERROR message and exception to stderr.
    """
    log_write_entry(sys.stderr, "ERROR", text, exception)
    # in case we send to somewhere else also send it to the standard error output (console)
    if sys.stderr is not sys.__stderr__:
        log_write_entry(sys.__stderr__, "ERROR", text, exception)


def log_write_entry(writer, prefix, text, exception=None):
    """
        Prints a message of format: date, time, prefix, text, exception to a writer.
    """
    now = datetime.datetime.now()
    header = now.isoformat(" ") + '\t' + prefix + '\t'

    print(header + text, end='\r\n', file=writer)

    if exception is not None:
        print(header + exception, end='\r\n', file=writer)


def find_unused_resources():
    """
        Report on unused ressources.
    """
    pass  # TODO not implemented yet

# singleton options dictionary (we only need one throughout the application)
options = {}


def load_options(file_name):
    """
        Load options from a JSON file and apply some conversions like changing the main window bounding rectangle
        from list to QtCore.QRect.
    """
    global options
    options = read_as_yaml(file_name)

    # delete entries that are not in Constants.Options
    for key in list(options.keys()):
        if key not in c.Options:
            del options[key]

    # copy values that are in Constants.Options but not here
    for key in c.Options:
        if key not in options:
            options[key] = c.Options[key].default

    # main window bounding rectangle, convert from list to QRect
    rect = get_option(c.O.MW_BOUNDS)
    if rect is not None:
        set_option(c.O.MW_BOUNDS, QtCore.QRect(*rect))

def get_option(option):
    """
        For an option (OptionEnum in Constants), returns the entry in the options dictionary stored here.
    """
    return options[option.name]

def set_option(option, value):
    """
        For an option (OptionEnum in Constants), sets the entry of the options dictionary store here to a certain value.
    """
    options[option.name] = value

def save_options(file_name):
    """
        Saves the options into a YAML file after performing some conversions from types like QtCore.QRect to list, ...
    """
    data = options.copy()

    # main window bounding rectangle, convert from QRect to list
    rect = data[c.O.MW_BOUNDS.name]
    data[c.O.MW_BOUNDS.name] = [rect.x(), rect.y(), rect.width(), rect.height()]

    # write to file
    write_as_yaml(file_name, data)