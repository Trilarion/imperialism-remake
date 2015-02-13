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

import os

from lib import utils as u
from base import constants as c

"""
    Generates the hot image areas map of the start screen.
"""

os.chdir('..')

# hot areas map
map = {}

# exit
map['exit'] = {
    'overlay': 'start.overlay.door.right.png',
    'offset': [575, 412],
    'label': 'Exit'
}

# help browser
map['help'] = {
    'overlay': 'start.overlay.window.left.png',
    'offset': [127, 397],
    'label': 'Help'
}

# game lobby
map['lobby'] = {
    'overlay': 'start.overlay.throne.png',
    'offset': [421, 459],
    'label': 'Game Lobby'
}

# editor
map['editor'] = {
    'overlay': 'start.overlay.map.png',
    'offset': [821, 60],
    'label': 'Scenario Editor'
}

# options
map['options'] = {
    'overlay': 'start.overlay.fireplace.png',
    'offset': [832, 505],
    'label': 'Preferences'
}

# write
file_name = os.path.join(c.Graphics_UI_Folder, 'start.overlay.info')
print('write to {}'.format(file_name))
u.write_as_yaml(file_name, map)