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
from imperialism_remake.server.models.turn import Turn
from imperialism_remake.server.models.workforce import Workforce
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.models.workforce_type import WorkforceType
from imperialism_remake.server.server_scenario import ServerScenario


class WorkforceCommon(Workforce):
    def __init__(self, server_scenario: ServerScenario, turn: Turn, workforce_id: uuid, row: int, column: int,
                 workforce_type: WorkforceType):
        super().__init__(workforce_id, row, column, workforce_type)

        self._server_scenario = server_scenario
        self._turn = turn

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
            super().plan_action(new_row, new_column, workforce_action)

            self._turn.add_workforce(self)
        else:
            if workforce_action == WorkforceAction.DUTY_ACTION:
                if self.is_action_allowed(new_row, new_column, WorkforceAction.MOVE):
                    super().plan_action(new_row, new_column, WorkforceAction.MOVE)

                    self._turn.add_workforce(self)

    def cancel_action(self) -> None:
        super().cancel_action()

        self._turn.remove_workforce(self)

    def _is_tech_allowed_on_map(self, terrain_type_on_map: int, terrain_type_for_tech: int,
                                technology_type: TechnologyType) -> bool:
        if terrain_type_on_map == terrain_type_for_tech and self._server_scenario.is_technology_available(
                technology_type):
            return True
        return False
