#!/usr/bin/env python3
#
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
import multiprocessing
import os
import sys

APPLICATION_NAME = 'imperialism_remake'


def get_arguments():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser(prog=APPLICATION_NAME)
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='enable detailed debug logging')
    return parser.parse_args()


def main():
    """
    Main entry point. Called from the script generated in setup.py and called when running this module with python.
    """

    # TODO freeze_support might be needed for windows
    # (https://docs.python.org/3.6/library/multiprocessing.html#multiprocessing.freeze_support)
    # check if this is still the case, we are using pynsist (https://github.com/takluyver/pynsist)
    # for packaging on Windows
    # multiprocessing.freeze_support()
    # probably not with pynsist because it ships a full featured Python

    # guidelines at https://docs.python.org/3.6/library/multiprocessing.html#programming-guidelines
    multiprocessing.set_start_method('spawn')

    # test for minimal supported python version (3.5)
    required_version = (3, 5)
    if sys.version_info < required_version:
        raise RuntimeError('Python version must be {}.{} at least.'.format(*required_version))

    # test for existence of PyQt5
    try:
        from PyQt5 import QtCore  # noqa: F401
    except ImportError:
        raise RuntimeError('PyQt5 must be installed.')

    # test for minimal supported Qt version (5.5)
    if QtCore.QT_VERSION < 0x50500:
        raise RuntimeError('Qt version of PyQt5 must be 5.5 at least.')

    # Add the parent directory of the package directory to Python's search path.
    # This allows the import of the 'imperialism_remake' modules.
    # This is required at least for Linux distributions of Python3, since the current working
    # directory is not part of Python's search path by default.
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    # import imperialism remake modules
    from imperialism_remake.lib import qt
    from imperialism_remake.base import constants, tools

    # fix PyQt5 exception eating
    qt.fix_pyqt5_exception_eating()

    # user folder
    user_folder = constants.get_user_directory()

    # if not existing, create user folder
    if not os.path.isdir(user_folder):
        os.mkdir(user_folder)

    # determine DEBUG_MODE from runtime arguments
    from imperialism_remake.base import switches
    args = get_arguments()
    switches.DEBUG_MODE = args.debug
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if switches.DEBUG_MODE else logging.INFO)

    logger.info('user data stored in: {}'.format(user_folder))

    # search for existing options file, if not existing, save it once (should just save an empty dictionary)
    options_file = os.path.join(user_folder, 'options.info')
    if not os.path.exists(options_file):
        tools.save_options(options_file)

    # create single options object, load options and send a log message
    tools.load_options(options_file)
    logger.info('options loaded from user folder (%s)', user_folder)

    # fix options: special case of some desktop environments under Linux where full screen mode does not work well

    # full screen support
    if tools.get_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED):
        session = os.environ.get("DESKTOP_SESSION")
        # TODO: what exactly is the problem and how can we detect it (without guessing)?
        if (session and (session.startswith('ubuntu')
                         or ('xfce' in session)
                         or session.startswith('xubuntu')
                         or ('gnome' in session))):
            tools.set_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED, False)
            logger.warning('Desktop environment %s has problems with full screen mode. Will turn if off.', session)

    # options constraint: we cannot have full screen without support
    if not tools.get_option(constants.Option.MAINWINDOW_FULLSCREEN_SUPPORTED):
        tools.set_option(constants.Option.MAINWINDOW_FULLSCREEN, False)

    # start server
    from imperialism_remake.server.server_process import ServerProcess

    server_process = ServerProcess()
    server_process.start()

    logger.info('server process started (%s)', server_process.pid)

    # start client, we will return when the client finishes
    from imperialism_remake.client.client.client import start_client
    start_client()

    logger.info('client started')

    # wait for server process to stop
    server_process.join()

    # save options
    tools.save_options(options_file)
    logger.info('options saved to file %s', options_file)

    # report on unused resources
    if switches.DEBUG_MODE:
        tools.find_unused_resources()

    # good bye message and shutdown logger
    logger.info('will exit soon - good bye')


if __name__ == '__main__':
    main()
