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
from imperialism_remake.server.models.raw_resource_type import RawResourceType
from imperialism_remake.server.models.technology_type import TechnologyType
from imperialism_remake.server.models.terrain_type import TerrainType
from imperialism_remake.server.models.turn_planned import TurnPlanned
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.server_scenario import ServerScenario
from imperialism_remake.server.workforce.workforce_common import WorkforceCommon


class WorkforceProspector(WorkforceCommon):
    def __init__(self, server_scenario: ServerScenario, turn_planned: TurnPlanned, workforce):
        super().__init__(server_scenario, turn_planned, workforce)

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction) -> bool:
        is_action_allowed = super().is_action_allowed(new_row, new_column, workforce_action)
        if not is_action_allowed:
            return False

        if workforce_action == WorkforceAction.DUTY_ACTION:
            tile_action_allowed = self._is_tile_duty_action_allowed(new_column, new_row)

            return tile_action_allowed
        return True

    def _is_tile_duty_action_allowed(self, new_column, new_row):
        terrain_type = self._server_scenario.terrain_at(new_column, new_row)
        tech_allowed = self._is_tech_allowed_on_map(terrain_type, TerrainType.HILLS.value,
                                                    TechnologyType.PROSPECTOR_WORK_HILLS) or self._is_tech_allowed_on_map(
            terrain_type, TerrainType.MOUNTAINS.value,
            TechnologyType.PROSPECTOR_WORK_MOUNTAIN) or self._is_tech_allowed_on_map(terrain_type,
                                                                                     TerrainType.SWAMP.value,
                                                                                     TechnologyType.PROSPECTOR_WORK_SWAMP)
        raw_resource_type = self._server_scenario.get_raw_resource_type(new_row, new_column)
        not_minable_raw_resource = raw_resource_type is not None and raw_resource_type != RawResourceType.COAL and raw_resource_type != RawResourceType.ORE

        return tech_allowed and not not_minable_raw_resource
