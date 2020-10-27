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
import random
from functools import partial

from PyQt5 import QtWidgets, QtCore

from imperialism_remake.base import constants, tools
from imperialism_remake.client.common.main_map import MainMap
from imperialism_remake.lib import qt
from imperialism_remake.server.models.terrain_type import TerrainType

logger = logging.getLogger(__name__)


class EditorMainMap(MainMap):
    #: signal, emitted if the change terrain context menu action is called on a terrain
    change_terrain = QtCore.pyqtSignal(int, int)

    #: signal, emitted if the change terrain resource context menu action is called on a terrain
    change_terrain_resource = QtCore.pyqtSignal(int, int)

    #: signal, emitted if a province info is requested
    province_info = QtCore.pyqtSignal(object)

    #: signal, emitted if a nation info is requested
    nation_info = QtCore.pyqtSignal(object)

    set_nation_event = QtCore.pyqtSignal(int, int, object, object)

    add_workforce_event = QtCore.pyqtSignal(int, int)

    remove_workforce_event = QtCore.pyqtSignal(object)

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
            self._add_menu_item_set_resource(column, menu, row)

            province = self._add_menu_item_province_info(column, menu, row)

            nation = self._add_menu_item_nation_info(column, menu, row)

            self._add_menu_item_set_nation(column, menu, nation, province, row)

            self._add_menu_item_river(column, menu, row)

            self._add_menu_item_roads(column, menu, row)

            self._add_menu_item_workforce(column, menu, row)

        menu.exec(event.globalPos())

    def _add_menu_item_workforce(self, column, menu, row):
        on_workforce = None

        selected_nation = self.scenario.server_scenario.nation_at(row, column)
        workforces = self.scenario.server_scenario.get_nation_asset(selected_nation).get_workforces()

        for id, w in workforces.items():
            if w.get_current_position() == (row, column):
                on_workforce = w
                break

        if on_workforce:
            a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'),
                                 'Delete ' + str(on_workforce.get_type()),
                                 self,
                                 partial(self.remove_workforce_event.emit, on_workforce))
            menu.addAction(a)
        else:
            a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'),
                                 'Add worker',
                                 self,
                                 partial(self.add_workforce_event.emit, row, column))
            menu.addAction(a)

    def _add_menu_item_roads(self, column, menu, row):
        roads = self.scenario.server_scenario.get_roads()

        not_on_road = True
        for road in roads:
            if [row, column] in road:
                not_on_road = False

        road_tiles = []
        for road in roads:
            if len(road) > 0:
                neighbors = self.scenario.server_scenario.neighbored_tiles(column, row)
                for neighbor in neighbors:
                    if [neighbor[1], neighbor[0]] in road:
                        road_tiles.append([neighbor[0], neighbor[1]])

        if not_on_road:
            province_id = self.scenario.server_scenario.province_at(column, row)
            city_position = self.scenario.server_scenario.province_property(province_id,
                                                                            constants.ProvinceProperty.TOWN_LOCATION)
            if city_position in self.scenario.server_scenario.neighbored_tiles(column, row):
                a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'),
                                     'Start road from city',
                                     self,
                                     partial(self._start_road_event, column, row, city_position))
                menu.addAction(a)

            if len(road_tiles) > 0:
                a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'), 'Add road',
                                     self,
                                     partial(self._add_road_event, column, row, road_tiles))
                menu.addAction(a)

        else:
            if len(road_tiles) > 0:
                a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'), 'Remove road',
                                     self,
                                     partial(self._remove_road_event, column, row, road_tiles))
                menu.addAction(a)

            # TODO allow road merge

    def _add_road_event(self, column, row, road_tiles):
        rand_road_index = random.randint(0, len(road_tiles) - 1)
        self.scenario.server_scenario.add_road([row, column],
                                               [road_tiles[rand_road_index][1], road_tiles[rand_road_index][0]])

        self._draw_roads()

    def _remove_road_event(self, column, row, road_tiles):
        roads = self.scenario.server_scenario.get_roads()
        for road in roads:
            for road_tile in road_tiles:
                if ([row, column], [road_tile[1], road_tile[0]]) == road:
                    roads.remove(([row, column], [road_tile[1], road_tile[0]]))
                    self._draw_roads()
                    return
                elif ([road_tile[1], road_tile[0]], [row, column]) == road:
                    roads.remove(([road_tile[1], road_tile[0]], [row, column]))
                    self._draw_roads()
                    return

    def _start_road_event(self, column, row, city_position):
        self.scenario.server_scenario.add_road([row, column], [city_position[1], city_position[0]])

        self._draw_roads()

    def _add_menu_item_river(self, column, menu, row):
        rivers = self.scenario.server_scenario.get_rivers()

        for river in rivers:
            if len(river['tiles']) > 0:
                if river['tiles'][0][0] == column and river['tiles'][0][1] == row:
                    a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'), 'Remove river',
                                         self,
                                         partial(self._remove_river_event, column, row, river['tiles']))
                    menu.addAction(a)
                    return

        not_on_river = True
        for river in rivers:
            if [column, row] in river['tiles']:
                not_on_river = False

        if not_on_river:
            for river in rivers:
                if len(river['tiles']) > 0:
                    neighbors = self.scenario.server_scenario.neighbored_tiles(column, row)
                    if river['tiles'][0] in neighbors:
                        a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'), 'Add river',
                                             self,
                                             partial(self._add_river_event, column, row, river['tiles']))
                        menu.addAction(a)
                        return

            neighbors = self.scenario.server_scenario.neighbored_tiles(column, row)
            sea_tiles = []
            for neighbor in neighbors:
                terrain_type = self.scenario.server_scenario.terrain_at(neighbor[0], neighbor[1])
                if terrain_type == TerrainType.SEA.value:
                    sea_tiles.append([neighbor[0], neighbor[1]])

            if len(sea_tiles) > 0:
                a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'),
                                     'Start river from Sea (random tail)',
                                     self,
                                     partial(self._start_river_event, column, row, sea_tiles))
                menu.addAction(a)
                return

    def _start_river_event(self, column, row, sea_tiles):
        self.scenario.server_scenario.add_river('Unknown',
                                                [[column, row], sea_tiles[random.randint(0, len(sea_tiles) - 1)]])

        self._draw_rivers()

    def _add_river_event(self, column, row, river_tiles):
        river_tiles.insert(0, [column, row])

        self._draw_rivers()

    def _remove_river_event(self, column, row, river_tiles):
        if len(river_tiles) > 2:
            river_tiles.remove([column, row])
        else:
            river_tiles.clear()

        self._draw_rivers()

    def _add_menu_item_set_nation(self, column, menu, nation, province, row):
        a = qt.create_action(tools.load_ui_icon('icon.editor.nation_info.png'), 'Set nation', self,
                             partial(self.set_nation_event.emit, row, column, nation, province))
        menu.addAction(a)

    def _add_menu_item_nation_info(self, column, menu, row):
        nation = self.scenario.server_scenario.nation_at(row, column)
        if nation:
            a = qt.create_action(tools.load_ui_icon('icon.editor.nation_info.png'), 'Nation info', self,
                                 partial(self.nation_info.emit, nation))
            menu.addAction(a)
        return nation

    def _add_menu_item_province_info(self, column, menu, row):
        province = self.scenario.server_scenario.province_at(column, row)
        if province:
            a = qt.create_action(tools.load_ui_icon('icon.editor.province_info.png'), 'Province info', self,
                                 partial(self.province_info.emit, province))
            menu.addAction(a)
        return province

    def _add_menu_item_set_resource(self, column, menu, row):
        a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain_resource.png'), 'Set resource', self,
                             partial(self.change_terrain_resource.emit, column, row))
        menu.addAction(a)

    def change_texture_tile(self, row, column) -> None:
        logger.debug(f"change_texture {row}, {column}")

        terrain = self.scenario.server_scenario.terrain_at(column, row)
        province = self.scenario.server_scenario.province_at(column, row)
        if province:
            if terrain == TerrainType.SEA.value:
                self.scenario.server_scenario.remove_province_map_tile(province, [column, row])

        self._draw_province_and_nation_borders()

    def change_nation_tile(self, row, column, province) -> None:
        logger.debug(f"change_nation_tile {row}, {column}, province:{province}")

        self.scenario.server_scenario.change_province_map_tile(province, [column, row])

        self._draw_province_and_nation_borders()

