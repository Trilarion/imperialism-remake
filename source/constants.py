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

def extend(path, part):
    return os.path.join(path, part)

Data_Folder = os.path.join('.', 'data')

Soundtrack_Folder = os.path.join('.', 'data', 'artwork', 'music', 'soundtrack')
Soundtrack_Playlist = extend(Soundtrack_Folder, 'playlist.info')

Options_Default = extend(Data_Folder, 'options.info.default')


