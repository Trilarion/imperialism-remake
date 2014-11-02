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

import random, os
from PySide import QtCore

from lib.network import Server
from base.network import NetworkClient
import constants as c, tools as t

class ServerManager(QtCore.QObject):

    def __init__(self):
        super().__init__()
        self.server = Server()
        self.server.new_client.connect(self.new_client)
        self.server_clients = []
        self.general_actions = {
            c.MsgID.scenario_titles : self.scenario_titles
        }

    def new_client(self, socket):
        client = NetworkClient()
        client.set_socket(socket)

        # give a new id
        found_id = False
        while not found_id:
            # theoretically this could take forever, practically only if we have 1e6 clients already
            id = random.randint(0, 1e6)
            if not any([id == client.id for client in self.server_clients]):
                # not any == none
                found_id = True
        client.id = id

        # add a GeneralActionListener
        client.register_receiver(c.MsgID.cat_general, self.general_actions_receiver)

        # finally add to list of clients
        self.server_clients.append(client)

    def general_actions_receiver(self, client, message):
        # get subtype
        subtype = message['signature'][1]
        if subtype in self.general_actions:
            return self.general_actions[subtype](client, message)
        return False

    def scenario_titles(self, client, message):
        # get all core scenario files
        scenario_files = [x for x in os.listdir(c.Core_Scenario_Folder) if x.endswith('.scenario')]

        # joing the path
        scenario_files = [os.path.join(c.Core_Scenario_Folder, x) for x in scenario_files]

        # read scenario titles
        scenario_titles = []
        for scenario_file in scenario_files:
            reader = t.ZipArchiveReader(scenario_file)
            properties = reader.read_as_json('properties')
            scenario_titles.append(properties['title'])

        # zip files and titles together
        scenarios = zip(scenario_titles, scenario_files)

        # sort them
        scenarios = sorted(scenarios) # default sort order is by first element anyway

        # return message
        answer = {
            'scenarios' : scenarios
        }
        client.send((c.MsgID.cat_general, c.MsgID.scenario_titles), answer)

        return True

# create a local server
server_manager = ServerManager()