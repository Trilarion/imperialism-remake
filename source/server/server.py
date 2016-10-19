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
import base.network
from lib import utils
import lib.network
from server.scenario import Scenario

# TODO change this
from base.constants import ScenarioProperties as k, NationProperties as kn


# TODO start this in its own process
# TODO ping server clients regularly and throw them out if not reacting
# TODO wait for a name but only change it once during a session

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

class ServerNetworkClient(base.network.NetworkClient):
    """
    Server network client.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # important properties
        self.subscribed_to_chat = False
        self.name = ''


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
        self.server = lib.network.ExtendedTcpServer()
        self.server.new_client.connect(self._new_client)
        self.server_clients = []
        self.chat_log = []

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
        client = ServerNetworkClient(socket)

        # give it a new id
        while True:
            # theoretically this could take forever, practically only if we have 1e6 clients already
            new_id = random.randint(0, 1e6)
            if not any([new_id == client.client_id for client in self.server_clients]):
                # not any == none
                break
        client.client_id = new_id
        print('new client with id {}'.format(new_id))

        # add some general channels and receivers
        # TODO the receivers should be in another module eventually
        client.connect_to_channel(constants.C.LOBBY, lobby_messages)
        client.connect_to_channel(constants.C.GENERAL, general_messages)

        # TODO only if localhost connection add the system channel
        client.connect_to_channel(constants.C.SYSTEM, self._system_messages)

        # chat message system, handled by a single central routine
        client.connect_to_channel(constants.C.CHAT, self._chat_system)

        # finally add to list of clients
        self.server_clients.append(client)

    def _chat_system(self, client:ServerNetworkClient, channel:constants.C, action:constants.M, content):
        """

        :param client:
        :param channel:
        :param action:
        :param content:
        """

        if action == constants.M.CHAT_SUBSCRIBE:
            # add this client to list of clients to be notified of new chat messages
            client.subscribed_to_chat = True

        elif action == constants.M.CHAT_UNSUBSCRIBE:
            # remove this client from list of clients to be notified of new chat messages
            client.subscribed_to_chat = False

        elif action == constants.M.CHAT_LOG:
            # send history/log of last chat messages
            pass

        elif action == constants.M.CHAT_MESSAGE:
            # new chat message from this client, log and distribute

            # format message
            chat_message = '{}: {}'.format(client.name, content)

            # append to chat log
            self.chat_log.append(chat_message)

            # distribute chat message
            for client in self.server_clients:
                if client.subscribed_to_chat:
                    client.send(constants.C.CHAT, constants.M.CHAT_MESSAGE, chat_message)


    def _system_messages(self, client:ServerNetworkClient, channel:constants.C, action:constants.M, content):
        """
        Handles system messages of a local client to its local server. Not intended for outside use.

        :param client:
        :param channel:
        :param action:
        :param content:
        """
        if action == constants.M.SYSTEM_SHUTDOWN:
            # shuts down

            print('server manager shuts down')
            # TODO disconnect all server clients, clean up, ...
            self.server.stop()
            self.shutdown.emit()

def general_messages(client:ServerNetworkClient, channel:constants.C, action:constants.M, content):
    """

    :param client:
    :param channel:
    :param action:
    :param content:
    """

    if action == constants.M.GENERAL_NAME:
        client.name = content

def lobby_messages(client:ServerNetworkClient, channel:constants.C, action:constants.M, content):
    """

    :param client:
    :param channel:
    :param action:
    :param content:
    """
    if action == constants.M.LOBBY_SCENARIO_CORE_LIST:
        # get list and return
        scenarios = scenario_core_titles()
        client.send(channel, action, scenarios)

    elif action == constants.M.LOBBY_SCENARIO_PREVIEW:
        # get preview and send it
        preview = scenario_preview(content)
        client.send(channel, action, preview)

def scenario_core_titles():
    """
    A server client received a message on the constants.C.SCENARIO_CORE_TITLES channel. Return all available core
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

    return scenarios


def scenario_preview(scenario_file_name):
    """
    A client got a message on the constants.C.SCENARIO_PREVIEW channel. In the message should be a scenario file name
    (key = 'scenario'). Assemble a preview and send it back.
    """
    t0 = time.clock()

    # TODO existing? can be loaded?
    scenario = Scenario.from_file(scenario_file_name)
    print('reading the file took {}s'.format(time.clock() - t0))

    preview = {'scenario': scenario_file_name}

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

    print('generating preview took {}s'.format(time.clock() - t0))

    return preview
