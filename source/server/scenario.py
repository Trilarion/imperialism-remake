# Imperialism remake
# Copyright (C) 2014-16 Trilarion
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

"""
    Defines a scenario, can be loaded and saved. Should only be known to the server, never to the client (which is a
    thin client).
"""

import math

from PyQt5 import QtCore

import base.constants as constants
import lib.utils as utils

# TODO rivers are implemented inefficiently

class Scenario(QtCore.QObject):
    """
        Has several dictionaries (properties, provinces, nations) and a list (map) defining everything.

        _properties is a dictionary with keys from constants.ScenarioProperties
        _provinces is a
        _nations is a
        _maps is a dictionary of different maps (terrain, resource)
        _rules is a dictionary of rules properties
    """

    def __init__(self):
        """
            Start with a clean state.
        """
        super().__init__()
        self.reset()

    # noinspection PyAttributeOutsideInit
    def reset(self):
        """
            Just empty
        """
        self._properties = {constants.ScenarioProperties.RIVERS: []}
        self._provinces = {}
        self._nations = {}
        self._maps = {}
        self._rules = {}

    def create_empty_map(self, columns, rows):
        """
            Given a size, constructs a map (list of two sub lists with each the number of tiles entries) which is 0.
        """
        self._properties[constants.ScenarioProperties.MAP_COLUMNS] = columns
        self._properties[constants.ScenarioProperties.MAP_ROWS] = rows
        number_tiles = columns * rows
        self._maps['terrain'] = [0] * number_tiles
        self._maps['resource'] = [0] * number_tiles

    def add_river(self, name, tiles):
        """
            Adds a river with a list of tiles and a name.
            TODO this is inefficient
        """
        river = {'name': name, 'tiles': tiles}
        self._properties[constants.ScenarioProperties.RIVERS].extend([river])

    def set_terrain_at(self, column, row, terrain):
        """
            Sets the terrain at a given position. No check is performed for valid terrain.
        """
        self._maps['terrain'][self._map_index(column, row)] = terrain

    def terrain_at(self, column, row):
        """
            Returns the terrain at a given position of the map.
        """
        return self._maps['terrain'][self._map_index(column, row)]

    def set_resource_at(self, column, row, resource):
        """
            Sets the resource value at a given position. No check is performed for valid resources.
        """
        self._maps['resource'][self._map_index(column, row)] = resource

    def resource_at(self, column, row):
        """
            Returns the resource value at a given position of the map.
        """
        return self._maps['resource'][self._map_index(column, row)]

    def map_position(self, x, y):
        """
            Converts a scene position to a map position (or return (-1,-1) if outside of the possible coordinates.

            A scene position is the position in the QGraphicsScene containing the map view and normalized by
            the tile size. The reason this conversion is done here is that the knowledge about the direction of the
            shift of each second row is kept only here at the scenario and not spread out.

            Each second row is shifted right (positive) by one half, starting with the second.
        """
        row = math.floor(y)
        column = math.floor(x - (row % 2) / 2)
        if row < 0 or row >= self._properties[constants.ScenarioProperties.MAP_ROWS] or column < 0 or column >= \
                self._properties[constants.ScenarioProperties.MAP_COLUMNS]:
            return -1, -1
        return column, row

    @staticmethod
    def scene_position(column, row):
        """
            Converts a map position to a scene position. A scene position is the the normalized (by the tile size)
            position of the upper, left corner of a map tile at position (column, row).

            Each second row is shifted right (positive) by one half, starting with the second.
            Columns and rows start at zero.
        """
        return column + (row % 2) / 2, row

    def _map_index(self, column, row):
        """
            Internal function. Calculates the index in the linear map for a given 2D position (first row, then column)?
        """
        index = row * self._properties[constants.ScenarioProperties.MAP_COLUMNS] + column
        return index

    def get_neighbor_position(self, column, row, direction):
        """
            Given a position (column, row) and a direction (see constants.TileDirections) return the position of the
            next neighbour tile in that direction given our staggered tile layout where the second and all other odd
            rows are shifted half a tile to the right (positive). Returns None if we would be outside of the map area.
        """
        if direction is constants.TileDirections.WEST:
            # west
            if column > 0:
                return [column - 1, row]
            else:
                return None
        elif direction is constants.TileDirections.NORTH_WEST:
            # north-west
            if row > 0:
                if row % 2 == 0:
                    # even rows (0, 2, 4, ..)
                    return [column - 1, row - 1]
                else:
                    # odd rows (1, 3, 5, ..)
                    return [column, row - 1]
            else:
                return None
        elif direction is constants.TileDirections.NORTH_EAST:
            # north-east
            if row > 0:
                if row % 2 == 0:
                    # even rows (0, 2, 4, ..)
                    return [column, row - 1]
                else:
                    # odd rows (1, 3, 5, ..)
                    return [column + 1, row - 1]
            else:
                return None
        elif direction is constants.TileDirections.EAST:
            # east
            if column < self._properties[constants.ScenarioProperties.MAP_COLUMNS] - 1:
                return [column + 1, row]
            else:
                return None
        elif direction is constants.TileDirections.SOUTH_EAST:
            # south-east
            if row < self._properties[constants.ScenarioProperties.MAP_ROWS] - 1:
                if row % 2 == 0:
                    # even rows (0, 2, 4, ..)
                    return [column, row + 1]
                else:
                    # odd rows (1, 3, 5, ..)
                    return [column + 1, row + 1]
            else:
                return None
        elif direction is constants.TileDirections.SOUTH_WEST:
            # south-west
            if row < self._properties[constants.ScenarioProperties.MAP_ROWS] - 1:
                if row % 2 == 0:
                    # even rows (0, 2, 4, ..)
                    return [column - 1, row + 1]
                else:
                    # odd rows (1, 3, 5, ..)
                    return [column, row + 1]
            else:
                return None

    def get_neighbored_tiles(self, column, row):
        """
            For all directions, get all neighbored tiles. Just executes get_neighbor_position() for all possible
            TileDirections
        """
        tiles = []
        for direction in constants.TileDirections:
            tiles.append(self.get_neighbor_position(column, row, direction))
        return tiles

    def __setitem__(self, key, value):
        """
            Given a key and a value, sets a scenario property.
        """
        self._properties[key] = value

    def __getitem__(self, key):
        """
            Given a key, returns a scenario property. One can only obtain properties that have been set before.
        """
        if key in self._properties:
            return self._properties[key]
        else:
            raise RuntimeError('Unknown property {}.'.format(key))

    def create_new_province(self):
        """
            Creates a new (nation-less) province and returns the id of it.
        """
        province = len(self._provinces)  # this always works because we check after loading the integrity of the keys
        # TODO unless we delete provinces, some more checks might be good here (like first non-used)
        self._provinces[province] = {}
        self._provinces[province][constants.ProvinceProperties.TILES] = []
        self._provinces[province][constants.ProvinceProperties.NATION] = None
        return province

    def set_province_property(self, province, key, value):
        """
            Sets a province property.
        """
        if province in self._provinces:
            self._provinces[province][key] = value
        else:
            raise RuntimeError('Unknown province {}.'.format(province))

    def get_province_property(self, province, key):
        """
            Gets a province property. One can only obtain properties that have been set before and only for provinces
            that exist.
        """
        if province in self._provinces and key in self._provinces[province]:
            return self._provinces[province][key]
        else:
            raise RuntimeError('Unknown province {} or property {}.'.format(province, key))

    def add_province_map_tile(self, province, position):
        """
            Adds a position to a province.
            TODO we should check that this position is not yet in another province (it should be cleared before). fail fast, fail often
        """
        if province in self._provinces and self.is_valid_position(position):
            self._provinces[province][constants.ProvinceProperties.TILES].append(position)

    def all_nations(self):
        """
            Return a list of ids for all nations.
        """
        return self._nations.keys()

    def create_new_nation(self):
        """
            Add a new nation and returns it.
        """
        nation = len(self._nations)  # this always gives a new unique number because we check after loading
        # TODO as long as we do not delete nations, some more checks here might be good
        self._nations[nation] = {}
        self._nations[nation][constants.NationProperties.PROVINCES] = []
        return nation

    def set_nation_property(self, nation, key, value):
        """
            Set nation property.
        """
        if nation in self._nations:
            self._nations[nation][key] = value
        else:
            raise RuntimeError('Unknown nation {}.'.format(nation))

    def get_nation_property(self, nation, key):
        """
            Gets a nation property. One can only obtain properties that have been set before and only for nations
            that exist.
        """
        if nation in self._nations and key in self._nations[nation]:
            return self._nations[nation][key]
        else:
            raise RuntimeError('Unknown nation {} or property {}.'.format(nation, key))

    def get_provinces_of_nation(self, nation):
        """
            Return ids for all provinces in a nation.
        """
        if nation in self._nations:
            return self._nations[nation][constants.NationProperties.PROVINCES]
        else:
            raise RuntimeError('Unknown nation {}.'.format(nation))

    def get_province_at(self, column, row):
        """
            Given a position (column, row) returns the province.

            TODO speed up by having a reference in the map. (see also programmers.SE question)
        """
        position = [column, row]
        for province in self._provinces:
            if position in self._provinces[province][constants.ProvinceProperties.TILES]:
                return province
        return None

    def transfer_province_to_nation(self, province, nation):
        """
            Moves a province to a nation.
        """
        # TODO this is not right yet
        # wire it in both ways
        self._nations[nation][constants.NationProperties.PROVINCES].append(province)
        self._provinces[province][constants.ProvinceProperties.NATION] = nation

    def get_terrain_name(self, terrain):
        """
            Get a special property from the rules.

            TODO move this to a special rules class. Only have rules() and setRules() here.
        """
        return self._rules['terrain.names'][terrain]

    def load(self, file_name):
        """
            Load/deserialize all internal variables from a zipped archive via YAML.
        """

        # so we can do that also during game play, we reset
        self.reset()

        reader = utils.ZipArchiveReader(file_name)

        self._properties = reader.read_as_yaml(constants.SCENARIO_FILE_PROPERTIES)
        self._maps = reader.read_as_yaml(constants.SCENARIO_FILE_MAPS)
        self._provinces = reader.read_as_yaml(constants.SCENARIO_FILE_PROVINCES)
        # TODO check all ids are smaller then len()

        self._nations = reader.read_as_yaml(constants.SCENARIO_FILE_NATIONS)
        # TODO check all ids are smaller then len()

        # read rule file
        # TODO how to specify which rules file apply
        rule_file = constants.extend(constants.SCENARIO_RULESET_FOLDER, self._properties['rules'])
        self._rules = utils.read_as_yaml(rule_file)

    def save(self, file_name):
        """
            Saves/serializes all internal variables via YAML into a zipped archive.
        """
        writer = utils.ZipArchiveWriter(file_name)
        writer.write_as_yaml(constants.SCENARIO_FILE_PROPERTIES, self._properties)
        writer.write_as_yaml(constants.SCENARIO_FILE_MAPS, self._maps)
        writer.write_as_yaml(constants.SCENARIO_FILE_PROVINCES, self._provinces)
        writer.write_as_yaml(constants.SCENARIO_FILE_NATIONS, self._nations)

        # rules are never updated by this mechanism
