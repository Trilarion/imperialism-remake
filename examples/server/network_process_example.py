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

import sys

import PyQt5.QtCore as QtCore

import imperialism_remake
import base.constants as constants
import base.network as network
import server.server as server

def client_connect():
    """
        Client tries to connect.
    """
    client.connect_to_host(constants.NETWORK_PORT)

def send():
    """
        Client sends two messages.
    """
    client.send(constants.CH_SCENARIO_PREVIEW)
    client.send(constants.CH_CORE_SCENARIO_TITLES, 'Hi guiys')

def send_shutdown():
    client.send(constants.CH_SYSTEM, 'shutdown')

if __name__ == '__main__':

    # because PyQt5 eats exceptions in the event thread this workaround
    sys.excepthook = imperialism_remake.exception_hook

    # create server process and start it
    server_process = server.ServerProcess()
    server_process.start()

    # create app in this process
    app = QtCore.QCoreApplication([])

    client = network.NetworkClient()

    # actions
    QtCore.QTimer.singleShot(100, client_connect)
    #QtCore.QTimer.singleShot(1000, send)
    QtCore.QTimer.singleShot(2000, send_shutdown)
    QtCore.QTimer.singleShot(3000, app.quit)

    app.exec_()
    print('client app has quit')

    # wait for server
    server_process.join()
