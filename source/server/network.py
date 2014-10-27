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
    Server network code. Only deals with the network connection, client connection management and message distribution.
"""

import random
from PySide import QtCore

import lib.network as net

class ServerClient(net.Client):

    def __init__(self):
        super().__init__()

class ServerManager(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self.server = net.Server()
        self.server.new_client.connect(self.new_client)
        self.server_clients = []

    def new_client(self, socket):
        client = ServerClient()
        client.set_socket(socket)
        client.id = self.create_new_id()

        # finally add to list of clients
        self.server_clients.append(client)

    def create_new_id(self):
        """
            Creates a new random id in the range of 0 to 1e6.
        """
        while True:
            # theoretically this could take forever, practically only if we have 1e6 clients already
            id = random.randint(0, 1e6)
            if not any([id == client.id for client in self.server_clients]):
                # not any == none
                return id

# create a local server
#manager = ServerManager()
