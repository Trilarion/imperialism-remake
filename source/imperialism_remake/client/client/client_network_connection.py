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

from imperialism_remake.base import constants, tools
from imperialism_remake.base.network import NetworkClient

logger = logging.getLogger(__name__)


class ClientNetworkConnection:
    def __init__(self, network_client):
        self._network_client = network_client

    def connect_to_system(self, callback):
        logger.debug('connect_to_system')
        self._network_client.connect_to_channel(constants.C.SYSTEM, callback)

    def request_monitor_update_from_system(self):
        """
        Sends a request for an update of the system monitor.
        """
        logger.debug('request_monitor_update_from_system')
        self._network_client.send(constants.C.SYSTEM, constants.M.SYSTEM_MONITOR_UPDATE)

    def disconnect_from_system(self, callback):
        logger.debug('disconnect_from_system')
        self._network_client.disconnect_from_channel(constants.C.SYSTEM, callback)

    def stop(self):
        logger.debug('stop')
        self._network_client.send(constants.C.SYSTEM, constants.M.SYSTEM_SHUTDOWN)
        # TODO is this okay, is there a better way
        self._network_client.socket.flush()

    def start(self):
        logger.debug('start')
        self._network_client.connect_to_host(constants.NETWORK_PORT)
        # TODO what if this is not possible
        # that should always be possible, if not, we should try again, and then throw an error

    def connect_to_lobby(self, callback):
        logger.debug('connect_to_lobby')
        self._network_client.connect_to_channel(constants.C.LOBBY, callback)

    def request_scenario_list_from_lobby(self):
        logger.debug('request_scenario_list_from_lobby')
        self._network_client.send(constants.C.LOBBY, constants.M.LOBBY_SCENARIO_CORE_LIST)

    def request_scenario_preview_from_lobby(self, scenario_file):
        logger.debug('request_scenario_preview_from_lobby')
        self._network_client.send(constants.C.LOBBY, constants.M.LOBBY_SCENARIO_PREVIEW, scenario_file)

    def disconnect_from_lobby(self, callback):
        logger.debug('disconnect_from_lobby')
        self._network_client.disconnect_from_channel(constants.C.LOBBY, callback)

    def connect_to_game(self, callback):
        logger.debug('connect_to_game')
        self._network_client.connect_to_channel(constants.C.GAME, callback)

    def request_turn_process_for_game(self, request):
        logger.debug('request_turn_process_for_game')
        self._network_client.send(constants.C.GAME, constants.M.GAME_TURN_PROCESS_REQUEST, request)

    def request_game_to_save(self, file_name):
        logger.debug('request_game_to_save:%s', file_name)
        self._network_client.send(constants.C.SYSTEM, constants.M.GAME_SAVE_REQUEST, file_name)

    def send_game_to_load(self, filename):
        logger.debug('send_game_to_load')
        self._network_client.send(constants.C.SYSTEM, constants.M.GAME_LOAD_REQUEST, filename)

    def disconnect_from_game(self, callback):
        logger.debug('disconnect_from_game')
        self._network_client.disconnect_from_channel(constants.C.GAME, callback)

    def connect_to_chat(self, callback):
        logger.debug('connect_to_chat')
        self._network_client.connect_to_channel(constants.C.CHAT, callback)
        self._network_client.send(constants.C.CHAT, constants.M.CHAT_SUBSCRIBE)

    def send_message_to_chat(self, chat_message):
        logger.debug('send_message_to_chat:%s', chat_message)
        self._network_client.send(constants.C.CHAT, constants.M.CHAT_MESSAGE, chat_message)

    def request_client_list_for_chat(self):
        """
        Sends a request to get an updated connected client list.
        """
        logger.debug('request_client_list_for_chat')
        self._network_client.send(constants.C.LOBBY, constants.M.LOBBY_CONNECTED_CLIENTS)

    def disconnect_from_chat(self, callback):
        logger.debug('disconnect_from_chat')
        self._network_client.send(constants.C.CHAT, constants.M.CHAT_UNSUBSCRIBE)
        self._network_client.disconnect_from_channel(constants.C.CHAT, callback)

    def is_connected(self):
        return self._network_client.is_connected()

    def get_peer_address(self):
        return self._network_client.peer_address()

    def send_client_name(self):
        logger.debug('send_client_name')
        self._network_client.send(constants.C.GENERAL, constants.M.GENERAL_NAME,
                                  tools.get_option(constants.Option.LOCALCLIENT_NAME))


network_connection = ClientNetworkConnection(NetworkClient())
