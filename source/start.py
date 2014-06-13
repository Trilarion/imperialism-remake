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
    Start the application.

    Start in project root folder and with 'debug' as script parameter is wished.
"""

if __name__ == '__main__':

    import sys

    # test for python version
    if sys.version_info < (3, 3):
        raise RuntimeError('Python version must be 3.3 at least.')

    # test for existence of PySide
    try:
        from PySide import QtCore
    except ImportError:
        raise RuntimeError('PySide must be installed.')

    import os, codecs, shutil
    import constants as c, tools as t

    # determine Debug_Mode from runtime arguments
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        Debug_Mode = True
        print('debug mode on')
    else:
        Debug_Mode = False

    # determine home dir
    if os.name == 'posix':
        # Linux / Unix
        User_Folder = os.path.join(os.getenv('HOME'), 'Imperialism Remake User Data')
    if (os.name == 'nt') and (os.getenv('USERPROFILE') is not None):
        # MS Windows
        User_Folder = os.path.join(os.getenv('USERPROFILE'), 'Imperialism Remake User Data')
    else:
        User_Folder = 'User Data'
    print('user data stored in: {}'.format(User_Folder))

    # if not exist, create user folder
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
        shutil.copyfile(c.Options_Default_File, Options_File)

    # create the single options object, load options and send the first log message
    t.options = t.Options()
    t.options.load(Options_File)
    t.log_info('options loaded from user folder ({})'.format(User_Folder))

    # test for phonon availability
    try:
        from PySide.phonon import Phonon
    except ImportError:
        t.log_error('Phonon backend not available, no sound.')
        # TODO set mute in options

    # now we can safely assume that the environment is good to us
    # and we simply start the client
    from client import client
    client.start()

    # save options
    t.options.save(Options_File)
    t.log_info('options saved')

    # finished
    t.log_info('will exit soon - good bye')
