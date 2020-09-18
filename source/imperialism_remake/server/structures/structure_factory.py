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
from imperialism_remake.server.server_scenario import ServerScenario
from imperialism_remake.server.structures.structure_farm_elevator import StructureFarmElevator
from imperialism_remake.server.structures.structure_warehouse import StructureWarehouse


class StructureFactory:
    @staticmethod
    def create_new_structure(server_scenario: ServerScenario, uuid: uuid.uuid4, row: int, column: int,
                             structure_type: StructureType) -> Structure:
        if structure_type == StructureType.FARM_ELEVATOR:
            return StructureFarmElevator(server_scenario, uuid, row, column)
        elif structure_type == StructureType.WAREHOUSE:
            return StructureWarehouse(server_scenario, uuid, row, column)
