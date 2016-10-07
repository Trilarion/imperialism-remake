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

"""
    Non-specific independent helper functions. Do not depend on any other part of the project except on package lib
    and base.constants and is specifically used by the project.
"""

import sys

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

import base.constants as constants
import lib.utils as utils

def load_ui_icon(name):
    """
    Loads an icon from a base icon path.

    :param name:
    :return:
    """
    file_name = constants.extend(constants.GRAPHICS_UI_FOLDER, name)
    return QtGui.QIcon(file_name)


def log_info(text):
    """
    Prints a INFO message to stdout.

    :param text:
    """
    utils.log_write_entry(sys.stdout, "INFO", text)


def log_warning(text):
    """
    Prints a WARNING message to stdout.

    :param text:
    """
    utils.log_write_entry(sys.stdout, "WARNING", text)


def log_error(text, exception=None):
    """
    Prints a ERROR message and exception to stderr.

    :param text:
    :param exception:
    """
    utils.log_write_entry(sys.stderr, "ERROR", text, exception)
    # in case we send to somewhere else also send it to the standard error output (console)
    if sys.stderr is not sys.__stderr__:
        utils.log_write_entry(sys.__stderr__, "ERROR", text, exception)

def find_unused_resources():
    """
    Report on unused resources.
    """
    pass  # TODO not implemented yet


# singleton options dictionary (we only need one throughout the application)
options = {}


def load_options(file_name):
    """
    Load options from a JSON file and apply some conversions like changing the main window bounding rectangle
    from list to QtCore.QRect.

    :param file_name:
    """
    global options
    options = utils.read_as_yaml(file_name)

    # delete entries that are not in Constants.Options
    for key in list(options.keys()):
        if key not in constants.Options:
            del options[key]

    # copy values that are in Constants.Options but not here
    for key in constants.Options:
        if key not in options:
            options[key] = constants.Options[key].default

    # main window bounding rectangle, convert from list to QRect
    rect = get_option(constants.Option.MAINWINDOW_BOUNDS)
    if rect is not None:
        set_option(constants.Option.MAINWINDOW_BOUNDS, QtCore.QRect(*rect))


def get_option(option):
    """
    For an option (OptionEnum in Constants), returns the entry in the options dictionary stored here.

    :param option:
    :return:
    """
    return options[option.name]


def set_option(option, value):
    """
    For an option (OptionEnum in Constants), sets the entry of the options dictionary store here to a certain value.

    :param option:
    :param value:
    """
    options[option.name] = value


def save_options(file_name):
    """
    Saves the options into a YAML file after performing some conversions from types like QtCore.QRect to list, ...

    :param file_name:
    """
    data = options.copy()

    # main window bounding rectangle, convert from QRect to list
    option = constants.Option.MAINWINDOW_BOUNDS.name
    if option in data:
        rect = data[option]
        data[option] = [rect.x(), rect.y(), rect.width(), rect.height()]

    # write to file
    utils.write_as_yaml(file_name, data)
