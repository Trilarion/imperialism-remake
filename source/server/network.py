# Imperialism remake
# Copyright (C) 2014 Trilarion
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

import random
from functools import partial

from PySide import QtCore, QtNetwork


class Server(QtCore.QObject):
    """
        Wrapper around QtNetwork.QTcpServer and a management of several connections (each a QtNetwork.QTcpSocket).
    """

    def __init__(self):
        """
        """
        super().__init__()
        self.server = QtNetwork.QTcpServer(self)
        self.server.newConnection.connect(self.new_connection)
        self.connections = {}

    def create_id(self):
        """
            Creates a new random id in the range of 0 to 1e6.
        """
        while True:
            # theoretically this could take forever, practically only if we have 1e6 connections already
            id = random.randint(0, 1e6)
            if id not in self.connections:
                return id

    def start(self, address):
        """
            Given an address (hostname, port) tries to start listening.
        """
        if not self.server.listen(address[0], address[1]):
            raise RuntimeError('Network error: cannot listen')

    def stop(self):
        """
            Stopps listening.
        """
        if self.server.isListening():
            self.server.close()

    def new_connection(self):
        """
            Zero or more new connections might be available, give them an id and wire them.
        """
        while self.server.hasPendingConnections():
            socket = self.server.nextPendingConnection()
            # get id
            id = self.create_id()
            self.connections[id] = socket
            # connect
            socket.disconnected.connect(partial(self.disconnected, id))
            socket.readyRead.connect(partial(self.receive, id))
            socket.error.connect(partial(self.error, id))

    def disconnected(self, socket):
        """
            One connection disconnected.
        """
        pass

    def error(self, socket):
        """
            An error occured with a connection, disconnect it.
        """
        socket.disconnectFromHost()

    def receive(self, id):
        """
            A certain connection (identified by its id) wants to send us something.
        """
        socket = self.connections[id]
        reader = QtCore.QDataStream(socket)
        message = reader.readString()

    def send(self, id, message):
        """
            We send a message to a certain connection (identified by its id).
        """
        socket = self.connections[id]
        writer = QtCore.QDataStream(socket)
        writer.setVersion(QtCore.QDataStream.Qt_4_8)
        writer.writeString(message)