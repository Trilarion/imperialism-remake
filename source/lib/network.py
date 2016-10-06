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
Basic general network functionality (client and server) wrapping around QtNetwork.QTcpSocket and QtNetwork.QTcpServer.

Messages are sent using yaml (for serialization) and zlib (for compression).
"""

import zlib

import PyQt5.QtCore as QtCore
import PyQt5.QtNetwork as QtNetwork
import yaml

#: shortcut for QtNetwork.QHostAddress.LocalHost/Any
SCOPE = {'local': QtNetwork.QHostAddress.LocalHost, 'any': QtNetwork.QHostAddress.Any}


class ExtendedTcpSocket(QtCore.QObject):
    """
    Wrapper around QtNetwork.QTcpSocket. The socket can either be given in the initialization or be created there.
    Sends and reads messages via serialization (yaml), compression (zlib) and wrapping (QByteArray) as well as
    un-wrapping, de-compressing and de-serialization on the other side.
    """

    #: signal for socket connected
    connected = QtCore.pyqtSignal()
    #: signal for socket disconnected
    disconnected = QtCore.pyqtSignal()
    #: signal for a SocketError
    error = QtCore.pyqtSignal(QtNetwork.QAbstractSocket.SocketError)
    #: signal for a received message (only whole messages are emitted)
    received = QtCore.pyqtSignal(object)

    def __init__(self, socket:QtNetwork.QTcpSocket=None):
        """
        Initializes the extended TCP socket. Either wraps around an existing socket or creates its own and resets
        the number of bytes written.

        :param socket: An already existing socket or None if none is given.
        """
        super().__init__()

        # new QTcpSocket() if none is given
        if socket is not None:
            self.socket = socket
        else:
            self.socket = QtNetwork.QTcpSocket()

        # some wiring, new data is handled by receive()
        self.socket.readyRead.connect(self.receive)
        self.socket.error.connect(self.error)
        self.socket.connected.connect(self.connected)
        self.socket.disconnected.connect(self.disconnected)
        self.socket.bytesWritten.connect(self.count_bytes_written)

        self.bytes_written = 0

    def peer_address(self):
        """
        Returns the peer address. The socket must be connected first.

        :return: A tuple of the peer address and the peer port
        """
        return self.socket.peerAddress(), self.socket.peerPort()

    def disconnect_from_host(self):
        """
        Attempts to close the underlying socket.
        """
        self.socket.disconnectFromHost()

    def connect_to_host(self, port, host='local'):
        """
        Tries to connect to a host specified by port and host address.

        :param port: The port number to connect to.
        :param host: The host address (or 'local' for the local host) to connect to.
        """
        # TODO only if not yet connected
        if host == 'local':
            host = SCOPE['local']
        print('client connects to host={} port={}'.format(host, port))
        self.socket.connectToHost(host, port)
        self.socket.waitForConnected(2000)

    def receive(self):
        """
        Called by the sockets readyRead signal. Not intended for outside use.
        While there are messages available read them and process them.
        Reading is reading of a QByteArray from the TCPSocket, un-compressing and de-serializing.
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

            print('socket received {}'.format(value))

            # print('connection id {} received {}'.format(self.id, value))
            self.received.emit(value)

    def send(self, value):
        """
        Sends a message by serializing, compressing and wrapping to a QByteArray, then streaming over the TCP socket.

        :param value: The message to send.
        """
        print('socket send {}'.format(value))
        # serialize value to yaml
        serialized = yaml.dump(value, allow_unicode=True)

        # encode to utf-8 bytes and compress
        compressed = zlib.compress(serialized.encode())

        # wrap in QByteArray
        bytearray = QtCore.QByteArray(compressed)

        # write using a data stream
        writer = QtCore.QDataStream(self.socket)
        writer.setVersion(QtCore.QDataStream.Qt_5_6)
        writer << bytearray

    def count_bytes_written(self, bytes):
        """
        Called by the sockets bytesWritten signal. Not intended for outside use.

        :param bytes: Number of written bytes.
        """
        self.bytes_written += bytes


class ExtendedTcpServer(QtCore.QObject):
    """
        Wrapper around QtNetwork.QTcpServer providing some simple functionality to determine the scope (local/any) and
        to delegate the acceptError and newConnection signals of the underlying QTcpServer.
    """

    #: signal for a new connected client socket
    new_client = QtCore.pyqtSignal(QtNetwork.QTcpSocket)

    def __init__(self):
        super().__init__()
        self.tcp_server = QtNetwork.QTcpServer(self)
        self.tcp_server.acceptError.connect(self.accept_error)
        self.tcp_server.newConnection.connect(self.new_connection)

    def accept_error(self, socket_error):
        """
        An error occurred.

        :param socket_error: QAbstractSocket::SocketError
        """
        print('accept error {}'.format(socket_error))

    def start(self, port, scope:SCOPE='local'):
        """
            Given a port number and a scope (local/any), starts listening.

        :param port: The port number.
        :param scope: The scope (local/any).
        """
        host = SCOPE[scope]
        print('server listens on host={} port={}'.format(host, port))
        if not self.tcp_server.listen(host, port):
            raise RuntimeError('Network error: cannot listen')
        print('is listening {}'.format(self.tcp_server.isListening()))

    def is_listening(self):
        """
        Is the server listening (active)?
        """
        return self.tcp_server.isListening()

    def stop(self):
        """
        Stops listening/closes the server.
        """
        if self.tcp_server.isListening():
            self.tcp_server.close()

    def new_connection(self):
        """
        Called by the newConnection signal of the QTCPServer.
        Zero or more new clients might be available, emit new_client signal for each of them.
        """
        print('new connection on server')
        while self.tcp_server.hasPendingConnections():
            # returns a new QTcpSocket
            socket = self.tcp_server.nextPendingConnection()
            # emit signal
            self.new_client.emit(socket)
