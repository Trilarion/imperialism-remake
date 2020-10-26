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

from imperialism_remake.client.utils import scene_utils

logger = logging.getLogger(__name__)


class ChangeTextureWidget(QtWidgets.QGraphicsView):
    """

    """
    #: signal, if emitted a new terrain has been chosen
    texture_selected = QtCore.pyqtSignal(int)

    COLUMNS_IN_A_ROW = 4

    def __init__(self, main_map, column, row, settings, mapper, texture_setter):
        super().__init__()

        logger.debug('__init__ column:%s, row:%s', column, row)

        self._column = column
        self._row = row
        self._main_map = main_map
        self._mapper = mapper
        self._texture_setter = texture_setter

        scene = QtWidgets.QGraphicsScene()

        self.setScene(scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self._rows_count = 1 + len(settings) // self.COLUMNS_IN_A_ROW

        for i in range(0, len(settings)):
            y = i // self.COLUMNS_IN_A_ROW
            x = i % self.COLUMNS_IN_A_ROW

            scene_utils.put_pixmap_in_tile_center(scene, self._mapper.get_pixmap_of_type(i), x, y, 1)

    def change_texture_tile(self, x, y):
        logger.debug("fill_texture x:%s, y:%s", x, y)

        tile_x = math.floor(self.COLUMNS_IN_A_ROW * x / self.width())
        tile_y = math.floor(self._rows_count * y / self.height())

        tile_number = tile_x + tile_y * self.COLUMNS_IN_A_ROW

        logger.debug("fill_texture tile_x:%s, tile_y:%s, tile_number:%s", tile_x, tile_y, tile_number)

        self._texture_setter(self._column, self._row, tile_number)
        self._main_map.fill_texture(self._column, self._row, self._mapper, tile_number)

        self._main_map.change_texture_tile(self._row, self._column)
