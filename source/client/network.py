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

from lib.network import *

class Client(QtCore.QObject):
    """
        Mostly a wrapper around QtNetwork.QTcpSocket and QDataStream to allow reading and writing of strings (messages).
    """
    received = QtCore.Signal(dict)

    def __init__(self):
        """
            Create a socket.
        """
        super().__init__()
        self.socket = QtNetwork.QTcpSocket(self)
        # some clients
        self.socket.readyRead.connect(self.receive)
        self.socket.disconnected.connect(self.disconnected)
        self.socket.error.connect(self.error)

    def login(self, host, port):
        """
            Given an address (list of two parts: hostname (str), port (int)) tries to connect the socket.
        """
        self.socket.connectToHost(host, port)

    def disconnected(self):
        print('client disconnected')

    def error(self):
        """
            Something went wrong. We should disconnect immediately.
        """
        print('error will disconnect')
        self.socket.disconnectFromHost()

    def receive(self):
        """
            A new mesage came, read the message as string.

            TODO will the whole message arrive in one piece?
        """
        while self.socket.bytesAvailable() > 0:
            value = read_from_socket_uncompress_and_deserialize(self.socket)
            print('client received {}'.format(json.dumps(value)))
            self.received.emit(value)

    def send(self, value):
        """
            Sends a message (a astring) over the socket.

            TODO check if connected before, error if not
        """
        serialize_compress_and_write_to_socket(self.socket, value)

client = Client()
