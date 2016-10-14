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
    Server network code. Only deals with the network connection, client connection management and message distribution.
"""

import multiprocessing
import os
import random
import sys
import time

import PyQt5.QtCore as QtCore
import PyQt5.QtNetwork as QtNetwork

import imperialism_remake
from base import constants
from base.network import NetworkClient
from lib import utils
from lib.network import ExtendedTcpServer
from server.scenario import Scenario

# TODO change this
from base.constants import ScenarioProperties as k, NationProperties as kn


# TODO start this in its own process
# TODO ping server clients regularly and throw them out if not reacting

class ServerProcess(multiprocessing.Process):
    """
    A Process that inside its run method executes a QCoreApplication which runs the server.
    """

    def __init__(self):
        super().__init__()

    def run(self):
        """
        Runs the server process by starting its own QCoreApplication.
        """
        # because PyQt5 eats exceptions in the event thread this workaround
        sys.excepthook = imperialism_remake.exception_hook

        app = QtCore.QCoreApplication([])

        # server manager, signal shutdown stops the app
        server_manager = ServerManager()
        server_manager.shutdown.connect(app.quit)
        # noinspection PyCallByClass
        QtCore.QTimer.singleShot(0, server_manager.start)

        # run event loop of app
        app.exec_()


class ServerManager(QtCore.QObject):
    """
    Manages the server, the clients on the server and the general services on the server. In particular creates new
    clients (NetworkClient) on the server (named server clients).
    """

    #: signal
    shutdown = QtCore.pyqtSignal()

    def __init__(self):
        """
        We start with a server (ExtendedTcpServer) and an empty list of server clients (NetworkClient).
        """
        super().__init__()
        self.server = ExtendedTcpServer()
        self.server.new_client.connect(self._new_client)
        self.server_clients = []

    def start(self):
        """
        Start the extended TCP server with a local scope.
        """
        print('server starts')
        self.server.start(constants.NETWORK_PORT)

    def _new_client(self, socket: QtNetwork.QTcpSocket):
        """
        A new connection (QTCPPSocket) to the server occurred. Give it an id and add some general receivers to the new
        server client (wrap the socket into a NetworkClient). Add the new server client to the internal client list.
        Not intended for outside use.

        :param socket: The socket for the new connection
        """
        # wrap into a NetworkClient
        client = NetworkClient(socket)

        # give it a new id
        while True:
            # theoretically this could take forever, practically only if we have 1e6 clients already
            new_id = random.randint(0, 1e6)
            if not any([new_id == client.id for client in self.server_clients]):
                # not any == none
                break
        client.client_id = new_id
        print('new client with id {}'.format(new_id))

        # add some general channels and receivers
        # TODO the receivers should be in another module eventually
        client.connect_to_channel(constants.CH_SCENARIO_PREVIEW, scenario_preview)
        client.connect_to_channel(constants.CH_CORE_SCENARIO_TITLES, core_scenario_titles)

        # TODO only if localhost connection add the system channel
        client.connect_to_channel(constants.CH_SYSTEM, self._system_messages)

        # finally add to list of clients
        self.server_clients.append(client)

    def _system_messages(self, client, message):
        """
        Handles system messages of a local client to its local server. Not intended for outside use.
        """
        if message == 'shutdown':
            print('server manager shuts down')
            # shutdown
            # TODO disconnect all server clients, clean up, ...
            self.server.stop()
            self.shutdown.emit()


def core_scenario_titles(client, message):
    """
    A server client received a message on the constants.CH_CORE_SCENARIO_TITLES channel. Return all available core
    scenario titles and file names.
    """
    # get all core scenario files
    scenario_files = [x for x in os.listdir(constants.CORE_SCENARIO_FOLDER) if x.endswith('.scenario')]

    # join the path
    scenario_files = [os.path.join(constants.CORE_SCENARIO_FOLDER, x) for x in scenario_files]

    # read scenario titles
    scenario_titles = []
    for scenario_file in scenario_files:
        reader = utils.ZipArchiveReader(scenario_file)
        properties = reader.read_as_yaml(constants.SCENARIO_FILE_PROPERTIES)
        scenario_titles.append(properties[k.TITLE])

    # zip files and titles together
    scenarios = zip(scenario_titles, scenario_files)

    # sort them
    scenarios = sorted(scenarios)  # default sort order is by first element anyway

    # return message
    titles = {'scenarios': scenarios}
    client.send(constants.CH_CORE_SCENARIO_TITLES, titles)


def scenario_preview(client, message):
    """
    A client got a message on the constants.CH_SCENARIO_PREVIEW channel. In the message should be a scenario file name
    (key = 'scenario'). Assemble a preview and send it back.
    """
    t0 = time.clock()

    file_name = message['scenario']  # should be the file name
    # TODO existing? can be loaded?
    scenario = Scenario.from_file(file_name)
    print('reading the file took {}s'.format(time.clock() - t0))

    preview = {'scenario': file_name}

    # some scenario properties should be copied
    scenario_copy_keys = [k.MAP_COLUMNS, k.MAP_ROWS, k.TITLE, k.DESCRIPTION]
    for key in scenario_copy_keys:
        preview[key] = scenario[key]

    # some nations properties should be copied
    nations = {}
    nation_copy_keys = [kn.COLOR, kn.NAME, kn.DESCRIPTION]
    for nation in scenario.nations():
        nations[nation] = {}
        for key in nation_copy_keys:
            nations[nation][key] = scenario.nation_property(nation, key)
    preview['nations'] = nations

    # assemble a nations map (-1 means no nation)
    columns = scenario[k.MAP_COLUMNS]
    rows = scenario[k.MAP_ROWS]
    nations_map = [-1] * (columns * rows)
    for nation_id in scenario.nations():
        provinces = scenario.provinces_of_nation(nation_id)
        for province in provinces:
            tiles = scenario.province_property(province, 'tiles')
            for column, row in tiles:
                nations_map[row * columns + column] = nation_id
    preview['map'] = nations_map

    # send return message
    client.send(message['reply-to'], preview)

    print('generating preview took {}s'.format(time.clock() - t0))
