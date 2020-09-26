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
import logging

from imperialism_remake.client.editor.change_texture_widget import ChangeTextureWidget
from imperialism_remake.server.models.terrain_resource_type import TerrainResourceType
from imperialism_remake.server.models.terrain_type import TerrainType

logger = logging.getLogger(__name__)


class ChangeTerrainResourceWidget(ChangeTextureWidget):
    def __init__(self, screen, column, row):
        super().__init__(screen.main_map, column, row, screen.scenario.server_scenario.get_terrain_resources_settings(),
                         screen.scenario.get_terrain_resource_to_pixmap_mapper(),
                         self._custom_set_terrain_resource_at)
        self._screen = screen

    def mousePressEvent(self, event):
        logger.debug("mousePressEvent x:%s, y:%s", event.x(), event.y())

        self._fill_texture(event.x(), event.y())

    def _custom_set_terrain_resource_at(self, column, row, resource):
        self._screen.scenario.server_scenario.set_terrain_resource_at(column, row, resource)

        if resource == TerrainResourceType.ORE.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.HILLS.value)
        elif resource == TerrainResourceType.COAL.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.HILLS.value)
        elif resource == TerrainResourceType.COTTON.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.PLAIN.value)
        elif resource == TerrainResourceType.FOREST.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.PLAIN.value)
        elif resource == TerrainResourceType.ORCHARD.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.PLAIN.value)
        elif resource == TerrainResourceType.GRAIN.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.PLAIN.value)
        elif resource == TerrainResourceType.SCRUBFOREST.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.PLAIN.value)
        elif resource == TerrainResourceType.SHEEP.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.HILLS.value)
        elif resource == TerrainResourceType.OIL.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.SWAMP.value)
        elif resource == TerrainResourceType.HORSE.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.PLAIN.value)
        elif resource == TerrainResourceType.BUFFALO.value:
            self._screen.scenario.server_scenario.set_terrain_at(column, row, TerrainType.PLAIN.value)
        else:
            raise Exception('Unknown resource:%s', resource)





