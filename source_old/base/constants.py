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

from PyQt5 import QtCore
import os
import sys
from enum import unique

import lib.utils as u

"""
    Game specific path locations for artwork, music, ...
    Only static values here.
"""


def extend(path, *parts):
    """
        Uses os.path.join to join parts of a path. Also checks for existence and raises an error
        if the path is not existing.
    """
    extended = os.path.join(path, *parts)
    if not os.path.exists(extended):
        raise RuntimeError('constructed path {} does not exist'.format(extended))
    if Debug_Mode:
        Used_Resources.add(extended)
    return extended

# debug mode and helpers
Debug_Mode = False
Used_Resources = set()

# resolve Project_Root directory as the directory that holds the .git folder
Project_Root = os.getcwd()
while '.git' not in [_dir for _dir in os.listdir(Project_Root)]:
    Project_Root = os.path.abspath(os.path.join(Project_Root, ".."))
    if Debug_Mode:
        sys.stderr.write("Searching for project root folder in: {0}\n".format(Project_Root))
    if Project_Root.count(os.sep) == 1:
        raise SystemExit

# base folders (do not directly contain data)
Data_Folder = extend(Project_Root, 'data')
Artwork_Folder = extend(Data_Folder, 'artwork')
Resources_Folder = extend(Project_Root, 'resources')

# scenarios (save games)
Scenario_Folder = extend(Data_Folder, 'scenarios')
Core_Scenario_Folder = extend(Scenario_Folder, 'core')
Scenario_Ruleset_Folder = extend(Scenario_Folder, 'rules')
Scenario_Ruleset_Standard_File = extend(Scenario_Ruleset_Folder, 'standard.rules')
# Saved_Scenario_Folder = extend(SCENARIO_FOLDER, 'saved')

# music related folders
Music_Folder = extend(Artwork_Folder, 'music')
Soundtrack_Folder = extend(Music_Folder, 'soundtrack')
Soundtrack_Playlist = extend(Soundtrack_Folder, 'playlist.info')

# graphics related folders
Graphics_Folder = extend(Artwork_Folder, 'graphics')
Graphics_UI_Folder = extend(Graphics_Folder, 'ui')
Graphics_Map_Folder = extend(Graphics_Folder, 'map')

# special locations
Manual_Index = extend(Resources_Folder, 'manual', 'index.md')
Global_Stylesheet = extend(Graphics_UI_Folder, 'style.css')

# other specific constants

# network communication
Network_Port = 42932

# minimal screen resolution
Screen_Min_Size = (1024, 768)

# options

@unique
class O(u.AutoNumberedEnum):
    VERSION = ()
        # to be displayed on the start screen
    LS_OPEN = ()
        # local server accepts outside connections
    LS_NAME = ()
    MW_BOUNDS = ()
    MW_MAXIMIZED = ()
    FULLSCREEN = ()
        # we start full screen (can be unset by the program for some linux desktop environments
    FULLSCREEN_SUPPORTED = ()
        # is full screen supported
    PHONON_SUPPORTED = ()
    BG_MUTE = ()

    def __init__(self):
        self.default = None

Options = O.__members__ # dictionary of name, Enum-value pairs

# default values for the Options
O.VERSION.default = 'v0.2.2 (2015-??-??)'
O.LS_OPEN.default = False
O.LS_NAME.default = 'server name'
O.FULLSCREEN.default = True
O.PHONON_SUPPORTED.default = True
O.BG_MUTE.default = False

# predefined channel names for network communication
CH_SCENARIO_PREVIEW = 'general.scenario.preview'
CH_CORE_SCENARIO_TITLES = 'general.core.scenarios.titles'


class TileDirections(u.AutoNumberedEnum):
    """
        Six directions for six neighbored tiles in clockwise order.
    """
    West = ()
    NorthWest = ()
    NorthEast = ()
    East = ()
    SouthEast = ()
    SouthWest = ()


class PropertyKeyNames:
    """
        Key names for general properties of a scenario.
    """

    TITLE = 'scenario.title'
    DESCRIPTION = 'scenario.description'
    MAP_COLUMNS = 'map.columns'
    MAP_ROWS = 'map.rows'
    RIVERS = 'rivers'


class NationPropertyKeyNames:
    """
        Key names for nation properties of a scenario.
    """

    COLOR = 'color'
    NAME = 'name'
    DESCRIPTION = 'description'
    CAPITAL_PROVINCE = 'capital_province'

def local_url(relative_path):
    absolute_path = os.path.abspath(relative_path)
    url = QtCore.QUrl.fromLocalFile(absolute_path)
    return url