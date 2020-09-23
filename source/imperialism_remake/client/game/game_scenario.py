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

"""
GUI and internal working of the scenario editor. This is also partly of the client but since the client should not
know anything about the scenario, we put it in the server module.
"""
import logging
import os

from imperialism_remake.client.client.client_network_connection import network_connection
from imperialism_remake.client.common.generic_scenario import GenericScenario
from imperialism_remake.server.server_scenario import ServerScenario

logger = logging.getLogger(__name__)


class GameScenario(GenericScenario):
    def init(self, server_base_scenario):
        logger.debug("init")

        self.server_scenario = ServerScenario(server_base_scenario)

        self._init()

    def load(self, file_name):
        """
        :param file_name:
        """
        logger.debug('load file_name:%s', file_name)

        if os.path.isfile(file_name):
            network_connection.send_game_to_load({'filename': file_name, 'nation': -1})

    def save(self, file_name):
        """
        :param file_name:
        """
        logger.debug('save file_name:%s', file_name)

        network_connection.request_game_to_save(file_name)
