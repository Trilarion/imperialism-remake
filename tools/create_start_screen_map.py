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
Generates the hot image areas map of the start screen.
"""

import os, sys

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    from imperialism_remake.lib import utils
    from imperialism_remake.base import constants

    # hot areas map
    map = {'exit': {
        'overlay': 'start.overlay.door.right.png',
        'offset': [575, 412],
        'label': 'Exit'
    }, 'help': {
        'overlay': 'start.overlay.window.left.png',
        'offset': [127, 397],
        'label': 'Help'
    }, 'lobby': {
        'overlay': 'start.overlay.throne.png',
        'offset': [421, 459],
        'label': 'Game Lobby'
    }, 'editor': {
        'overlay': 'start.overlay.map.png',
        'offset': [821, 60],
        'label': 'Scenario Editor'
    }, 'options': {
        'overlay': 'start.overlay.fireplace.png',
        'offset': [832, 505],
        'label': 'Preferences'
    }}

    # exit

    # help browser

    # game lobby

    # editor

    # options

    # write
    file_name = os.path.join(constants.GRAPHICS_UI_FOLDER, 'start.overlay.info')
    print('write to {}'.format(file_name))
    utils.write_to_file(file_name, map)