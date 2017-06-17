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
Start in project root folder and with '--debug' as parameter if wished.
"""

import argparse
import logging
import os
import sys


APPLICATION_NAME = 'imperialism_remake'


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
    Just take current package.
    """
    package_path = os.path.dirname(__file__)
    print(package_path)
    os.chdir(package_path)


def get_arguments():
    parser = argparse.ArgumentParser(prog=APPLICATION_NAME)
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='enable detailed debug logging')
    return parser.parse_args()


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

    # Add the parent directory of the package directory to Python's search path.
    # This allows the import of the 'imperialism_remake' modules.
    # This is required at least for Linux distributions of Python3, since the current working
    # directory is not part of Python's search path by default.
    sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

    # set start directory
    set_start_directory()

    # determine user folder
    if os.name == 'posix':
        # Linux / Unix
        # see 'XDG_CONFIG_HOME' in https://specifications.freedesktop.org/basedir-spec/
        config_basedir = os.getenv('XDG_CONFIG_HOME',
                                   os.path.join(os.path.expanduser('~'), '.config'))
        user_folder = os.path.join(config_basedir, APPLICATION_NAME)
    elif (os.name == 'nt') and (os.getenv('USERPROFILE') is not None):
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

    args = get_arguments()
    log_level = logging.DEBUG if args.debug else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_console_handler = logging.StreamHandler()
    log_console_handler.setFormatter(log_formatter)
    logger.addHandler(log_console_handler)
    switches.DEBUG_MODE = args.debug
    if switches.DEBUG_MODE:
        logger.info('debug mode is on')

    # redirect output to log files (will be overwritten at each start)
    log_filename = os.path.join(user_folder, 'remake.log')
    log_details_handler = logging.FileHandler(log_filename, mode='w', encoding='utf-8')
    log_details_handler.setFormatter(log_formatter)
    logger.addHandler(log_details_handler)
    logger.info('writing detailed log messages to %s', log_filename)

    error_filename = os.path.join(user_folder, 'remake.error.log')
    log_error_handler = logging.FileHandler(error_filename, mode='w', encoding='utf-8')
    log_error_handler.setFormatter(log_formatter)
    log_error_handler.setLevel(logging.ERROR)
    logger.addHandler(log_error_handler)
    logger.info('writing error log messages to %s', error_filename)

    # import some base libraries
    import imperialism_remake.base.tools as tools

    # search for existing options file, if not existing, save it once (should just save an empty dictionary)
    Options_File = os.path.join(user_folder, 'options.info')
    if not os.path.exists(Options_File):
        tools.save_options(Options_File)

    # create single options object, load options and send a log message
    tools.load_options(Options_File)
    logger.info('options loaded from user folder (%s)', user_folder)

    # special case of some desktop environments under Linux where full screen mode does not work well
    from imperialism_remake.base import constants

    # full screen support
    if tools.get_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED):
        session = os.environ.get("DESKTOP_SESSION")
        if session and (session.startswith('ubuntu') or 'xfce' in session or session.startswith('xubuntu') or 'gnome' in session):
            tools.set_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED, False)
            logger.warning('Desktop environment %s has problems with full screen mode. Will turn if off.', session)
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
    logger.info('options saved to file %s', Options_File)

    # report on unused resources
    if switches.DEBUG_MODE:
        tools.find_unused_resources()

    # good bye message
    logger.info('will exit soon - good bye')

if __name__ == '__main__':
    main()
