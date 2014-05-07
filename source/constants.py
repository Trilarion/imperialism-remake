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

import os, sys, codecs, shutil
import tools

Debug_Mode = True

def extend(path, *parts):
    extended = os.path.join(path, *parts)
    if not os.path.exists(extended):
        raise RuntimeError('constructed path {} does not exist'.format(extended))
    return extended

# general folder (do not directly contain data)
Data_Folder = os.path.join('.', 'data')
Artwork_Folder = extend(Data_Folder, 'artwork')

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

# determine home dir
folder = 'Imperialism Remake'
if os.name == 'posix':
    # Linux / Unix
    User_Folder = os.path.join(os.getenv('HOME'), folder)
elif (os.name == 'nt') and (os.getenv('USERPROFILE') is not None):
    # MS Windows
    User_Folder = os.path.join(os.getenv('USERPROFILE'), folder)
else:
    User_Folder = '..'

# if not exists, create home dir
if not os.path.isdir(User_Folder):
    os.mkdir(User_Folder)

# redirect output to log files (will be overwritten each time)
Log_File = os.path.join(User_Folder, 'remake.log')
Error_File = os.path.join(User_Folder, 'remake.error.log')
if not Debug_Mode:
    sys.stdout = codecs.open(Log_File, encoding='utf-8', mode='w')
    sys.stderr = codecs.open(Error_File, encoding='utf-8', mode='w')

# search for existing options file, load it
Options_File = os.path.join(User_Folder, 'options.info')
if not os.path.exists(Options_File):
    shutil.copyfile(Options_Default_File, Options_File)
tools.options.load()

tools.log_info('options loaded from user folder ({})'.format(User_Folder))