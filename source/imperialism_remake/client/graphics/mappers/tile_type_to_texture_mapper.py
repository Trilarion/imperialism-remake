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

from PyQt5 import QtGui

from imperialism_remake.base import constants

logger = logging.getLogger(__name__)


class TileTypeToTextureMapper:
    def __init__(self, server_scenario):
        super().__init__()

        terrain_settings = server_scenario.get_terrain_settings()

        self.pixmaps = {}
        for terrain_type in terrain_settings:
            pixmap = QtGui.QPixmap(
                constants.extend(constants.GRAPHICS_TERRAINS_FOLDER,
                                 terrain_settings[terrain_type]['texture_filename']))
            self.pixmaps[terrain_type] = pixmap.scaled(constants.TILE_SIZE, constants.TILE_SIZE)

    def get_pixmap_of_type(self, tile_type: int):
        if tile_type >= len(self.pixmaps):
            raise RuntimeError('Tile type undefined: %s', tile_type)

        return self.pixmaps[tile_type]
