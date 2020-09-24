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
import uuid

from imperialism_remake.server.models.technology_type import TechnologyType
from imperialism_remake.server.models.terrain_type import TerrainType
from imperialism_remake.server.models.turn_planned import TurnPlanned
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.models.workforce_type import WorkforceType
from imperialism_remake.server.server_scenario import ServerScenario


class WorkforceCommon:
    def __init__(self, server_scenario: ServerScenario, turn_planned: TurnPlanned, workforce):
        self._workforce = workforce
        self._server_scenario = server_scenario
        self._turn_planned = turn_planned

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction) -> bool:
        if new_column < 0 or new_row < 0:
            return False

        terrain_type = self._server_scenario.terrain_at(new_column, new_row)
        if terrain_type == TerrainType.SEA.value:
            return False

        return True

    def get_name(self) -> str:
        return self._server_scenario.get_workforce_settings()[self.get_type().value]['name']

    def plan_action(self, new_row: int, new_column: int, workforce_action: WorkforceAction) -> None:
        if self.is_action_allowed(new_row, new_column, workforce_action):
            self._workforce.plan_action(new_row, new_column, workforce_action)

            self._turn_planned.add_workforce(self._workforce)
        else:
            if workforce_action == WorkforceAction.DUTY_ACTION:
                if self.is_action_allowed(new_row, new_column, WorkforceAction.MOVE):
                    self._workforce.plan_action(new_row, new_column, WorkforceAction.MOVE)

                    self._turn_planned.add_workforce(self._workforce)

    def cancel_action(self) -> None:
        self._workforce.cancel_action()

        self._turn_planned.remove_workforce(self._workforce)

    def _is_tech_allowed_on_map(self, type_on_map: int, type_for_tech: int,
                                technology_type: TechnologyType) -> bool:
        if type_on_map == type_for_tech and self._server_scenario.is_technology_available(
                technology_type):
            return True
        return False

    def get_id(self) -> uuid:
        return self._workforce.get_id()

    def get_type(self) -> WorkforceType:
        return self._workforce.get_type()

    def get_action(self) -> WorkforceAction:
        return self._workforce.get_action()

    def get_new_position(self) -> (int, int):
        return self._workforce.get_new_position()

    def get_current_position(self) -> (int, int):
        return self._workforce.get_current_position()
