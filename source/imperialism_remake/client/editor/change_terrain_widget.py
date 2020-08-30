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
import math

from PyQt5 import QtWidgets, QtCore

from imperialism_remake.client.common.tile_type_to_texture_mapper import TileTypeToTextureMapper
from imperialism_remake.client.utils import scene_utils

logger = logging.getLogger(__name__)


class ChangeTerrainWidget(QtWidgets.QGraphicsView):
    """

    """
    #: signal, if emitted a new terrain has been chosen
    terrain_selected = QtCore.pyqtSignal(int)

    COLUMNS_IN_A_ROW = 4

    def __init__(self, screen, column, row):
        super().__init__()

        logger.debug('__init__ column:%s, row:%s', column, row)

        self.column = column
        self.row = row

        self.screen = screen
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        for i in range(0, len(screen.scenario.server_scenario.get_terrain_settings())):
            y = i // self.COLUMNS_IN_A_ROW
            x = i % self.COLUMNS_IN_A_ROW

            scene_utils.put_pixmap_in_tile_center(self.scene,
                                                  TileTypeToTextureMapper(self.screen.scenario).get_pixmap_of_type(i),
                                                  x, y, 1)

    def mousePressEvent(self, event):
        logger.debug("mousePressEvent x:%s, y:%s", event.x(), event.y())

        tile_x = math.floor(self.COLUMNS_IN_A_ROW * event.x() / self.scene.width())
        tile_y = math.floor(self.COLUMNS_IN_A_ROW * event.y() / self.scene.height() / 2)

        tile_number = tile_x + tile_y * self.COLUMNS_IN_A_ROW

        logger.debug("mousePressEvent tile_x:%s, tile_y:%s, tile_number:%s", tile_x, tile_y, tile_number)

        self.screen.scenario.server_scenario.set_terrain_at(self.column, self.row, tile_number)
        self.screen.main_map.fill_tile_texture(self.column, self.row)
