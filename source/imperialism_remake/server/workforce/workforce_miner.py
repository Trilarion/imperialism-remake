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
from imperialism_remake.server.models.structure_type import StructureType
from imperialism_remake.server.models.technology_type import TechnologyType
from imperialism_remake.server.models.terrain_resource_type import TerrainResourceType
from imperialism_remake.server.models.turn_planned import TurnPlanned
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.server_scenario import ServerScenario
from imperialism_remake.server.workforce.workforce_common import WorkforceCommon


class WorkforceMiner(WorkforceCommon):
    def __init__(self, server_scenario: ServerScenario, turn_planned: TurnPlanned, workforce):
        _tech_to_structure_level_map = {
            TerrainResourceType.ORE.value: {
                1: TechnologyType.MINER_MINE_LEVEL1,
                2: TechnologyType.MINER_MINE_LEVEL2,
                3: TechnologyType.MINER_MINE_LEVEL3},
            TerrainResourceType.COAL.value: {
                1: TechnologyType.MINER_MINE_LEVEL1,
                2: TechnologyType.MINER_MINE_LEVEL2,
                3: TechnologyType.MINER_MINE_LEVEL3
            }
        }

        super().__init__(server_scenario, turn_planned, workforce, _tech_to_structure_level_map)

    def _can_build_or_upgrade(self, new_column, new_row, workforce_action, structure_type):
        if workforce_action == WorkforceAction.DUTY_ACTION:
            for prospector_resource_id, prospector_resource_state in self._server_scenario.get_nation_prospector_resource_state(
                    self._workforce.get_nation(), new_row, new_column).items():
                structures = self._server_scenario.get_structures_at(new_row, new_column)
                if structures is not None:
                    for structure in structures:
                        if structure.get_type() == structure_type:
                            return structure.can_upgrade() and self._is_upgrade_allowed(prospector_resource_id,
                                                                                        structure.get_level())
                return self._is_upgrade_allowed(prospector_resource_id, 0)
        return True

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction) -> bool:
        is_action_allowed = super().is_action_allowed(new_row, new_column, workforce_action)
        if not is_action_allowed:
            return False

        return self._can_build_or_upgrade(new_column, new_row, workforce_action, StructureType.MINE)
