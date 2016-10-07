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

import sys

from PyQt5 import QtCore

def client_connect():
    """
        Client tries to connect.
    """
    client.connect_to_host(constants.NETWORK_PORT)

def send():
    """
        Client sends two messages.
    """
    message = {
        'channel': constants.CH_SCENARIO_PREVIEW,
        'content': None
    }
    client.send(message)

    message = {
        'channel' : constants.CH_CORE_SCENARIO_TITLES,
        'content' : 'Hi guys'
    }
    client.send(message)

if __name__ == '__main__':

    import imperialism_remake

    sys.excepthook = imperialism_remake.exception_hook
    imperialism_remake.set_start_directory()

    from base import constants, network
    from server.server import ServerManager

    app = QtCore.QCoreApplication([])

    server_manager = ServerManager()
    client = network.NetworkClient()

    # actions
    QtCore.QTimer.singleShot(0, server_manager.start)
    QtCore.QTimer.singleShot(100, client_connect)
    QtCore.QTimer.singleShot(1000, send)
    QtCore.QTimer.singleShot(3000, app.quit)

    app.exec_()
