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
from imperialism_remake.server.models.structure_type import StructureType


class ResourceCalculator:
    def __init__(self, server_scenario, nation_id, old_roads, old_structures):
        self._server_scenario = server_scenario
        self._nation_id = nation_id
        self._old_roads = old_roads
        self._old_structures = old_structures
        self._capital_col, self._capital_row = self._server_scenario.get_capital_position(self._nation_id)

        self._produced_raw_resources = {}

    def calculate(self):
        self._calculate_produced_raw_resources()

    def _calculate_produced_raw_resources(self):
        forward_road_hash_map = {}
        backward_road_hash_map = {}
        for start, stop in self._old_roads:
            if start not in forward_road_hash_map:
                forward_road_hash_map[start] = [stop]
            else:
                forward_road_hash_map[start].append(stop)

            if stop not in backward_road_hash_map:
                backward_road_hash_map[stop] = [start]
            else:
                backward_road_hash_map[stop].append(start)

        def __get_wh_structure(structures, position):
            if position[0] in structures and position[1] in structures[position[0]]:
                for structure in structures[position[0]][position[1]]:
                    if structure.get_type() == StructureType.WAREHOUSE:
                        return structures[position[0]][position[1]]
            else:
                return None

        def __get_not_wh_structure(structures, position):
            if position[0] in structures and position[1] in structures[position[0]]:
                for structure in structures[position[0]][position[1]]:
                    if structure.get_type() != StructureType.WAREHOUSE:
                        return structures[position[0]][position[1]]
            else:
                return None

        def __add_neighbor_not_wh_structures(capital_reachable_structures, position):
            for neighbour_tile in self._server_scenario.neighbored_tiles(position[1], position[0]):
                __add_not_wh_structure(capital_reachable_structures, neighbour_tile)

        def __add_not_wh_structure(capital_reachable_structures, neighbour_tile):
            not_wh = __get_not_wh_structure(self._old_structures, (neighbour_tile[1], neighbour_tile[0]))
            if not_wh is not None and not_wh[0] not in capital_reachable_structures:
                capital_reachable_structures.add(not_wh[0])

        capital_reachable_warehouses = []
        queue = [(self._capital_row, self._capital_col)]
        visited = set()
        visited.add((self._capital_row, self._capital_col))
        while len(queue) > 0:
            road_part = queue.pop()
            if road_part in forward_road_hash_map:
                structure = __get_wh_structure(self._old_structures, road_part)
                if structure is not None:
                    capital_reachable_warehouses.append(structure)
                for road_other_part in forward_road_hash_map[road_part]:
                    if road_other_part not in visited:
                        queue.insert(0, road_other_part)
                        visited.add(road_other_part)
            if road_part in backward_road_hash_map:
                structure = __get_wh_structure(self._old_structures, road_part)
                if structure is not None:
                    capital_reachable_warehouses.append(structure)
                for road_other_part in backward_road_hash_map[road_part]:
                    if road_other_part not in visited:
                        queue.insert(0, road_other_part)
                        visited.add(road_other_part)

        capital_reachable_structures = set()
        for wh in capital_reachable_warehouses:
            position = wh[0].get_position()
            __add_not_wh_structure(capital_reachable_structures, position)
            __add_neighbor_not_wh_structures(capital_reachable_structures, position)

        __add_neighbor_not_wh_structures(capital_reachable_structures,
                                         (self._capital_row, self._capital_col))

        for structure in capital_reachable_structures:
            raw_resource_type = structure.get_raw_resource_type()
            if raw_resource_type not in self._produced_raw_resources:
                self._produced_raw_resources[raw_resource_type] = 0
            self._produced_raw_resources[raw_resource_type] += structure.get_level()

    def update_raw_resources(self, raw_resources):
        for name, raw_resource in self._produced_raw_resources.items():
            raw_resources[name] += raw_resource