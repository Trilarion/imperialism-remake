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
Examples for base.network and server.network
"""

from PyQt5 import QtCore

import imperialism_remake
from base import constants, network
from server.server import ServerManager

def client_connect():
    """
    Client tries to connect.
    """
    client.connect_to_host(constants.NETWORK_PORT)

def send():
    """
    Client sends a message.
    """
    client.connect_to_channel(constants.C.LOBBY, receive)
    client.send(constants.C.LOBBY, constants.M.LOBBY_SCENARIO_CORE_LIST)

def receive(client, channel, action, content):
    """
    Receives the answer.
    """
    client.disconnect_from_channel(channel, receive)
    print('received on channel {} with action {} and content {}'.format(channel, action, content))


if __name__ == '__main__':
    imperialism_remake.fix_pyqt5_exception_eating()
    imperialism_remake.set_start_directory()

    app = QtCore.QCoreApplication([])

    server_manager = ServerManager()
    client = network.NetworkClient()

    # actions
    QtCore.QTimer.singleShot(0, server_manager.start)
    QtCore.QTimer.singleShot(100, client_connect)
    QtCore.QTimer.singleShot(1000, send)
    QtCore.QTimer.singleShot(3000, app.quit)

    app.exec_()
