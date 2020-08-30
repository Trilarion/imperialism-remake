# Imperialism remake
# Copyright (C) 2014-16 Trilarion
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

Messages are sent using pickle (for serialization) and zlib (for compression).
"""

import logging
import pickle
import time
import zlib

from PyQt5 import QtCore, QtNetwork

#: shortcut for QtNetwork.QHostAddress.LocalHost/Any
SCOPE = {'local': QtNetwork.QHostAddress.LocalHost, 'any': QtNetwork.QHostAddress.Any}

logger = logging.getLogger(__name__)


class ExtendedTcpSocket(QtCore.QObject):
    """
    Wrapper around QtNetwork.QTcpSocket. The socket can either be given in the initialization or be created there.
    Sends and reads messages via serialization (pickle), compression (zlib) and wrapping (QByteArray) as well as
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

    def __init__(self, socket: QtNetwork.QTcpSocket = None):
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

        # some wiring, new data is handled by _receive()
        self.socket.readyRead.connect(self._receive)
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
        logger.info('client connecting to host=%s port=%d', host, port)
        # try to connect multiple times - maybe the server did not manage to start, yet
        failure_count = 0
        while True:
            self.socket.connectToHost(host, port)
            if self.socket.waitForConnected(2000):
                break
            else:
                time.sleep(0.2)
                logger.warning("connection delayed - will try again")
                failure_count += 1
                if failure_count == 10:
                    raise RuntimeError('Failed to connect to server: host=%s port=%d', host, port)
        logger.info('client successfully connected to host=%s port=%d', host, port)

    def is_connected(self):
        """

        :return: True if it is connected
        """
        return self.socket.state() == QtNetwork.QAbstractSocket.ConnectedState

    def _receive(self):
        """
        Called by the sockets readyRead signal. Not intended for outside use.
        While there are messages available read them and process them.
        Reading is reading of a QByteArray from the TCPSocket, un-compressing and de-serializing.
        """
        while self.socket.bytesAvailable() > 0:
            logger.info('socket will receive')
            # read a QByteArray using a data stream
            reader = QtCore.QDataStream(self.socket)
            bytearray = QtCore.QByteArray()
            reader >> bytearray

            # uncompress bytes from bytearray
            uncompressed = zlib.decompress(bytearray.data())

            # security validator (check for everything that we do not like (!!python)
            # TODO implement this

            value = pickle.loads(uncompressed)

            logger.debug('socket received: %s', value)

            self.received.emit(value)

    def send(self, value):
        """
        Sends a message by serializing, compressing and wrapping to a QByteArray, then streaming over the TCP socket.

        :param value: The message to send.
        """
        if not self.is_connected():
            raise RuntimeError('Try to send on unconnected socket.')

        logger.debug('socket send: %s', value)

        compressed = zlib.compress(pickle.dumps(value))

        # wrap in QByteArray
        bytearray = QtCore.QByteArray(compressed)

        # write using a data stream
        writer = QtCore.QDataStream(self.socket)
        writer.setVersion(QtCore.QDataStream.Qt_5_10)
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
        self.tcp_server.newConnection.connect(self._new_connection)

    def accept_error(self, socket_error):
        """
        An error occurred.

        :param socket_error: QAbstractSocket::SocketError
        """
        logger.info('accept error %s', socket_error)

    def start(self, port, scope: SCOPE = 'local'):
        """
            Given a port number and a scope (local/any), starts listening.

        :param port: The port number.
        :param scope: The scope (local/any).
        """
        host = SCOPE[scope]
        logger.info('server listens on host=%s port=%d', host, port)
        if not self.tcp_server.listen(host, port):
            raise RuntimeError('Network error: cannot listen')
        logger.info('is listening %s', self.tcp_server.isListening())

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

    def _new_connection(self):
        """
        Called by the newConnection signal of the QTCPServer. Not intended for outside use.
        Zero or more new clients might be available, emit new_client signal for each of them.
        """
        logger.info('new connection on server')
        while self.tcp_server.hasPendingConnections():
            # returns a new QTcpSocket
            socket = self.tcp_server.nextPendingConnection()
            # emit signal
            self.new_client.emit(socket)
