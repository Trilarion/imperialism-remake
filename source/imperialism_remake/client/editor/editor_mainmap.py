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

from PyQt5 import QtWidgets

from imperialism_remake.base import constants, tools
from imperialism_remake.client.common.main_map import MainMap
from imperialism_remake.lib import qt

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

        # is there a province
        province = self.scenario.server_scenario.province_at(column, row)
        if province:
            a = qt.create_action(tools.load_ui_icon('icon.editor.province_info.png'), 'Province info', self,
                                 partial(self.province_info.emit, province))
            menu.addAction(a)

            # is there also nation
            nation = self.scenario.server_scenario.province_property(province, constants.ProvinceProperty.NATION)
            if nation:
                a = qt.create_action(tools.load_ui_icon('icon.editor.nation_info.png'), 'Nation info', self,
                                     partial(self.nation_info.emit, nation))
                menu.addAction(a)

        menu.exec(event.globalPos())
