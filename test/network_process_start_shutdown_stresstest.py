# Imperialism remake
# Copyright (C) 2016 Trilarion
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
Examples for base.network and server.network using ServerProcess
"""

from PyQt5 import QtCore
from imperialism_remake import start
from imperialism_remake.base import constants, network as base_network
from imperialism_remake.server import server

def client_connect():
    """
    Client tries to connect.
    """
    client.connect_to_host(constants.NETWORK_PORT)

def send_shutdown():
    """
    Send shutdown message.
    """
    client.send(constants.C.SYSTEM, constants.M.SYSTEM_SHUTDOWN)
    client.socket.flush()

if __name__ == '__main__':
    start.fix_pyqt5_exception_eating()
    start.set_start_directory()

    # create server process and start it
    server_process = server.ServerProcess()
    server_process.start()

    # create app in this process
    app = QtCore.QCoreApplication([])

    client = base_network.NetworkClient()

    # actions
    QtCore.QTimer.singleShot(100, client_connect)
    QtCore.QTimer.singleShot(200, send_shutdown)
    QtCore.QTimer.singleShot(300, app.quit)

    app.exec_()

    # wait for server
    server_process.join()
