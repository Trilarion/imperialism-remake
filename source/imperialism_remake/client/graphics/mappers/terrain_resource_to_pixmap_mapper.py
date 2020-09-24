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

from imperialism_remake.base import constants
from imperialism_remake.client.graphics.mappers.terrain_to_pixmap_mapper import TerrainToPixmapMapper

logger = logging.getLogger(__name__)


class TerrainResourceToPixmapMapper(TerrainToPixmapMapper):
    def __init__(self, server_scenario):
        super().__init__(server_scenario.get_terrain_resources_settings(), constants.GRAPHICS_TERRAIN_RESOURCES_FOLDER,
                         'texture_filename')

    def get_pixmap_of_type(self, resource_type: int):
        if resource_type < 1 or resource_type > len(self.pixmaps):
            #logger.warning('Tile type undefined: %s', resource_type)
            return None

        return self._get_pixmap_of_type(resource_type)
