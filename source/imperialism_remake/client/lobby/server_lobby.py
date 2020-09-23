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
Game lobby. Place for starting/loading games.
"""
import logging

from PyQt5 import QtCore, QtWidgets

from imperialism_remake.base import constants, network as base_network
from imperialism_remake.client.client.client_network_connection import network_connection
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


class ServerLobby(QtWidgets.QWidget):
    """
    Server lobby.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout(self)

        self.client_list_widget = QtWidgets.QListWidget()
        #       list.itemSelectionChanged.connect(self.selection_changed)
        #       list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.client_list_widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.client_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.client_list_widget.setFixedWidth(200)
        layout.addWidget(qt.wrap_in_groupbox(self.client_list_widget, 'Players'))

        self.chat_log_text_edit = QtWidgets.QTextEdit()
        self.chat_log_text_edit.setEnabled(False)
        chat_log_group = qt.wrap_in_groupbox(self.chat_log_text_edit, 'Chat log')

        self.chat_input_edit = QtWidgets.QLineEdit()
        self.chat_input_edit.returnPressed.connect(self.send_chat_message)
        chat_input_group = qt.wrap_in_groupbox(self.chat_input_edit, 'Chat input')
        layout.addLayout(qt.wrap_in_boxlayout((chat_log_group, chat_input_group), horizontal=False, add_stretch=False),
                         stretch=1)

        # connection to server

        # chat messages
        network_connection.connect_to_chat(self.receive_chat_messages)

        # LOBBY
        network_connection.connect_to_lobby(self.receive_lobby_messages)

        self.request_updated_client_list()

        # set timer for connected client updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.request_updated_client_list)
        self.timer.setInterval(5000)
        self.timer.start()

    def send_chat_message(self):
        """
        Sends a chat message.
        """
        network_connection.send_message_to_chat(self.chat_input_edit.text())

        self.chat_input_edit.setText('')

    def receive_chat_messages(self, client: base_network.NetworkClient, channel: constants.C, action: constants.M,
                              content):
        """
        Receives a chat message. Adds it to the chat log.

        :param client:
        :param channel:
        :param action:
        :param content:
        """
        if action == constants.M.CHAT_MESSAGE:
            self.chat_log_text_edit.append(content)

    def request_updated_client_list(self):
        """
        Sends a request to get an updated connected client list.
        """
        network_connection.request_client_list_for_chat()

    def receive_lobby_messages(self, client: base_network.NetworkClient, channel: constants.C, action: constants.M,
                               content):
        """
        Handles all received lobby messages.

        :param client:
        :param channel:
        :param action:
        :param content:
        """
        if action == constants.M.LOBBY_CONNECTED_CLIENTS:
            self.client_list_widget.clear()
            self.client_list_widget.addItems(content)

    def cleanup(self, parent_widget):
        """
        User wants to close the dialog

        :param parent_widget:
        """
        network_connection.disconnect_from_chat(self.receive_chat_messages)
        network_connection.disconnect_from_lobby(self.receive_lobby_messages)

        return True
