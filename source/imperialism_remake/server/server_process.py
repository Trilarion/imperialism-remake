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
import logging.handlers
import multiprocessing
import os

from PyQt5 import QtCore

from imperialism_remake.lib import qt
from imperialism_remake.server.server_manager import ServerManager

logger = logging.getLogger(__name__)


# TODO start this in its own process
# TODO wait for a name but only change it once during a session


class ServerProcess(multiprocessing.Process):
    """
    A Process that inside its run method executes a QCoreApplication which runs the server.
    """

    def __init__(self, log_queue, log_formatter, log_level):
        super().__init__()
        self._log_queue = log_queue
        self._log_formatter = log_formatter
        self._log_level = log_level

    def run(self):
        """
        Runs the server process by starting its own QCoreApplication.
        """
        self._configure_forked_logger()

        qt.fix_pyqt5_exception_eating()

        app = QtCore.QCoreApplication([])

        # server manager, signal shutdown stops the app
        server_manager = ServerManager()
        server_manager.shutdown.connect(app.quit)
        # noinspection PyCallByClass
        QtCore.QTimer.singleShot(100, server_manager.start)

        # run event loop of app
        app.exec_()

    def _configure_forked_logger(self):
        """ create a new logging handler that will inject its records into a queue

        The listener of this queue runs in the main process (that opened the log files and stdout)
        as a thread and will output all incoming log records via its configured handlers.
        """
        log_queue_handler = logging.handlers.QueueHandler(self._log_queue)
        log_queue_handler.setFormatter(self._log_formatter)
        root = logging.getLogger()
        root.setLevel(self._log_level)
        # remove all possibly inherited handlers - we only need our new queue logger
        for handler in root.handlers:
            root.removeHandler(handler)
        root.addHandler(log_queue_handler)
        logger = logging.getLogger(__name__)
        logger.info("created a multiprocess logger (pid=%d)", os.getpid())
