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

from PyQt5 import QtCore

from imperialism_remake.base import constants
from imperialism_remake.base.network import local_network_client
from imperialism_remake.server.models.turn_planned import TurnPlanned
from imperialism_remake.server.models.turn_result import TurnResult
from imperialism_remake.server.models.workforce import Workforce
from imperialism_remake.server.server_network_client import ServerNetworkClient
from imperialism_remake.server.structures.structure_factory import StructureFactory
from imperialism_remake.server.workforce.workforce_factory import WorkforceFactory

logger = logging.getLogger(__name__)


class TurnManager(QtCore.QObject):
    event_turn_completed = QtCore.pyqtSignal(TurnResult)

    def __init__(self, scenario):
        super().__init__()

        self._scenario = scenario
        self._turn_planned = TurnPlanned()

        local_network_client.connect_to_channel(constants.C.GAME, self._game_message_received)

    def get_turn_planned(self) -> TurnPlanned:
        return self._turn_planned

    def make_turn(self) -> None:
        logger.debug("make_turn start")

        logger.debug("send next planned state for workforces: %s", self._turn_planned.get_workforces())
        self._send_turn_planned_to_server(self._turn_planned)

        logger.debug("turn planned")

    def _process_turn_result(self, turn_result) -> None:
        logger.debug("_process_turn_result")

        del self._turn_planned
        self._turn_planned = TurnPlanned()

        for w_id, w in turn_result.get_workforces().items():
            workforce = WorkforceFactory.create_new_workforce(self._scenario.server_scenario, self._turn_planned, w)
            self._turn_planned.add_workforce(workforce)
            turn_result.get_workforces()[workforce.get_id()] = workforce

        for s_id, s in turn_result.get_structures().items():
            structure = StructureFactory.create_new_structure(self._scenario.server_scenario, s)
            turn_result.get_structures()[s.get_id()] = structure

        self.event_turn_completed.emit(turn_result)

    def _send_turn_planned_to_server(self, turn_planned: TurnPlanned):
        logger.debug("_send_message_to_server send message:%s", turn_planned)

        local_network_client.send(constants.C.GAME, constants.M.GAME_TURN_PROCESS_REQUEST, turn_planned)

    def _game_message_received(self, client: ServerNetworkClient, channel: constants.C, action: constants.M, content):
        logger.debug("_game_message_received send message action:%s, content:%s", action, content)
        if action == constants.M.GAME_TURN_PROCESS_RESPONSE:
            self._process_turn_result(content)
