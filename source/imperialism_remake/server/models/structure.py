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

from imperialism_remake.server.models.structure_type import StructureType


class Structure:
    def __init__(self, structure_id: uuid, row: int, column: int, structure_type: StructureType, raw_resource_type,
                 max_level):
        self._structure_id = structure_id
        self._structure_type = structure_type

        self._row = row
        self._column = column

        self._level = 1
        self._max_level = max_level

        self._raw_resource_type = raw_resource_type

        # Overriden in inherited workforce class implementations
        self._build_expenses = None

    def get_id(self) -> uuid:
        return self._structure_id

    def get_type(self) -> StructureType:
        return self._structure_type

    def get_position(self) -> (int, int):
        return self._row, self._column

    def get_level(self) -> int:
        return self._level

    def set_level(self, level) -> None:
        self._level = level

    def get_max_level(self) -> int:
        return self._max_level

    def get_raw_resource_type(self):
        return self._raw_resource_type
