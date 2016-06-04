# Imperialism remake
# Copyright (C) 2014 Trilarion
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

import math

from PyQt5 import QtCore

import lib.utils as u
from base import constants as c

"""
    Defines a scenario, can be loaded and saved. Should only be known to the server, never to the client (which is a
    thin client).
"""

# TODO rivers are implemented inefficiently

class Scenario(QtCore.QObject):
    """
        Has several dictionaries (properties, provinces, nations) and a list (map) defining everything.
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
        self._properties = {c.PropertyKeyNames.RIVERS: []}
        self._provinces = {}
        self._nations = {}
        self._map = {}

    def create_map(self, columns, rows):
        """
            Given a size, constructs a map (list of two sub lists with each the number of tiles entries) which is 0.
        """
        self._properties[c.PropertyKeyNames.MAP_COLUMNS] = columns
        self._properties[c.PropertyKeyNames.MAP_ROWS] = rows
        number_tiles = columns * rows
        self._map['terrain'] = [0] * number_tiles
        self._map['resource'] = [0] * number_tiles

    def add_river(self, name, tiles):
        """
            Adds a river with a list of tiles and a name.
        """
        river = {
            'name': name,
            'tiles': tiles
        }
        self._properties[c.PropertyKeyNames.RIVERS].extend([river])

    def set_terrain_at(self, column, row, terrain):
        """
            Sets the terrain at a given position.
        """
        self._map['terrain'][self.map_index(column, row)] = terrain

    def terrain_at(self, column, row):
        """
            Returns the terrain at a given position.
        """
        return self._map['terrain'][self.map_index(column, row)]

    def set_resource_at(self, column, row, resource):
        """
            Sets the resource value at a given position.
        """
        self._map['resource'][self.map_index(column, row)] = resource

    def resource_at(self, column, row):
        """
            Returns the resource value at a given position from the map.
        """
        return self._map['resource'][self.map_index(column, row)]

    def map_position(self, x, y):
        """
            Converts a scene position to a map position (or return (-1,-1) if
        """
        column = math.floor(x - (y % 2) / 2)
        row = math.floor(y)
        if row < 0 or row >= self._properties[c.PropertyKeyNames.MAP_ROWS] or column < 0\
                or column >= self._properties[c.PropertyKeyNames.MAP_COLUMNS]:
            return -1, -1
        return column, row

    @staticmethod
    def scene_position(column, row):
        """
            Converts a map position to a scene position
        """
        # TODO move to client side, has nothing to do with server (or has it?)
        return column + (row % 2) / 2, row

    def map_index(self, column, row):
        """
            Calculates the index in the linear map for a given 2D position (first row, then column)?
        """
        index = row * self._properties[c.PropertyKeyNames.MAP_COLUMNS] + column
        return index

    def get_neighbor_position(self, column, row, direction):
        """
            Given a positon (column, row) and a direction (c.TileDirections) return the position of the next neighbor
            tile in that direction given our staggered tile layout where the second and all other odd rows are shifted
            half a tile to the right. Returns None if we would be outside of the map area.
        """
        if direction is c.TileDirections.West:
            # west
            if column > 0:
                return [column - 1, row]
            else:
                return None
        elif direction is c.TileDirections.NorthWest:
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
        elif direction is c.TileDirections.NorthEast:
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
        elif direction is c.TileDirections.East:
            # east
            if column < self._properties[c.PropertyKeyNames.MAP_COLUMNS] - 1:
                return [column + 1, row]
            else:
                return None
        elif direction is c.TileDirections.SouthEast:
            # south-east
            if row < self._properties[c.PropertyKeyNames.MAP_ROWS] - 1:
                if row % 2 == 0:
                    # even rows (0, 2, 4, ..)
                    return [column, row + 1]
                else:
                    # odd rows (1, 3, 5, ..)
                    return [column + 1, row + 1]
            else:
                return None
        elif direction is c.TileDirections.SouthWest:
            # south-west
            if row < self._properties[c.PropertyKeyNames.MAP_ROWS] - 1:
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
            For all directions, get all neighbored tiles.
        """
        tiles = []
        for direction in c.TileDirections:
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

    def new_province(self):
        """
            Creates a new (nation-less) province and returns it.
        """
        province = len(self._provinces)  # this always works because we check after loading
        self._provinces[province] = {}
        self._provinces[province]['tiles'] = []
        self._provinces[province]['nation'] = None
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
            Gets a province property.
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
            self._provinces[province]['tiles'].append(position)

    def all_nations(self):
        """
            Return a list of ids for all nations.
        """
        return self._nations.keys()

    def new_nation(self):
        """
            Add a new nation and returns it.
        """
        nation = len(self._nations)  # this always gives a new unique number because we check after loading
        self._nations[nation] = {}
        self._nations[nation]['properties'] = {}
        self._nations[nation]['provinces'] = []
        return nation

    def set_nation_property(self, nation, key, value):
        """
            Set nation property.
        """
        if nation in self._nations:
            self._nations[nation]['properties'][key] = value
        else:
            raise RuntimeError('Unknown nation {}.'.format(nation))

    def get_nation_property(self, nation, key):
        """
            Gets a nation property.
        """
        if nation in self._nations and key in self._nations[nation]['properties']:
            return self._nations[nation]['properties'][key]
        else:
            raise RuntimeError('Unknown nation {} or property {}.'.format(nation, key))

    def get_provinces_of_nation(self, nation):
        """
            Return ids for all provinces in a nation.
        """
        if nation in self._nations:
            return self._nations[nation]['provinces']
        else:
            raise RuntimeError('Unknown nation {}.'.format(nation))

    def get_province_at(self, column, row):
        """
            Given a position (column, row) returns the province.

            TODO speed up by having a reference in the map. (see also programmers.SE question)
        """
        position = [column, row]  # internally because of JSON saving we only have []
        for province in self._provinces:
            if position in self._provinces[province]['tiles']:
                return province
        return None

    def transfer_province_to_nation(self, province, nation):
        """
            Moves a province to a nation.
        """
        # TODO this is not right yet
        # wire it in both ways
        self._nations[nation]['provinces'].append(province)
        self._provinces[province]['nation'] = nation

    def get_terrain_name(self, terrain):
        """
            Get a special property from the rules.

            TODO move this to a special rules class. Only have rules() and setRules() here.
        """
        return self._properties['rules']['terrain.names'][terrain]

    def load(self, file_name):
        """
            Loads/deserializes all internal variables from a zipped archive via JSON.
        """
        self.reset()
        reader = u.ZipArchiveReader(file_name)
        self._properties = reader.read_as_yaml('properties')
        self._map = reader.read_as_yaml('map')
        self._provinces = reader.read_as_yaml('provinces')
        # TODO check all ids are smaller then len()
        self._nations = reader.read_as_yaml('nations')
        # TODO check all ids are smaller then len()
        self.load_rules()

    def load_rules(self):
        """

        """
        # read rules
        rule_file = c.extend(c.Scenario_Ruleset_Folder, self._properties['rules'])
        self._properties['rules'] = u.read_as_yaml(rule_file)

    def save(self, file_name):
        """
            Saves/serializes all internal variables via JSON into a zipped archive.
        """
        writer = u.ZipArchiveWriter(file_name)
        writer.write_as_yaml('properties', self._properties)
        writer.write_as_yaml('map', self._map)
        writer.write_as_yaml('provinces', self._provinces)
        writer.write_as_yaml('nations', self._nations)
