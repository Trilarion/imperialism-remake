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

import zlib
import yaml

from PySide import QtCore, QtNetwork

SCOPE = {
    'local': QtNetwork.QHostAddress.LocalHost,
    'any': QtNetwork.QHostAddress.Any
}

class Client(QtCore.QObject):
    """

    """
    connected = QtCore.Signal()
    disconnected = QtCore.Signal()
    error = QtCore.Signal(QtNetwork.QAbstractSocket.SocketError)
    received = QtCore.Signal(object)

    def __init__(self):
        """

        """
        super().__init__()
        self.socket = None
        self.bytes_written = 0
        #print('new connection id {}, address {}, port {}'.format(id, socket.peerAddress().toString(), socket.peerPort()))

    def set_socket(self, socket=None):
        if self.socket is not None:
            raise RuntimeError('Socket already set!')
        if socket is None:
            socket = QtNetwork.QTcpSocket()
        self.socket = socket
        # self.socket.setParent(self)
        self.socket.readyRead.connect(self.receive)
        self.socket.error.connect(self.error)
        self.socket.connected.connect(self.connected)
        self.socket.disconnected.connect(self.disconnected)
        self.socket.bytesWritten.connect(self.count_bytes_written)

    def disconnectFromHost(self):
        self.socket.disconnectFromHost()

    def connectToHost(self, port, host='local'):
        if host is 'local':
            host = SCOPE['local']
        self.socket.connectToHost(host, port)

    def receive(self):
        """
            While there are messages available read them and process them.
            Reading is reading of a QByteArray from the TCPSocket, uncompressing and deserializing.
        """
        while self.socket.bytesAvailable() > 0:
            # read a QByteArray using a data stream
            reader = QtCore.QDataStream(self.socket)
            bytearray = QtCore.QByteArray()
            reader >> bytearray

            # uncompress bytes from bytearray
            uncompressed = zlib.decompress(bytearray.data())

            # security validator (check for everything that we do not like (!!python)
            # TODO implement this

            # decode from utf-8 bytes to unicode and deserialize from yaml
            value = yaml.load(uncompressed.decode())

            print('connection id {} received {}'.format(self.id, value))
            self.received.emit(value)

    def send(self, value):
        """
            We send a message back to the client.
            We do it by serialization, compressing and writing of a QByteArray to the TCPSocket.
        """
        # serialize value to yaml
        serialized = yaml.dump(value, allow_unicode=True)

        # encode to utf-8 bytes and compress
        compressed = zlib.compress(serialized.encode())

        # wrap in QByteArray
        bytearray = QtCore.QByteArray(compressed)

        # write using a data stream
        writer = QtCore.QDataStream(self.socket)
        writer.setVersion(QtCore.QDataStream.Qt_4_8)
        writer << bytearray

    def count_bytes_written(self, bytes):
        self.bytes_written += bytes


class Server(QtCore.QObject):
    """
        Wrapper around QtNetwork.QTcpServer and a management of several clients (each a QtNetwork.QTcpSocket).
    """

    new_client = QtCore.Signal(QtNetwork.QTcpSocket)

    def __init__(self):
        """
        """
        super().__init__()
        self.server = QtNetwork.QTcpServer(self)
        self.server.newConnection.connect(self.new_connection)

    def start(self, port, scope='local'):
        """
            Given an address (hostname, port) tries to start listening.
            QtNetwork.QHostAddress.Any
        """
        host = SCOPE[scope]
        if not self.server.listen(host, port):
            raise RuntimeError('Network error: cannot listen')

    def isListening(self):
        return self.server.isListening()

    def scope(self):
        if self.isListening():
            return SCOPE.keys()[SCOPE.values().index(self.server.serverAddress())]
        else:
            return None

    def stop(self):
        """
            Stopps listening.
        """
        if self.isListening():
            self.server.close()

    def new_connection(self):
        """
            Zero or more new clients might be available, emit new_client signal for each of them.
        """
        while self.server.hasPendingConnections():
            # returns a new QTcpSocket
            socket = self.server.nextPendingConnection()
            # emit signal
            self.new_client.emit(socket)


