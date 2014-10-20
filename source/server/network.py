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
from functools import partial

from PySide import QtNetwork

import lib.network as net

class ServerClient(net.EnhancedSocket):

    def __init__(self, socket):
        super().__init__(socket)



class Server(net.Server):

    def __init__(self):
        super().__init__(ServerClient)
        self.new_client.connect(self.initialize_new_client)

    def new_id(self):
        """
            Creates a new random id in the range of 0 to 1e6.
        """
        while True:
            # theoretically this could take forever, practically only if we have 1e6 clients already
            id = random.randint(0, 1e6)
            if id not in self.clients:
                return id

    def initialize_new_client(self, client):
        pass


# create a local server
server = Server()
