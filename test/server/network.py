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

from PyQt5 import QtCore, QtNetwork

from base import constants as c
from server.server import ServerManager
from lib.network import ExtendedTcpServer
from base.network import Client

server = ServerManager()
server.server.start(c.NETWORK_PORT)
client = Client()
client.set_socket()

def setup():
    client.connect_to_host(c.NETWORK_PORT)
    # print('wait {}'.format(server.server.waitForNewConnection(1000)))

def send():
    message = {
        'channel': c.CH_SCENARIO_PREVIEW,
        'content': None
    }
    client.send(message)

    message = {
        'channel' : c.CH_CORE_SCENARIO_TITLES,
        'content' : 'Hi guys'
    }
    client.send(message)


app = QtCore.QCoreApplication([])

QtCore.QTimer.singleShot(100, setup)
QtCore.QTimer.singleShot(1000, send)
QtCore.QTimer.singleShot(3000, app.quit)
app.exec_()
