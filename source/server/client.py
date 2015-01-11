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

from PySide import QtCore

class ServerClientManager():

    def __init__(self):
        self.clients_chat = []

    def chat_register(self, client):
        pass

    def chat_unregister(self, client):
        pass

    def chat_broadcast(self, client, text):
        pass

manager = ServerClientManager()

class ServerClient(QtCore.QObject):

    send = QtCore.Signal(dict)

    def __init__(self):
        super().__init__()

    def receive(self, message):
        if message['type'] is 'chat.register':
            manager.chat_register(self)
        if message['type'] is 'chat.message':
            manager.chat_broadcast(self, message['text'])
