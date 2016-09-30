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
    Examples for usages of ExtendedTcpSocket and ExtendedTcpServer from lib.network
"""

import sys
import datetime
import PyQt5.QtCore as QtCore
import lib.network as network

def exception_hook(type, value, tback):
    """
        PyQt5 by default eats exceptions (see http://stackoverflow.com/q/14493081/1536976)
    """
    sys.__excepthook__(type, value, tback)

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

def client_sends_something():
    log('client tries to send something')
    client.send({'cat': [1, 2, 3]})

def client_received(message):
    log('client received message: {}'.format(message))

def server_start():
    log('server tries to start')
    server.start(PORT)

def server_stop():
    log('server tries to stop')
    server.stop()

sclient = None
def server_new_client(client):
    global sclient
    sclient = network.ExtendedTcpSocket(client)
    sclient.received.connect(sclient_received)
    log('server has new connection')

def sclient_received(message):
    log('server-client received message: {}'.format(message))

def server_client_sends_something():
    log('server-client tries to send something')
    sclient.send([1, 2, 'Three'])

if __name__ == '__main__':

    sys.excepthook = exception_hook

    app = QtCore.QCoreApplication([])

    client = network.ExtendedTcpSocket()
    client.connected.connect(client_connected)
    client.disconnected.connect(client_disconnected)
    client.received.connect(client_received)

    server = network.ExtendedTcpServer()
    server.new_client.connect(server_new_client)

    # actions
    QtCore.QTimer.singleShot(100, server_start)
    QtCore.QTimer.singleShot(200, client_connect)
    QtCore.QTimer.singleShot(1000, client_sends_something)
    QtCore.QTimer.singleShot(1100, server_client_sends_something)
    QtCore.QTimer.singleShot(4500, server_stop)
    QtCore.QTimer.singleShot(5000, app.quit)

    app.exec_()