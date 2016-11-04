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

from base import switches
from lib import utils


def extend(path, *parts):
    """
        Uses os.path.join to join parts of a path. Also checks for existence and raises an error
        if the path is not existing.
    """
    extended = os.path.join(path, *parts)
    if switches.FILE_EXISTENCE_CHECK and not os.path.exists(extended):
        raise RuntimeError('constructed path {} does not exist'.format(extended))
    return extended


# TODO track used resources by the program

#: base folders (do not directly contain data)
DATA_FOLDER = extend('.', 'data')
ARTWORK_FOLDER = extend(DATA_FOLDER, 'artwork')

#: scenarios (save games)
SCENARIO_FOLDER = extend(DATA_FOLDER, 'scenarios')
CORE_SCENARIO_FOLDER = extend(SCENARIO_FOLDER, 'core')
SCENARIO_RULESET_FOLDER = extend(SCENARIO_FOLDER, 'rules')
SCENARIO_RULESET_STANDARD_FILE = extend(SCENARIO_RULESET_FOLDER, 'standard.rules')
SCENARIO_CLIENT_FOLDER = extend(SCENARIO_FOLDER, 'client')
SCENARIO_CLIENT_STANDARD_FILE = extend(SCENARIO_CLIENT_FOLDER, 'standard.config')
# Saved_Scenario_Folder = extend(SCENARIO_FOLDER, 'saved')

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
    LOCALCLIENT_NAME = ()
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
Option.LOCALSERVER_NAME.default = 'Alice'
Option.LOCALCLIENT_NAME.default = 'Bob'
Option.MAINWINDOW_FULLSCREEN.default = True  # we start full screen (can be unset by the program for some linux desktop environments
Option.SOUNDTRACK_MUTE.default = False
Option.SOUNDTRACK_VOLUME.default = 50

@unique
class C(utils.AutoNumberedEnum):
    """
    Predefined channels for network communication.
    """

    GENERAL = ()
    CHAT = ()
    SYSTEM = ()
    LOBBY = ()

@unique
class M(utils.AutoNumberedEnum):
    """
    Predefined network message types.
    """

    SYSTEM_SHUTDOWN = ()
    SYSTEM_MONITOR_UPDATE = ()

    CHAT_SUBSCRIBE = ()
    CHAT_UNSUBSCRIBE = ()
    CHAT_LOG = ()
    CHAT_MESSAGE = ()

    GENERAL_NAME = ()

    LOBBY_SCENARIO_CORE_LIST = ()
    LOBBY_SCENARIO_PREVIEW = ()
    LOBBY_CONNECTED_CLIENTS = ()

@unique
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


@unique
class ScenarioProperty(utils.AutoNumberedEnum):
    """
    Keys for general properties of a scenario.
    """

    TITLE = ()
    DESCRIPTION = ()
    MAP_COLUMNS = ()
    MAP_ROWS = ()
    RIVERS = ()
    RULES = ()
    GAME_YEAR_RANGE = ()

@unique
class NationProperty(utils.AutoNumberedEnum):
    """
    Keys for nation properties of a scenario.
    """
    PROVINCES = ()
    COLOR = ()
    NAME = ()
    DESCRIPTION = ()
    CAPITAL_PROVINCE = ()

@unique
class ProvinceProperty(utils.AutoNumberedEnum):
    """
    Keys for properties of provinces.
    """
    TILES = ()
    NAME = ()
    NATION = ()
    TOWN_LOCATION = ()

#: name of properties file in a zipped scenario file
SCENARIO_FILE_PROPERTIES = 'scenario-properties'
#: name of maps file in a zipped scenario file
SCENARIO_FILE_MAPS = 'maps'
#: name of provinces file in a zipped scenario file
SCENARIO_FILE_PROVINCES = 'provinces'
#: name of nations file in a zipped scenario file
SCENARIO_FILE_NATIONS = 'nations'


class ClientConfiguration:
    """
    Key names for scenario client configuration properties.
    """
    OVERVIEW_WIDTH = 'overview.width'

@unique
class OverviewMapMode(utils.AutoNumberedEnum):
    """
    Overview map modes.
    """
    POLITICAL = ()
    # local server accepts outside connections
    GEOGRAPHICAL = ()
