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

import random
from functools import partial
from PySide import QtCore, QtNetwork

class Server(QtCore.QObject):

    def __init__(self, address):
        super().__init__()
        self.address = address
        self.server = QtNetwork.QTcpServer(self)
        self.server.newConnection.connect(self.new_connection)
        self.connections = {}

    def create_id(self):
        while True:
            id = random.randint(0, 1e6)
            if id not in self.connections:
                return id

    def start(self):
        if not self.server.listen(self.address[0], self.address[1]):
            raise RuntimeError('Network error: cannot listen')

    def stop(self):
        if self.server.isListening():
            self.server.close()

    def new_connection(self):
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
        pass

    def error(self, socket):
        socket.disconnectFromHost()

    def receive(self, id):
        socket = self.connections[id]
        reader = QtCore.QDataStream(socket)
        message = reader.readString()

    def send(self, id, message):
        socket = self.connections[id]
        writer = QtCore.QDataStream(socket)
        writer.setVersion(QtCore.QDataStream.Qt_4_8)
        writer.writeString(message)