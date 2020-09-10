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

import os, sys

from PyQt5 import QtCore

import imperialism_remake.server.server_manager


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

    # add source directory to path if needed
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    from imperialism_remake.base import constants, network as base_network
    from imperialism_remake.server import server_process

    app = QtCore.QCoreApplication([])

    server_manager = imperialism_remake.server.server_manager.ServerManager()
    client = base_network.NetworkClient()

    # actions
    QtCore.QTimer.singleShot(0, server_manager.start)
    QtCore.QTimer.singleShot(100, client_connect)
    QtCore.QTimer.singleShot(1000, send)
    QtCore.QTimer.singleShot(3000, app.quit)

    app.exec_()
