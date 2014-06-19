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
    Game specific path locations for artwork, music, ...
    Only real constant constants.
"""

import os

def extend(path, *parts):
    extended = os.path.join(path, *parts)
    if not os.path.exists(extended):
        raise RuntimeError('constructed path {} does not exist'.format(extended))
    return extended

# general folder (do not directly contain data)
Data_Folder = extend('.', 'data')
Artwork_Folder = extend(Data_Folder, 'artwork')

# scenario
Scenario_Folder = extend(Data_Folder, 'scenarios')
Core_Scenario_Folder = extend(Scenario_Folder, 'core')
Saved_Scenario_Folder = extend(Scenario_Folder, 'saved')

# music related folder
Music_Folder = extend(Artwork_Folder, 'music')
Soundtrack_Folder = extend(Music_Folder, 'soundtrack')
Soundtrack_Playlist = extend(Soundtrack_Folder, 'playlist.info')

# graphics related folder
Graphics_Folder = extend(Artwork_Folder, 'graphics')
Graphics_UI_Folder = extend(Graphics_Folder, 'ui')

# special locations
Options_Default_File = extend(Data_Folder, 'options.info.default')
Manual_Index = extend(Data_Folder, 'manual', 'index.html')

# network
Network_Port = 42932