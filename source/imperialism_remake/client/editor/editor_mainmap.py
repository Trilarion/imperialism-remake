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
from functools import partial

from PyQt5 import QtWidgets, QtGui, QtCore

from imperialism_remake.base import constants, tools
from imperialism_remake.client.common.main_map import MainMap
from imperialism_remake.client.utils.scene_utils import scene_position
from imperialism_remake.lib import qt
from imperialism_remake.server.models.terrain_type import TerrainType

logger = logging.getLogger(__name__)


class EditorMainMap(MainMap):
    def contextMenuEvent(self, event):  # noqa: N802
        """
        Right click (context click) on a tile. Shows the context menu, depending on the tile position
        """

        logger.debug('contextMenuEvent event.pos:%s', event.pos())

        # if there is no scenario existing, don't process the context click
        if not self.scenario.server_scenario:
            return

        # get mouse position in scene coordinates
        scene_position = self.mapToScene(event.pos()) / constants.TILE_SIZE
        column, row = self.scenario.server_scenario.map_position(scene_position.x(), scene_position.y())

        # create context menu
        menu = QtWidgets.QMenu(self)

        # change terrain
        a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain.png'), 'Set terrain', self,
                             partial(self.change_terrain.emit, column, row))
        menu.addAction(a)

        terrain_type = self.scenario.server_scenario.terrain_at(column, row)
        if terrain_type != TerrainType.SEA.value:
            a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'), 'Set resource', self,
                                 partial(self.change_terrain_resource.emit, column, row))
            menu.addAction(a)

            nation = self.scenario.server_scenario.nation_at(column, row)
            if nation:
                province = self.scenario.server_scenario.province_at(column, row)
                a = qt.create_action(tools.load_ui_icon('icon.editor.province_info.png'), 'Province info', self,
                                     partial(self.province_info.emit, province))
                menu.addAction(a)

            a = qt.create_action(tools.load_ui_icon('icon.editor.nation_info.png'), 'Nation info', self,
                                 partial(self.nation_info.emit, nation))
            menu.addAction(a)

        menu.exec(event.globalPos())

    def change_texture_tile(self, row, column) -> None:
        logger.debug(f"change_texture {row}, {column}")

        terrain = self.scenario.server_scenario.terrain_at(column, row)
        province = self.scenario.server_scenario.province_at(column, row)
        if province:
            if terrain == TerrainType.SEA.value:
                    self.scenario.server_scenario.remove_province_map_tile(province, [column, row])

        self._draw_province_and_nation_borders()

    def change_nation_tile(self, row, column) -> None:
        logger.debug(f"change_nation_tile {row}, {column}")

        #TODO

        self._draw_province_and_nation_borders()

    def change_province_tile(self, row, column) -> None:
        logger.debug(f"change_province_tile {row}, {column}")

        #TODO

        self._draw_province_and_nation_borders()
