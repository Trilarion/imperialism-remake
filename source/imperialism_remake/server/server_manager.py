# Imperialism remake
# Copyright (C) 2020 amtyurin
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

import logging
import os
import time
import uuid
from datetime import datetime

from PyQt5 import QtCore, QtNetwork

from imperialism_remake.base import constants
from imperialism_remake.lib import network as lib_network, utils
from imperialism_remake.server.server_network_client import ServerNetworkClient
from imperialism_remake.server.server_scenario import ServerScenario

logger = logging.getLogger(__name__)


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
        logger.info("ServerManager started")
        self.server = lib_network.ExtendedTcpServer()
        self.server.new_client.connect(self._new_client)
        self.server_clients = []
        self.chat_log = []

    def start(self):
        """
        Start the extended TCP server with a local scope.
        """
        logger.info('server starts (pid=%d)', os.getpid())
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
            new_id = uuid.uuid4()
            if not any([new_id == client.client_id for client in self.server_clients]):
                # not any == none
                break
        # noinspection PyUnboundLocalVariable
        client.client_id = new_id
        logger.info('new client with id {}'.format(new_id))

        # add some general channels and receivers
        # TODO the receivers should be in another module eventually
        client.connect_to_channel(constants.C.LOBBY, self._lobby_messages)
        client.connect_to_channel(constants.C.GENERAL, self._general_messages)

        # TODO only if localhost connection add the system channel
        client.connect_to_channel(constants.C.SYSTEM, self._system_messages)

        # chat message system, handled by a single central routine
        client.connect_to_channel(constants.C.CHAT, self._chat_system)

        # finally add to list of clients
        self.server_clients.append(client)

        logger.info('server server_clients len: %d', len(self.server_clients))

    def _chat_system(self, client: ServerNetworkClient, channel: constants.C, action: constants.M, content):
        """

        :param client:
        :param channel:
        :param action:
        :param content:
        """

        logger.debug('_chat_system action: %s', action)
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
            now = datetime.now().strftime('%H:%M:%S')
            chat_message = '{}: {} - {}'.format(now, client.name, content)

            # append to chat log
            self.chat_log.append(chat_message)

            # distribute chat message
            for client in self.server_clients:
                if client.subscribed_to_chat:
                    client.send(constants.C.CHAT, constants.M.CHAT_MESSAGE, chat_message)

    def _system_messages(self, client: ServerNetworkClient, channel: constants.C, action: constants.M, content):
        """
        Handles system messages of a local client to its local server. Not intended for outside use.

        :param client:
        :param channel:
        :param action:
        :param content:
        """
        logger.debug('_system_messages action: %s', action)

        if action == constants.M.SYSTEM_SHUTDOWN:
            # shuts down

            logger.info('server manager shuts down')
            # TODO disconnect all server clients, clean up, ...
            self.server.stop()
            self.shutdown.emit()

        elif action == constants.M.SYSTEM_MONITOR_UPDATE:

            # assemble monitor update
            update = {
                'number_connected_clients': len(self.server_clients)
            }
            client.send(constants.C.SYSTEM, constants.M.SYSTEM_MONITOR_UPDATE, update)

    def _lobby_messages(self, client: ServerNetworkClient, channel: constants.C, action: constants.M, content):
        """

        :param client:
        :param channel:
        :param action:
        :param content:
        """
        logger.debug('_lobby_messages action: %s', action)

        if action == constants.M.LOBBY_SCENARIO_CORE_LIST:
            # get list of scenarios and send it back
            scenarios = self._scenario_core_titles()
            client.send(channel, action, scenarios)

        elif action == constants.M.LOBBY_SCENARIO_PREVIEW:
            # get preview and send it back
            preview = self.scenario_preview(content)
            client.send(channel, action, preview)

        elif action == constants.M.LOBBY_CONNECTED_CLIENTS:
            # get list of connected clients and send it back
            connected_clients = [c.name for c in self.server_clients]
            client.send(channel, action, connected_clients)

    def _general_messages(self, client: ServerNetworkClient, channel: constants.C, action: constants.M, content):
        """

        :param client:
        :param channel:
        :param action:
        :param content:
        """
        logger.debug('_general_messages action: %s', action)
        if action == constants.M.GENERAL_NAME:
            client.name = content

    def _scenario_core_titles(self):
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
            properties = reader.read_from_file(constants.SCENARIO_FILE_PROPERTIES)
            scenario_titles.append(properties[constants.ScenarioProperty.TITLE])

        # zip files and titles together
        scenarios = zip(scenario_titles, scenario_files)

        # sort them
        scenarios = sorted(scenarios)  # default sort order is by first element anyway

        return scenarios

    def scenario_preview(self, scenario_file_name):
        """
        A client got a message on the constants.C.SCENARIO_PREVIEW channel. In the message should be a scenario file name
        (key = 'scenario'). Assemble a preview and send it back.
        """
        t0 = time.clock()

        # TODO existing? can be loaded?
        scenario = ServerScenario.from_file(scenario_file_name)
        logger.info('reading of the file took {}s'.format(time.clock() - t0))

        preview = {'scenario': scenario_file_name}

        # some scenario properties should be copied
        scenario_copy_keys = [constants.ScenarioProperty.MAP_COLUMNS,
                              constants.ScenarioProperty.MAP_ROWS,
                              constants.ScenarioProperty.TITLE,
                              constants.ScenarioProperty.DESCRIPTION]
        for key in scenario_copy_keys:
            preview[key] = scenario[key]

        # some nations properties should be copied
        nations = {}
        nation_copy_keys = [constants.NationProperty.COLOR,
                            constants.NationProperty.NAME,
                            constants.NationProperty.DESCRIPTION]
        for nation in scenario.nations():
            nations[nation] = {}
            for key in nation_copy_keys:
                nations[nation][key] = scenario.nation_property(nation, key)
        preview['nations'] = nations

        # assemble a nations map (-1 means no nation)
        columns = scenario[constants.ScenarioProperty.MAP_COLUMNS]
        rows = scenario[constants.ScenarioProperty.MAP_ROWS]
        nations_map = [-1] * (columns * rows)
        for nation_id in scenario.nations():
            provinces = scenario.provinces_of_nation(nation_id)
            for province in provinces:
                tiles = scenario.province_property(province, constants.ProvinceProperty.TILES)
                for column, row in tiles:
                    nations_map[row * columns + column] = nation_id
        preview['map'] = nations_map

        logger.info('generating preview took {}s'.format(time.clock() - t0))

        return preview
