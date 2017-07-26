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

import sys, os
import datetime

from PyQt5 import QtCore

from imperialism_remake.lib import network

PORT = 37846

def now():
    """
        Return current time, including fractions of seconds.
    """
    return datetime.datetime.now().strftime('%H:%M:%S,%f')

def log(message):
    """
        Print a log message including the current time.
    """
    print('{}  {}'.format(now(), message))

def client_connected():
    """
        Client has connected.
    """
    log('client connected')

def client_disconnected():
    """
        Client has been disconnected.
    """
    log('client disconnected')

def client_connect():
    """
        Action, client tries to connect.
    """
    log('client tries to connect')
    client.connect_to_host(PORT)

def client_sends_something():
    """
        Action, client tries to send something.
    """
    log('client tries to send something')
    client.send({'cat': [1, 2, 3]})

def client_received(message):
    """
        Client received a message
    """
    log('client received message: {}'.format(message))

def server_start():
    """
        Action, server tries to start.
    """
    log('server tries to start')
    server.start(PORT)

def server_stop():
    """
        Action, server tries to stop.
    """
    log('server tries to stop')
    server.stop()

sclient = None # server client

def server_new_client(client):
    """
        New client connected to server.
    """
    global sclient
    sclient = network.ExtendedTcpSocket(client)
    sclient.received.connect(sclient_received)
    sclient.error.connect(print)
    log('server has new connection')

def sclient_received(message):
    """
        Connected server client received something.
    """
    log('server-client received message: {}'.format(message))

def server_client_sends_something():
    """
        Action, server client tries to send something
    """
    log('server-client tries to send something')
    sclient.send([1, 2, 'Three'])

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    app = QtCore.QCoreApplication([])

    # create client
    client = network.ExtendedTcpSocket()
    client.connected.connect(client_connected)
    client.disconnected.connect(client_disconnected)
    client.received.connect(client_received)
    client.error.connect(print)

    server = network.ExtendedTcpServer()
    server.new_client.connect(server_new_client)

    # actions
    # server stars and client connected
    QtCore.QTimer.singleShot(100, server_start)
    QtCore.QTimer.singleShot(200, client_connect)
    # they exchange messages
    QtCore.QTimer.singleShot(1000, client_sends_something)
    QtCore.QTimer.singleShot(1100, server_client_sends_something)
    # server stops, should disconnect the client
    QtCore.QTimer.singleShot(4500, server_stop)
    # quit the app
    QtCore.QTimer.singleShot(5000, app.quit)

    app.exec_()