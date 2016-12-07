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
Starts the application (a client and a server).
Start in project root folder and with 'debug' as parameter if wished.
"""

import os
import sys

def exception_hook(type, value, traceback):
    """
    Use sys.__excepthook__, the standard hook.
    """
    sys.__excepthook__(type, value, traceback)

def fix_pyqt5_exception_eating():
    """
    PyQt5 by default eats exceptions (see http://stackoverflow.com/q/14493081/1536976)
    """
    sys.excepthook = exception_hook

def set_start_directory():
    """
        If the start directory is above the ./data directory we go down (up to three levels) and search for a data
        folder, then set it as current directory.
    """
    base_path = '.'
    counter = 0
    while True:
        path = os.path.join(base_path, 'data')
        if os.path.isdir(path):
            print('home: {}'.format(base_path))
            os.chdir(base_path)
            break
        counter += 1
        if counter > 3:
            raise RuntimeError('Cannot find home directory (containing the data folder)')
        base_path = os.path.join(base_path, '..')



def main():
    """
    Main entry point. Called from the script generated in setup.py and called when running this module with python.
    """
    # test for python version
    required_version = (3, 5)
    if sys.version_info < required_version:
        raise RuntimeError('Python version must be {}.{} at least.'.format(*required_version))

    # test for existence of PyQt5
    try:
        from PyQt5 import QtCore
    except ImportError:
        raise RuntimeError('PyQt5 must be installed.')

    # fix PyQt5 exception eating
    fix_pyqt5_exception_eating()

    # set start directory
    set_start_directory()

    # determine user folder
    if os.name == 'posix':
        # Linux / Unix
        user_folder = os.path.join(os.getenv('HOME'), 'Imperialism Remake User Data')
    if (os.name == 'nt') and (os.getenv('USERPROFILE') is not None):
        # MS Windows
        user_folder = os.path.join(os.getenv('USERPROFILE'), 'Imperialism Remake User Data')
    else:
        user_folder = 'User Data'
    print('user data stored in: {}'.format(user_folder))

    # if not exist, create user folder
    if not os.path.isdir(user_folder):
        os.mkdir(user_folder)

    # determine DEBUG_MODE from runtime arguments
    from imperialism_remake.base import switches

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        switches.DEBUG_MODE = True
    if switches.DEBUG_MODE:
        print('debug mode is on')

    # redirect output to log files (will be overwritten at each start)
    Log_File = os.path.join(user_folder, 'remake.log')
    Error_File = os.path.join(user_folder, 'remake.error.log')
    # in debug mode print to the console instead
    if not switches.DEBUG_MODE:
        import codecs

        sys.stdout = codecs.open(Log_File, encoding='utf-8', mode='w')
        sys.stderr = codecs.open(Error_File, encoding='utf-8', mode='w')

    # import some base libraries
    import imperialism_remake.base.tools as tools

    # search for existing options file, if not existing, save it once (should just save an empty dictionary)
    Options_File = os.path.join(user_folder, 'options.info')
    if not os.path.exists(Options_File):
        tools.save_options(Options_File)

    # create single options object, load options and send a log message
    tools.load_options(Options_File)
    tools.log_info('options loaded from user folder ({})'.format(user_folder))

    # special case of some desktop environments under Linux where full screen mode does not work well
    from imperialism_remake.base import constants

    # full screen support
    if tools.get_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED):
        session = os.environ.get("DESKTOP_SESSION")
        if session and (session.startswith('ubuntu') or 'xfce' in session or session.startswith('xubuntu') or 'gnome' in session):
            tools.set_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED, False)
            tools.log_warning('Desktop environment {} has problems with full screen mode. Will turn if off.'.format(session))
    # we cannot have full screen without support
    if not tools.get_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED):
        tools.set_option(constants.Option.MAINWINDOW_FULLSCREEN, False)

    # now we can safely assume that the environment is good to us

    # start server
    import multiprocessing

    # multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    from imperialism_remake.server.server import ServerProcess

    server_process = ServerProcess()
    server_process.start()

    # start client, we will return when the program finishes
    from imperialism_remake.client.client import start_client

    start_client()

    # wait for server
    server_process.join()

    # save options
    tools.save_options(Options_File)
    tools.log_info('options saved')

    # report on unused resources
    if switches.DEBUG_MODE:
        tools.find_unused_resources()

    # good bye message
    tools.log_info('will exit soon - good bye')

if __name__ == '__main__':
    main()