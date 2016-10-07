# Imperialism remake
# Copyright (C) 2014-16 Trilarion
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
    Game specific path locations for artwork, music, ...
    Only static values here.
"""

import os
from enum import unique

import lib.utils as utils

#: global switch for DEBUG MODE on (displays errors and info messages on console) and DEBUG MODE off (stores errors
# in the error log file)
DEBUG_MODE = True

#: QtWebEngine available
QtWebEngine_AVAILABLE = True
try:
    from PyQt5 import QtWebEngineWidgets
except ImportError:
    QtWebEngine_AVAILABLE = False


def extend(path, *parts):
    """
        Uses os.path.join to join parts of a path. Also checks for existence and raises an error
        if the path is not existing.
    """
    extended = os.path.join(path, *parts)
    if not os.path.exists(extended):
        raise RuntimeError('constructed path {} does not exist'.format(extended))
    if DEBUG_MODE:
        used_resources.add(extended)
    return extended


#: helpers
used_resources = set()

#: base folders (do not directly contain data)
DATA_FOLDER = extend('.', 'data')
ARTWORK_FOLDER = extend(DATA_FOLDER, 'artwork')

#: scenarios (save games)
SCENARIO_FOLDER = extend(DATA_FOLDER, 'scenarios')
CORE_SCENARIO_FOLDER = extend(SCENARIO_FOLDER, 'core')
SCENARIO_RULESET_FOLDER = extend(SCENARIO_FOLDER, 'rules')
SCENARIO_RULESET_STANDARD_FILE = extend(SCENARIO_RULESET_FOLDER, 'standard.rules')
#: Saved_Scenario_Folder = extend(SCENARIO_FOLDER, 'saved')

#: music related folders
MUSIC_FOLDER = extend(ARTWORK_FOLDER, 'music')
SOUNDTRACK_FOLDER = extend(MUSIC_FOLDER, 'soundtrack')
SOUNDTRACK_INFO_FILE = extend(SOUNDTRACK_FOLDER, 'soundtrack.info')

#: graphics related folders
GRAPHICS_FOLDER = extend(ARTWORK_FOLDER, 'graphics')
GRAPHICS_UI_FOLDER = extend(GRAPHICS_FOLDER, 'ui')
GRAPHICS_MAP_FOLDER = extend(GRAPHICS_FOLDER, 'map')

#: special locations
DOCUMENTATION_BASE_FOLDER = extend(DATA_FOLDER, 'manual')
DOCUMENTATION_INDEX_FILE = extend(DOCUMENTATION_BASE_FOLDER, 'index.html')
DOCUMENTATION_PREFERENCES_FILE = extend(DOCUMENTATION_BASE_FOLDER, 'ui', 'preferences.html')
GLOBAL_STYLESHEET_FILE = extend(GRAPHICS_UI_FOLDER, 'style.css')

# other specific constants

#: network communication
NETWORK_PORT = 42932

#: minimal screen resolution
MINIMAL_SCREEN_SIZE = (1024, 768)


# options

@unique
class Option(utils.AutoNumberedEnum):
    """
        Options as automatically numbered enum. The members of it are then the Options.
    """
    LOCALSERVER_OPEN = ()
    # local server accepts outside connections
    LOCALSERVER_NAME = ()
    MAINWINDOW_BOUNDS = ()
    MAINWINDOW_MAXIMIZED = ()  # bool
    MAINWINDOW_FULLSCREEN = ()
    MAINWINDOW_FULLSCREEN_SUPPORTED = ()  # is full screen supported

    # soundtrack
    SOUNDTRACK_MUTE = ()  # bool
    SOUNDTRACK_VOLUME = ()  # int from 0 to 100

    def __init__(self):
        self.default = None


Options = Option.__members__  # dictionary of name, Enum-value pairs

#: default values for the Options
Option.LOCALSERVER_OPEN.default = False
Option.LOCALSERVER_NAME.default = 'server name'
Option.MAINWINDOW_FULLSCREEN.default = True  # we start full screen (can be unset by the program for some linux desktop environments
Option.SOUNDTRACK_MUTE.default = False
Option.SOUNDTRACK_VOLUME.default = 50

#: predefined channel names for network communication
CH_SCENARIO_PREVIEW = 'general.scenario.preview'
CH_CORE_SCENARIO_TITLES = 'general.core.scenarios.titles'
CH_SYSTEM = 'system'


class TileDirections(utils.AutoNumberedEnum):
    """
    Six directions for six neighbored tiles in clockwise order.
    """
    WEST = ()
    NORTH_WEST = ()
    NORTH_EAST = ()
    EAST = ()
    SOUTH_EAST = ()
    SOUTH_WEST = ()

    def __init__(self):
        self.default = None


class ScenarioProperties:
    """
    Key names for general properties of a scenario.
    """

    SCENARIO_TITLE = 'scenario.title'
    SCENARIO_DESCRIPTION = 'scenario.description'
    MAP_COLUMNS = 'map.columns'
    MAP_ROWS = 'map.rows'
    RIVERS = 'rivers'


class ProvinceProperties:
    """
    Key names of properties of provinces.
    """
    TILES = 'tiles'
    NATION = 'nation'


class NationProperties:
    """
    Key names for nation properties of a scenario.
    """
    PROVINCES = 'provinces'
    COLOR = 'color'
    NAME = 'name'
    DESCRIPTION = 'description'
    CAPITAL_PROVINCE = 'capital_province'
