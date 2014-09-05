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
    Client network code
"""

from PySide import QtCore, QtNetwork


class Client(QtCore.QObject):
    """
        Mostly a wrapper around QtNetwork.QTcpSocket and QDataStream to allow reading and writing of strings (messages).
    """
    received = QtCore.Signal(str)

    def __init__(self):
        """
            Create a socket.
        """
        super().__init__()
        self.socket = QtNetwork.QTcpSocket(self)
        # some connections
        self.socket.readyRead.connect(self.receive)
        self.error.connect(self.error)

    def login(self, address):
        """
            Given an address (list of two parts: hostname (str), port (int)) tries to connect the socket.
        """
        self.socket.connectToHost(address[0], address[1])

    def error(self):
        """
            Something went wrong. We should disconnect immediately.
        """
        self.socket.disconnectFromHost()

    def receive(self):
        """
            A new mesage came, read the message as string.

            TODO will the whole message arrive in one piece?
        """
        reader = QtCore.QDataStream(self.socket)
        message = reader.readString()
        self.received.emit(message)

    def send(self, message):
        """
            Sends a message (a astring) over the socket.

            TODO check if connected before, error if not
        """
        writer = QtCore.QDataStream(self.socket)
        writer.setVersion(QtCore.QDataStream.Qt_4_8)
        writer.writeString(message)