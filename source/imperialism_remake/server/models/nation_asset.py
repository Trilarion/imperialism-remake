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

from imperialism_remake.server.models.goods import Goods
from imperialism_remake.server.models.materials import Materials
from imperialism_remake.server.models.raw_resource_type import RawResourceType
from imperialism_remake.server.models.workforce import Workforce


class NationAsset:
    def __init__(self, nation_id: uuid):
        self._nation_id = nation_id

        self._workforces = {}
        self._raw_resources = {}
        self._materials = {}
        self._goods = {}

        # TODO what are default resources values?
        for raw_resource in RawResourceType:
            self._raw_resources[raw_resource] = 0
        for material in Materials:
            self._materials[material] = 0
        for good in Goods:
            self._goods[good] = 0

        # This is coordinates for each of resources/workforces
        self.asset_locations = {}

    def get_nation_id(self) -> uuid:
        return self._nation_id

    def add_or_update_workforce(self, workforce: Workforce) -> None:
        self._workforces[workforce.get_id()] = workforce

        row, column = workforce.get_current_position()
        if row not in self.asset_locations:
            self.asset_locations[row] = {}
        self.asset_locations[row][column] = workforce

    def delete_workforce(self, workforce: Workforce) -> None:
        if workforce.get_id() in self._workforces:
            del self._workforces[workforce.get_id()]

    def get_raw_resources(self) -> {}:
        return self._raw_resources

    def get_materials(self) -> {}:
        return self._materials

    def get_goods(self) -> {}:
        return self._goods

    def get_workforces(self) -> {}:
        return self._workforces
