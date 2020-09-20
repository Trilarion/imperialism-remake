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
import uuid

from imperialism_remake.server.models.structure import Structure
from imperialism_remake.server.models.structure_type import StructureType
from imperialism_remake.server.models.turn_result import TurnResult
from imperialism_remake.server.models.workforce import Workforce
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.models.workforce_type import WorkforceType

logger = logging.getLogger(__name__)


class ServerTurnProcessor:
    def __init__(self):
        self._clients = []
        self._clients_turn_planned = {}
        self._turn_processing_finished_event_handler = None

    def client_turn_ended(self, client, turn_planned):
        logger.debug('client_turn_ended: %s', client)
        self._clients_turn_planned[client.client_id] = turn_planned

        if len(self._clients_turn_planned) == len(self._clients):
            self._process_turn()

    def set_turn_processing_finished_event_handler(self, turn_processing_finished_event_handler):
        self._turn_processing_finished_event_handler = turn_processing_finished_event_handler

    def add_client(self, client):
        logger.debug('add_client: %s', client)
        self._clients.append(client)

    def _process_turn(self):
        logger.debug('_process_turn for %s clients', len(self._clients))

        common_turn_result = self._get_common_turn_result()

        for client in self._clients:
            personal_turn_result = self._get_personal_turn_result(client)

            self._turn_processing_finished_event_handler(client, common_turn_result)
            self._turn_processing_finished_event_handler(client, personal_turn_result)

    def _get_personal_turn_result(self, client):
        personal_turn_result = TurnResult()

        old_workforces = self._clients_turn_planned[client.client_id].get_workforces()
        for k, w in old_workforces.items():
            r, c = w.get_new_position()
            # Move worker to new position
            personal_turn_result.get_workforces()[w.get_id()] = Workforce(w.get_id(), r, c, w.get_type())

            if w.get_action() == WorkforceAction.DUTY_ACTION:
                if w.get_type() == WorkforceType.GEOLOGIST:
                    self._process_geologist(c, r, personal_turn_result, w)

        return personal_turn_result

    def _get_common_turn_result(self):
        turn_result = TurnResult()
        for client in self._clients:
            old_workforces = self._clients_turn_planned[client.client_id].get_workforces()

            for k, w in old_workforces.items():
                r, c = w.get_new_position()

                if w.get_action() == WorkforceAction.DUTY_ACTION:
                    if w.get_type() == WorkforceType.ENGINEER:
                        self._process_engineer(c, r, turn_result, w)
        return turn_result

    def _process_engineer(self, c, r, turn_result, w):
        logger.debug('_process_engineer c:%s, r:%s', c, r)

        # add roads
        old_r, old_c = w.get_current_position()
        if old_r != r or old_c != c:
            # TODO we must add road to server scenario on server, but where is our server scenario instance on server???
            # self._server_scenario.add_road((r, c), (old_r, old_c))
            turn_result.get_roads().append(((r, c), (old_r, old_c)))

        # add structures
        if old_r == r and old_c == c:
            wh = Structure(uuid.uuid4(), r, c, StructureType.WAREHOUSE)
            # TODO we must add structure to server scenario on server, but where is our server scenario instance on server???
            # self._scenario.server_scenario.add_structure(r, c, wh)
            turn_result.get_structures()[wh.get_id()] = wh

    def _process_geologist(self, c, r, turn_result, w):
        logger.debug('_process_geologist c:%s, r:%s', c, r)
