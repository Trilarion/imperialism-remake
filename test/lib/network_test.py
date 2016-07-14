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

'''

'''

import datetime
import PyQt5.QtCore as QtCore
import lib.network as network

PORT = 37846

def now():
    return datetime.datetime.now().strftime('%H:%M:%S,%f')

def log(message):
    print('{}  {}'.format(now(), message))

def client_connected():
    log('client connected')

def client_disconnected():
    log('client disconnected')

def client_connect():
    log('client tries to connect')
    client.connect_to_host(PORT)

def server_start():
    log('server tries to start')
    server.start(PORT)

app = QtCore.QCoreApplication([])

client = network.ExtendedTcpSocket()
client.connected.connect(client_connected)
client.disconnected.connect(client_disconnected)

server = network.ExtendedTcpServer()

# actions
QtCore.QTimer.singleShot(100, server_start)
QtCore.QTimer.singleShot(200, client_connect)
QtCore.QTimer.singleShot(5000, app.quit)

app.exec_()