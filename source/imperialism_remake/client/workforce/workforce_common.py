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

from imperialism_remake.server.models.terrain_type import TerrainType
from imperialism_remake.server.models.workforce import Workforce
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.models.workforce_type import WorkforceType


class WorkforceCommon(Workforce):
    def __init__(self, server_scenario, workforce_id, row, column, workforce_type: WorkforceType):
        super().__init__(workforce_id, row, column, workforce_type)

        self._server_scenario = server_scenario

    def is_action_allowed(self, new_column, new_row, workforce_action: WorkforceAction):
        if self._row < 0 or self._column < 0:
            return False

        terrain_type = self._server_scenario.terrain_at(new_column, new_row)
        if terrain_type == TerrainType.SEA:
            return False

    def get_name(self):
        return self._server_scenario.get_workforce_settings()[self.get_type().value]['name']


