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

from PySide import QtCore
import tools as t

# some constants
key_map_size = 'map-size'

class Scenario(QtCore.QObject):

    Complete_Change = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.clear()

    def clear(self):
        self._properties = {}
        self._provinces = {}
        self._nations = {}
        self._map = []

    def create_map(self, size):
        self._properties[key_map_size] = size
        number_tiles = size[0] * size[1]
        self._map = [[0]*number_tiles]*2

    def set_terrain_at(self, position, terrain):
        self._map[0][self.map_index(position)] = terrain

    def terrain_at(self, position):
        return self._map[0][self.map_index(position)]

    def set_resource_at(self, position, resource):
        self._map[1][self.map_index(position)] = resource

    def resource_at(self, position):
        return self._map[1][self.map_index(position)]

    def map_index(self, position):
        print(position)
        index = position[0] * self._properties[key_map_size][0] + position[1]
        return index

    def __setitem__(self, key, value):
        """

        :param key:
        :param value:
        :return:
        """
        self._properties[key] = value

    def __getitem__(self, key):
        """
            One can only obtain properties that have been set before.
        """
        if key in self._properties:
            return self._properties[key]
        else:
            raise RuntimeError('Unknown property {}.'.format(key))

    def new_province(self):
        province = len(self._provinces) # this always works because we check after loading
        self._provinces[province] = {}
        return province

    def set_province_property(self, province, key, value):
        if province in self._provinces:
            self._provinces[province][key] = value
        else:
            raise RuntimeError('Unknown province {}.'.format(province))

    def get_province_property(self, province, key):
        if province in self._provinces and key in self._provinces[province]:
            return self._provinces[province][key]
        else:
            raise RuntimeError('Unknown province {} or property {}.'.format(province, key))

    def new_nation(self):
        nation = len(self._nations) # this always gives a new unique number because we check after loading
        self._nations[nation] = {}
        self._nations[nation]['properties'] = {}
        self._nations[nation]['provinces'] = []
        return nation

    def set_nation_property(self, nation, key, value):
        if nation in self._nations:
            self._nations[nation]['properties'][key] = value
        else:
            raise RuntimeError('Unknown nation {}.'.format(nation))

    def get_nation_property(self, nation, key):
        if nation in self._nations and key in self._nations[nation]['properties']:
            return self._nations[nation]['properties'][key]
        else:
            raise RuntimeError('Unknown nation {} or property {}.'.format(nation, key))

    def transfer_province_to_nation(self, province, nation):
        # TODO this is not right yet
        self._nations[nation]['provinces'].append(province)

    def load(self, file_name):
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
        writer = t.ZipArchiveWriter(file_name)
        writer.write_json('properties', self._properties)
        writer.write_json('map', self._map)
        writer.write_json('provinces', self._provinces)
        writer.write_json('nations', self._nations)
