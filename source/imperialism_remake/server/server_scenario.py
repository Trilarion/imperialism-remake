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
import logging
import math

from PyQt5 import QtCore

from imperialism_remake.base import constants
from imperialism_remake.lib import utils

logger = logging.getLogger(__name__)


# TODO rivers are implemented inefficiently

class ServerScenario(QtCore.QObject):
    """
    Has several dictionaries (properties, provinces, nations) and a list (map) defining everything.

    * _properties is a dictionary with keys from constants.ScenarioProperties
    * _provinces is a dictionary with
    * _nations is a
    * _maps is a dictionary of different maps (terrain, resource)
      each map is a linear list, the map size is a scenario property
    * _rules is a dictionary of rules properties

    Notes:
    * See also constants.ScenarioProperties, constants.NationProperties, constants.ProvinceProperties
    * Each province has nation id stored.
    * Each nation has province ids stored.
    """

    def __init__(self):
        """
        Start with a clean state.
        """
        super().__init__()
        self._properties = {constants.ScenarioProperty.RIVERS: []}
        self._provinces = {}
        self._nations = {}
        self._maps = {}
        self._rules = {}

    @staticmethod
    def from_file(file_path):
        """
        Load/deserialize all internal variables from a zipped archive
        """
        # TODO what if not a valid scenario file, we should raise an error then

        logger.debug('from_file file: %s', file_path)

        scenario = ServerScenario()

        reader = utils.ZipArchiveReader(file_path)

        scenario._properties = reader.read_from_file(constants.SCENARIO_FILE_PROPERTIES)
        scenario._maps = reader.read_from_file(constants.SCENARIO_FILE_MAPS)
        scenario._provinces = reader.read_from_file(constants.SCENARIO_FILE_PROVINCES)
        # TODO check all ids are smaller then len()

        scenario._nations = reader.read_from_file(constants.SCENARIO_FILE_NATIONS)
        # TODO check all ids are smaller then len()

        # read rule file
        # TODO how to specify which rules file apply
        rule_file = constants.extend(constants.SCENARIO_RULESET_FOLDER, scenario[constants.ScenarioProperty.RULES])
        scenario._rules = utils.read_from_file(rule_file)

        return scenario

    def create_empty_map(self, columns, rows):
        """
        Given a size, constructs a map (list of two sub lists with each the number of tiles entries) which is 0.

        :param columns: Number of columns.
        :param rows: Number of rows.
        """

        logger.debug('create_empty_map columns:%s, rows:%s', columns, rows)

        self._properties[constants.ScenarioProperty.MAP_COLUMNS] = columns
        self._properties[constants.ScenarioProperty.MAP_ROWS] = rows
        number_tiles = columns * rows
        self._maps['terrain'] = [0] * number_tiles
        self._maps['resource'] = [0] * number_tiles

    def add_river(self, name, tiles):
        """
            Adds a river with a list of tiles and a name.
            TODO this is inefficient
        """
        logger.debug('add_river name:%s, tiles:%s', name, tiles)

        river = {'name': name, 'tiles': tiles}
        self._properties[constants.ScenarioProperty.RIVERS].extend([river])

    def set_terrain_at(self, column, row, terrain):
        """
        Sets the terrain at a given position. Here, no check is performed for valid terrain.

        :param column: Column position
        :param row: Row position
        :param terrain: Terrain value
        """
        logger.debug('set_terrain_at column:%s, row:%s, terrain:%s', column, row, terrain)

        self._maps['terrain'][self._map_index(column, row)] = terrain

    def terrain_at(self, column, row):
        """
        Returns the terrain at a given position of the map.

        :param column: Column position
        :param row: Row position
        :return: Terrain value
        """
        return self._maps['terrain'][self._map_index(column, row)]

    def terrain_name(self, terrain):
        """
        Get a special property from the rules.
        """
        # TODO move this to a special rules class. Only have rules() and setRules() here.
        return self._rules['terrain_settings'][terrain]['name']

    def set_resource_at(self, column, row, resource):
        """
        Sets the resource value at a given position. No check is performed for valid resources.

        :param column: Column position
        :param row: Row position
        :param resource: Resource value
        """
        logger.debug('set_resource_at column:%s, row:%s, resource:%s', column, row, resource)
        self._maps['resource'][self._map_index(column, row)] = resource

    def resource_at(self, column, row):
        """
        Returns the resource value at a given position of the map.

        :param column: Column position
        :param row: Row position
        :return: Resource value
        """
        return self._maps['resource'][self._map_index(column, row)]

    @staticmethod
    def scene_position(column, row):
        """
            Converts a map position to a scene position.

            A scene position is the the normalized (by the tile size) position of the upper, left corner of a map tile
            at position (column, row) in the map.

            Our convention for this is that each second row is shifted right (positive) by one half, starting with the
            second. Columns and rows start at zero. To not mix this up with other possible ways all the knowledge about
            the shift of the stagger is in this class in methods scene_position() and map_position().
        """
        return column + (row % 2) / 2, row

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
        if row < 0 or row >= self._properties[constants.ScenarioProperty.MAP_ROWS] or column < 0 or column >= \
                self._properties[constants.ScenarioProperty.MAP_COLUMNS]:
            return -1, -1
        return column, row

    def _map_index(self, column, row):
        """
            Internal function. Calculates the index in the linear map for a given 2D position (first row, then column)?
        """
        index = row * self._properties[constants.ScenarioProperty.MAP_COLUMNS] + column
        return index

    def neighbor_position(self, column, row, direction):
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
            if column < self._properties[constants.ScenarioProperty.MAP_COLUMNS] - 1:
                return [column + 1, row]
            else:
                return None
        elif direction is constants.TileDirections.SOUTH_EAST:
            # south-east
            if row < self._properties[constants.ScenarioProperty.MAP_ROWS] - 1:
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
            if row < self._properties[constants.ScenarioProperty.MAP_ROWS] - 1:
                if row % 2 == 0:
                    # even rows (0, 2, 4, ..)
                    return [column - 1, row + 1]
                else:
                    # odd rows (1, 3, 5, ..)
                    return [column, row + 1]
            else:
                return None

    def neighbored_tiles(self, column, row):
        """
            For all directions, get all neighbored tiles. Just executes neighbor_position() for all possible
            TileDirections
        """
        tiles = []
        for direction in constants.TileDirections:
            tiles.append(self.neighbor_position(column, row, direction))
        return tiles

    def __setitem__(self, key, value):
        """
        Given a key and a value, sets a scenario property.

        :param key:
        :param value:
        """
        if key not in constants.ScenarioProperty.__members__.values():
            raise RuntimeError('Not a valid ScenarioProperty: {}.'.format(key))
        self._properties[key] = value

    def __getitem__(self, key):
        """
        Given a key, returns a scenario property. One can only obtain properties that have been set before.

        :param key: The key
        :return: The value
        """
        if key not in self._properties:
            raise RuntimeError('Unknown property {}.'.format(key))
        return self._properties[key]

    def add_province(self):
        """
        Creates a new (nation-less) province and returns the id of it.
        """
        province = len(self._provinces)  # this always works because we check after loading the integrity of the keys

        logger.debug('add_province province:%s', province)

        # TODO unless we delete provinces, some more checks might be good here (like first non-used)
        self._provinces[province] = {
            constants.ProvinceProperty.TILES: [],
            constants.ProvinceProperty.NATION: None
        }
        return province

    def remove_province(self, province):
        """
        Removes a province. Call from editor. This has irreversible and very far reaching consequences.

        :param province: Province
        """
        logger.debug('remove_province province:%s', province)

        if province not in self._provinces:
            raise RuntimeError('Unknown province {}.'.format(province))

        # delete reference to province in nation
        nation = self._provinces[province][constants.ProvinceProperty.NATION]
        self._nations[nation][constants.NationProperty.PROVINCES].remove(province)

        # delete province
        del self._provinces[province]

    def set_province_property(self, province, key, value):
        """
            Sets a province property.
        """
        logger.debug('set_province_property province:%s, key:%s, value:%s', province, key, value)

        if province not in self._provinces:
            raise RuntimeError('Unknown province {}.'.format(province))
        if key not in constants.ProvinceProperty.__members__.values():
            raise RuntimeError('Not a valid ProvinceProperty: {}.'.format(key))
        self._provinces[province][key] = value

    def province_property(self, province, key):
        """
            Gets a province property. One can only obtain properties that have been set before and only for provinces
            that exist.
        """
        logger.debug('set_province_property province:%s, key:%s', province, key)

        if province in self._provinces and key in self._provinces[province]:
            return self._provinces[province][key]
        else:
            raise RuntimeError('Unknown province {} or property {}.'.format(province, key))

    def add_province_map_tile(self, province, position):
        """
        Adds a position to a province.

        :param province:
        :param position:
        :return:
        """
        logger.debug('add_province_map_tile province:%s, position:%s', province, position)

        # TODO TODO we should check that this position is not yet in another province (it should be cleared before).
        #     fail fast, fail often
        if province in self._provinces and self.is_valid_position(position):
            self._provinces[province][constants.ProvinceProperty.TILES].append(position)

    def provinces(self):
        """
        Return a list of ids for all provinces. A province is just an id for us.
        """
        return self._provinces.keys()

    def provinces_of_nation(self, nation):
        """
            Return ids for all provinces in a nation.
        """
        logger.debug('provinces_of_nation nation:%s', nation)

        # TODO not needed, replace
        if nation in self._nations:
            return self._nations[nation][constants.NationProperty.PROVINCES]
        else:
            raise RuntimeError('Unknown nation {}.'.format(nation))

    def province_at(self, column, row):
        """
        Given a position (column, row) returns the province.

        :param column: Map column
        :param row: Map row
        :return: Province
        """
        logger.debug('province_at column:%s, row:%s', column, row)

        #  TODO speed up by having a reference in the map. (see also programmers.SE question)
        position = [column, row]
        for province in self._provinces:
            if position in self._provinces[province][constants.ProvinceProperty.TILES]:
                return province
        return None

    def transfer_province_to_nation(self, province, nation):
        """
        Moves a province to a nation.
        """
        logger.debug('transfer_province_to_nation province:%s, nation:%s', province, nation)

        # TODO this is not right yet
        # wire it in both ways
        self._nations[nation][constants.NationProperty.PROVINCES].append(province)
        self._provinces[province][constants.ProvinceProperty.NATION] = nation

    def nations(self):
        """
        Return a list of ids for all nations. A nation is just an id for us.
        """
        return self._nations.keys()

    def add_nation(self):
        """
        Add a new nation and returns it.
        """
        nation = len(self._nations)  # this always gives a new unique number because we check after loading

        logger.debug('add_nation nation:%s', nation)

        # TODO as long as we do not delete nations, some more checks here might be good
        self._nations[nation] = {
            constants.NationProperty.PROVINCES: [],
        }
        return nation

    def remove_nation(self, nation):
        """
        Removes a nation. Call from editor. This has irreversible and very far reaching consequences.

        :param nation: Nation
        """
        logger.debug('remove_nation nation:%s', nation)

        if nation not in self._nations:
            raise RuntimeError('Unknown nation {}.'.format(nation))

        # delete reference to nation in provinces
        for province in self._nations[nation][constants.NationProperty.PROVINCES]:
            self.set_province_property(province, constants.ProvinceProperty.NATION, None)

        # delete nation
        del self._nations[nation]

    def set_nation_property(self, nation, key, value):
        """
        Set nation property.

        :param nation:
        :param key:
        :param value:
        :return:
        """
        logger.debug('set_nation_property nation:%s, key:%s, value:%s', nation, key, value)

        if nation not in self._nations:
            raise RuntimeError('Unknown nation {}.'.format(nation))
        if key not in constants.NationProperty.__members__.values():
            raise RuntimeError('Not a valid NationProperty: {}.'.format(key))

        self._nations[nation][key] = value

    def nation_property(self, nation_key, property_key):
        """
        Gets a nation property. One can only obtain properties that have been set before and only for nations
        that exist.
        """
        logger.debug('set_nation_property nation_key:%s, property_key:%s', nation_key, property_key)

        try:
            nation = self._nations[nation_key]
        except KeyError:
            raise RuntimeError('Unknown nation "{}" (known nations: {}).'
                               .format(nation_key, ", ".join([str(key) for key in self._nations])))
        try:
            return nation[property_key]
        except KeyError:
            raise RuntimeError('Unknown nation property "{}" (known properties: {}).'
                               .format(property_key, ", ".join([str(key) for key in nation])))

    def save(self, file_name):
        """
            Saves/serializes all internal variables into a zipped archive.
        """
        logger.debug('save file_name:%s', file_name)

        writer = utils.ZipArchiveWriter(file_name)
        writer.write_to_file(constants.SCENARIO_FILE_PROPERTIES, self._properties)
        writer.write_to_file(constants.SCENARIO_FILE_MAPS, self._maps)
        writer.write_to_file(constants.SCENARIO_FILE_PROVINCES, self._provinces)
        writer.write_to_file(constants.SCENARIO_FILE_NATIONS, self._nations)

        # rules are never updated by this mechanism

    def get_terrain_settings(self):
        return self._rules['terrain_settings']
