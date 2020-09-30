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

from imperialism_remake.base import constants
from imperialism_remake.server.models.technology_type import TechnologyType


class ServerScenarioBase:
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

    RESOURCE = 'resource'
    TERRAIN = 'terrain'
    ROAD = 'road'
    STRUCTURE = 'structure'

    def __init__(self):
        """
        Start with a clean state.
        """
        self._properties = {constants.ScenarioProperty.RIVERS: []}
        self._provinces = {}
        self._nations = {}
        self._maps = {}
        self._rules = {}

        self._available_technologies = set()

        # TODO read technologies from scenario/properties/rules...
        self._available_technologies.add(TechnologyType.ROAD_THROUGH_HILLS)
        self._available_technologies.add(TechnologyType.ROAD_THROUGH_PLAINS)
        self._available_technologies.add(TechnologyType.PROSPECTOR_WORK_HILLS)
        self._available_technologies.add(TechnologyType.PROSPECTOR_WORK_MOUNTAIN)
        self._available_technologies.add(TechnologyType.FARMER_ORCHARD_LEVEL1)
        self._available_technologies.add(TechnologyType.FARMER_GRAIN_LEVEL1)
        self._available_technologies.add(TechnologyType.FORESTER_FOREST_LEVEL1)

    @property
    def available_technologies(self):
        return self._available_technologies

    @property
    def maps(self):
        return self._maps

    @maps.setter
    def maps(self, maps):
        self._maps = maps

    @property
    def properties(self):
        return self._properties

    @properties.setter
    def properties(self, properties):
        self._properties = properties

    @property
    def provinces(self):
        return self._provinces

    @provinces.setter
    def provinces(self, provinces):
        self._provinces = provinces

    @property
    def nations(self):
        return self._nations

    @nations.setter
    def nations(self, nations):
        self._nations = nations

    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules):
        self._rules = rules
