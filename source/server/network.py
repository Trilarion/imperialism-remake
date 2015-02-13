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

import random
import os
import time

from PySide import QtCore

from lib.network import Server
import lib.utils as u
import base.constants as c
from base.constants import PropertyKeyNames as k, NationPropertyKeyNames as kn
from base.network import NetworkClient
from server.scenario import Scenario

"""
    Server network code. Only deals with the network connection, client connection management and message distribution.
"""

# TODO ping server clients regularly and throw them out if not reacting

class ServerManager(QtCore.QObject):
    """
        Manages the server, the clients on the server and the general services on the server. In particular creates new
        clients on the server (server clients),
    """

    def __init__(self):
        """
            We start with a server and an empty list of server clients.
        """
        super().__init__()
        self.server = Server()
        self.server.new_client.connect(self.new_client)
        self.server_clients = []

    def new_client(self, socket):
        """
            A new connection to the server. Give an id and add some general receivers to the new server client.
            Finally append new server client to the internal client list.
        """
        client = NetworkClient()
        client.set_socket(socket)

        # give a new id
        while True:
            # theoretically this could take forever, practically only if we have 1e6 clients already
            id = random.randint(0, 1e6)
            if not any([id == client.id for client in self.server_clients]):
                # not any == none
                break
        client.client_id = id

        # add some general receivers.
        client.connect_to_channel(c.CH_SCENARIO_PREVIEW, self.scenario_preview)
        client.connect_to_channel(c.CH_CORE_SCENARIO_TITLES, self.core_scenario_titles)

        # finally add to list of clients
        self.server_clients.append(client)

    def core_scenario_titles(self, client, message):
        """
            A server client received a message on the c.CH_CORE_SCENARIO_TITLES channel. Return all available core
            scenario titles and file names.
        """
        # get all core scenario files
        scenario_files = [x for x in os.listdir(c.Core_Scenario_Folder) if x.endswith('.scenario')]

        # joing the path
        scenario_files = [os.path.join(c.Core_Scenario_Folder, x) for x in scenario_files]

        # read scenario titles
        scenario_titles = []
        for scenario_file in scenario_files:
            reader = u.ZipArchiveReader(scenario_file)
            properties = reader.read_as_yaml('properties')
            scenario_titles.append(properties[k.TITLE])

        # zip files and titles together
        scenarios = zip(scenario_titles, scenario_files)

        # sort them
        scenarios = sorted(scenarios)  # default sort order is by first element anyway

        # return message
        titles = {
            'scenarios': scenarios
        }
        client.send(message['reply-to'], titles)

    def scenario_preview(self, client, message):
        """
            A client got a message on the c.CH_SCENARIO_PREVIEW channel. In the message should be a scenario file name
            (key = 'scenario'). Assemble a preview and send it back.
        """
        t0 = time.clock()

        scenario = Scenario()
        file_name = message['scenario']  # should be the file name
        # TODO existing? can be loaded?
        scenario.load(file_name)
        print('reading the file took {}s'.format(time.clock() - t0))

        preview = {}
        preview['scenario'] = file_name

        # some scenario properties should be copied
        scenario_copy_keys = [k.MAP_COLUMNS, k.MAP_ROWS, k.TITLE, k.DESCRIPTION]
        for key in scenario_copy_keys:
            preview[key] = scenario[key]

        # some nations properties should be copied
        nations = {}
        nation_copy_keys = [kn.COLOR, kn.NAME, kn.DESCRIPTION]
        for nation in scenario.all_nations():
            nations[nation] = {}
            for key in nation_copy_keys:
                nations[nation][key] = scenario.get_nation_property(nation, key)
        preview['nations'] = nations

        # assemble a nations map (-1 means no nation)
        columns = scenario[k.MAP_COLUMNS]
        rows = scenario[k.MAP_ROWS]
        map = [-1] * (columns * rows)
        for nation_id in scenario.all_nations():
            provinces = scenario.get_provinces_of_nation(nation_id)
            for province in provinces:
                tiles = scenario.get_province_property(province, 'tiles')
                for column, row in tiles:
                    map[row * columns + column] = nation_id
        preview['map'] = map

        # send return message
        client.send(message['reply-to'], preview)

        print('generating preview took {}s'.format(time.clock() - t0))

# create a local server
server_manager = ServerManager()