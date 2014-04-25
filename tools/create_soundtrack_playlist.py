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

import os, json

if __name__ == '__main__':

    # create the playlist, a list of (filename, title)
    playlist = [('01 Imperialism Theme.ogg', 'Imperialism Theme'),
                ('02 Silent Ashes.ogg', 'Silent Ashes')]

    # write to data/artwork/music/soundtrack/playlist.info
    file_path = os.path.join('..', 'data', 'artwork', 'music', 'soundtrack', 'playlist.info')
    file = open(file_path, 'w')
    json.dump(playlist, file, indent=2, separators=(',', ': '))


