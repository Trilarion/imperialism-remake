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
Examples for base.network and server.network using chat
"""

from PyQt5 import QtCore

import imperialism_remake
from base import constants, network
from server.server import ServerManager

def clients_connect():
    """
    Clients try to connect.
    """
    clientA.connect_to_host(constants.NETWORK_PORT)
    clientB.connect_to_host(constants.NETWORK_PORT)

def clients_send_names():
    """
    Clients send their names.
    """
    clientA.send(constants.C.GENERAL, constants.M.GENERAL_NAME, 'Alice')
    clientB.send(constants.C.GENERAL, constants.M.GENERAL_NAME, 'Bob')

def clientA_subscribes():
    """
    Client A subscribes to chat messages.
    """
    clientA.connect_to_channel(constants.C.CHAT, receives_chat)
    clientA.send(constants.C.CHAT, constants.M.CHAT_SUBSCRIBE)

def clientB_subscribes():
    """
    Client B subscribes to chat messages.
    """
    clientB.connect_to_channel(constants.C.CHAT, receives_chat)
    clientB.send(constants.C.CHAT, constants.M.CHAT_SUBSCRIBE)

def receives_chat(client, channel, action, message):
    """
    Chat received
    """
    if action == constants.M.CHAT_MESSAGE:
        print('client {} received chat {}'.format(client, message))


def clientA_chats():
    """
    Client A chats.
    """
    clientA.send(constants.C.CHAT, constants.M.CHAT_MESSAGE, "I'm fine Bob, and you?")

def clientB_chats():
    """
    Client B chats.
    """
    clientB.send(constants.C.CHAT, constants.M.CHAT_MESSAGE, 'Hi Alice, how are you?')

if __name__ == '__main__':
    imperialism_remake.fix_pyqt5_exception_eating()
    imperialism_remake.set_start_directory()

    app = QtCore.QCoreApplication([])

    server_manager = ServerManager()
    clientA = network.NetworkClient()
    clientB = network.NetworkClient()

    # actions
    QtCore.QTimer.singleShot(0, server_manager.start)
    QtCore.QTimer.singleShot(100, clients_connect)
    QtCore.QTimer.singleShot(500, clients_send_names)
    QtCore.QTimer.singleShot(800, clientA_subscribes)
    QtCore.QTimer.singleShot(1000, clientB_chats)
    QtCore.QTimer.singleShot(1200, clientB_subscribes)
    QtCore.QTimer.singleShot(1400, clientA_chats)
    QtCore.QTimer.singleShot(3000, app.quit)

    app.exec_()
