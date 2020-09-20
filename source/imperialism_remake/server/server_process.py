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
Server network code. Only deals with the network connection, client connection management and message distribution.
"""
import logging
import logging.config
import multiprocessing
import os

from PyQt5 import QtCore

from imperialism_remake.lib import qt
from imperialism_remake.server import server_config_log
from imperialism_remake.server.server_manager import ServerManager

logger = logging.getLogger(__name__)


# TODO wait for a name but only change it once during a session


class ServerProcess(multiprocessing.Process):
    """
    A Process that inside its run method executes a QCoreApplication which runs the server.
    """

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Runs the server process by starting its own QCoreApplication.
        """
        logging.config.dictConfig(server_config_log.LOG_CONFIG)

        qt.fix_pyqt5_exception_eating()

        app = QtCore.QCoreApplication([])

        # server manager, signal shutdown stops the app
        server_manager = ServerManager()
        server_manager.shutdown.connect(app.quit)
        # noinspection PyCallByClass
        QtCore.QTimer.singleShot(100, server_manager.start)

        logger.info("Server process is started (pid=%d)", os.getpid())

        # run event loop of app
        app.exec_()
