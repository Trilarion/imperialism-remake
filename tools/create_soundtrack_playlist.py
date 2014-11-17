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
    Generates the playlist of the soundtrack (file names and titles displayed
    in the game). Phonon cannot read metadata under Windows sometimes, see:
    http://stackoverflow.com/questions/23288557/phonon-cant-get-meta-data-of-audio-files-in-python
"""

import os

os.chdir('..')

from base import constants as c
from lib import utils as u

# create the playlist, a list of (filename, title)
playlist = [('01 Imperialism Theme.ogg', 'Imperialism Theme'),
            ('02 Silent Ashes.ogg', 'Silent Ashes')]

# write
print('write to {}'.format(c.Soundtrack_Playlist))
u.write_as_yaml(c.Soundtrack_Playlist, playlist)