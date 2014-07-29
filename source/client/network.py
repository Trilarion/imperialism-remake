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

from PySide import QtCore, QtNetwork


class Client(QtCore.QObject):
    received = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        self.socket = QtNetwork.QTcpSocket(self)

    def login(self, address):
        self.socket.connectToHost(address[0], address[1])
        self.socket.readyRead.connect(self.receive)
        self.error.connect(self.error)

    def error(self):
        self.socket.disconnectFromHost()

    def receive(self):
        reader = QtCore.QDataStream(self.socket)
        message = reader.readString()
        self.received.emit(message)

    def send(self, message):
        writer = QtCore.QDataStream(self.socket)
        writer.setVersion(QtCore.QDataStream.Qt_4_8)
        writer.writeString(message)