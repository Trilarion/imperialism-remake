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

'''
    Basic actions of QTcpServer, QTcpSocket communication.
'''

from PyQt5 import QtCore, QtNetwork

def new_server_connection():
    print('new server connection')

def new_client_connection():
    print('new client connection')

def setup():
    server.listen(QtNetwork.QHostAddress.LocalHost, 34543)
    client_socket.connectToHost(QtNetwork.QHostAddress.LocalHost, 34543)


app = QtCore.QCoreApplication([])

server = QtNetwork.QTcpServer()
server.newConnection.connect(new_server_connection)
client_socket = QtNetwork.QTcpSocket()
client_socket.connected.connect(new_client_connection)

QtCore.QTimer.singleShot(0, setup)
QtCore.QTimer.singleShot(3000, app.quit)
app.exec_()