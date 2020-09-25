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

from imperialism_remake.server.models.structure import Structure
from imperialism_remake.server.models.structure_type import StructureType
from imperialism_remake.server.models.terrain_type import TerrainType
from imperialism_remake.server.server_scenario import ServerScenario


class StructureCommon:
    def __init__(self, server_scenario: ServerScenario, structure: Structure):
        self._structure = structure
        self._server_scenario = server_scenario

    def can_build(self, row, column) -> bool:
        if column < 0 or row < 0:
            return False

        terrain_type = self._server_scenario.terrain_at(column, row)
        if terrain_type == TerrainType.SEA.value:
            return False

        return True

    def get_id(self) -> uuid:
        return self._structure.get_id()

    def get_type(self) -> StructureType:
        return self._structure.get_type()

    def get_position(self) -> (int, int):
        return self._structure.get_position()

    def get_level(self) -> int:
        return self._structure.get_level()

    def can_upgrade(self) -> bool:
        if self._structure.get_level() > self._structure.get_max_level():
            return False
        return True

    def upgrade(self) -> None:
        if self.can_upgrade():
            self._structure.set_level(self._structure.get_level() + 1)
