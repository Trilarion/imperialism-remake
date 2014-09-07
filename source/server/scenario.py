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

"""
    Defines a scenario, can be loaded and saved. Should only be known to the server, never to the client (which is a
    thin client).
"""

from PySide import QtCore

import tools as t

# some constants
key_map_size = 'map-size'


class Scenario(QtCore.QObject):
    """
        Has several dictionaries (properties, provinces, nations) and a list (map) defining everything.
    """
    Complete_Change = QtCore.Signal()

    def __init__(self):
        """
            Start with a clean state.
        """
        super().__init__()
        self.clear()

    def clear(self):
        """
            We just set all internal variables to empty dictionaries and lists. This is a rather undefined state then
            and needs to be populated by meaningful data later on.
        """
        self._properties = {}
        self._provinces = {}
        self._nations = {}
        self._map = []

    def create_map(self, size):
        """
            Given a size, constructs a map (list of two sub lists with each the number of tiles entries) which is 0.
        """
        self._properties[key_map_size] = size
        number_tiles = size[0] * size[1]
        self._map = [[0] * number_tiles] * 2

    def set_terrain_at(self, position, terrain):
        """
            Sets the terrain at a given position.
        """
        self._map[0][self.map_index(position)] = terrain

    def terrain_at(self, position):
        """
            Returns the terrain at a given position.
        """
        return self._map[0][self.map_index(position)]

    def set_resource_at(self, position, resource):
        """
            Sets the resource value at a given position.
        """
        self._map[1][self.map_index(position)] = resource

    def resource_at(self, position):
        """
            Returns the resource value at a given position from the map.
        """
        return self._map[1][self.map_index(position)]

    def map_index(self, position):
        """
            Calculates the index in the linear map for a given 2D position (first row, then column)?
        """
        print(position)
        index = position[0] * self._properties[key_map_size][0] + position[1]
        return index

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

    def transfer_province_to_nation(self, province, nation):
        """
            Moves a province to a nation.
        """
        # TODO this is not right yet
        self._nations[nation]['provinces'].append(province)

    def load(self, file_name):
        """
            Loads/deserializes all internal variables from a zipped archive via JSON.
        """
        self.clear()
        reader = t.ZipArchiveReader(file_name)
        self._properties = reader.read_as_json('properties')
        self._map = reader.read_as_json('map')
        self._provinces = reader.read_as_json('provinces')
        # TODO check all ids are smaller then len()
        self._nations = reader.read_as_json('nations')
        # TODO check all ids are smaller then len()
        self.Complete_Change.emit()

    def save(self, file_name):
        """
            Saves/serializes all internal variables via JSON into a zipped archive.
        """
        writer = t.ZipArchiveWriter(file_name)
        writer.write_json('properties', self._properties)
        writer.write_json('map', self._map)
        writer.write_json('provinces', self._provinces)
        writer.write_json('nations', self._nations)
