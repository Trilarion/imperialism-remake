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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRectF

from imperialism_remake.base import constants
from imperialism_remake.client.utils import scene_utils
from imperialism_remake.client.utils.scene_utils import scene_position
from imperialism_remake.lib import qt
from imperialism_remake.server.models.prospector_resource_state import ProspectorResourceState

logger = logging.getLogger(__name__)


class MainMap(QtWidgets.QGraphicsView):
    """
    The big map holding the game map and everything.
    """

    #: signal, emitted if the tile at the mouse pointer (focus) changes
    mouse_move_event = QtCore.pyqtSignal(int, int)

    #: signal, emitted if the change terrain context menu action is called on a terrain
    change_terrain = QtCore.pyqtSignal(int, int)

    #: signal, emitted if the change terrain resource context menu action is called on a terrain
    change_terrain_resource = QtCore.pyqtSignal(int, int)

    #: signal, emitted if a province info is requested
    province_info = QtCore.pyqtSignal(object)

    #: signal, emitted if a nation info is requested
    nation_info = QtCore.pyqtSignal(object)

    mouse_press_event = QtCore.pyqtSignal(object, QtGui.QMouseEvent)

    def __init__(self, scenario, selected_nation):
        super().__init__()

        self._selected_nation = selected_nation

        logger.debug('__init__')

        self.scenario = scenario

        self.setObjectName('map-view')
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setMouseTracking(True)
        self.current_column = -1
        self.current_row = -1

        self._borders = []

    def redraw(self) -> None:
        """
        Whenever a scenario is been created or loaded new we need to draw the whole map.
        """
        logger.debug('redraw started')

        self.scene.clear()

        columns = self.scenario.server_scenario[constants.ScenarioProperty.MAP_COLUMNS]
        rows = self.scenario.server_scenario[constants.ScenarioProperty.MAP_ROWS]

        width = (columns + 0.5) * constants.TILE_SIZE
        height = rows * constants.TILE_SIZE
        self.scene.setSceneRect(0, 0, width, height)

        self._fill_textures(columns, rows, self.scenario.get_terrain_type_to_pixmap_mapper(),
                            self.scenario.server_scenario.terrain_at)

        self._fill_textures(columns, rows, self.scenario.get_terrain_resource_to_pixmap_mapper(),
                            self.scenario.server_scenario.terrain_resource_at)

        self._fill_half_tiles(columns, rows)

        self._draw_rivers()

        self._draw_towns_and_names()

        self._draw_grid_and_coords(columns, rows)

        self.partial_redraw()

        # emit focus changed with -1, -1
        self.mouse_move_event.emit(-1, -1)

        logger.debug('redraw finished')

    def partial_redraw(self):
        logger.debug('partial_redraw started')

        self._draw_roads()

        self._draw_structures()

        self._draw_province_and_nation_borders()

        self._draw_prospector_terrain_resources()

        logger.debug('partial_redraw finished')

    def _fill_textures(self, columns, rows, mapper, obj_type_getter) -> None:
        logger.debug("_fill_textures")
        for column in range(0, columns):
            for row in range(0, rows):
                self.fill_texture(column, row, mapper, obj_type_getter(column, row))

    def fill_texture(self, column, row, mapper, obj_type, z_value=1) -> None:
        pixmap = mapper.get_pixmap_of_type(obj_type)
        if pixmap is None:
            # logger.warning("No pixmap defined for type:%s, col:%s, row:%s", obj_type, column, row)
            return

        sx, sy = scene_position(column, row)
        scene_utils.put_pixmap_in_tile_center(self.scene, pixmap, sx, sy, z_value)

    def _draw_prospector_terrain_resources(self):
        logger.debug("_draw_prospector_terrain_resources")
        if self._selected_nation is None:
            selected_nations = self.scenario.server_scenario.nations()
        else:
            selected_nations = [self._selected_nation]

        for nation in selected_nations:
            for row, value in self.scenario.server_scenario.nation_property(nation,
                                                                            constants.NationProperty.PROSPECTOR_RESOURCE_STATE).items():
                for column, prospector_resource_state in value.items():
                    for resource_type, resource_state in prospector_resource_state.items():
                        if ProspectorResourceState.REVEALED == resource_state:
                            self.fill_texture(column, row, self.scenario.get_terrain_resource_to_pixmap_mapper(),
                                              resource_type)

    def _fill_half_tiles(self, columns, rows) -> None:
        logger.debug("_fill_half_tiles")
        # fill the half tiles which are not part of the map
        brush = QtGui.QBrush(QtCore.Qt.darkGray)
        for row in range(0, rows):
            if row % 2 == 0:
                item = self.scene.addRect(columns * constants.TILE_SIZE, row * constants.TILE_SIZE,
                                          constants.TILE_SIZE / 2,
                                          constants.TILE_SIZE, pen=qt.TRANSPARENT_PEN)
            else:
                item = self.scene.addRect(0, row * constants.TILE_SIZE, constants.TILE_SIZE / 2, constants.TILE_SIZE,
                                          pen=qt.TRANSPARENT_PEN)
            item.setBrush(brush)
            item.setZValue(1)

    def _draw_grid_and_coords(self, columns, rows) -> None:
        logger.debug("_draw_grid_and_coords")
        # draw the grid and the coordinates
        for column in range(0, columns):
            for row in range(0, rows):
                sx, sy = scene_position(column, row)
                # item = self.scene.addRect(sx * constants.TILE_SIZE, sy * constants.TILE_SIZE,  constants.TILE_SIZE,  constants.TILE_SIZE)
                # item.setZValue(1000)
                text = '({},{})'.format(column, row)
                item = QtWidgets.QGraphicsSimpleTextItem(text)
                item.setBrush(QtGui.QBrush(QtCore.Qt.black))
                item.setPos((sx + 0.5) * constants.TILE_SIZE - item.boundingRect().width() / 2,
                            sy * constants.TILE_SIZE)
                item.setZValue(1001)
                self.scene.addItem(item)

    def _draw_towns_and_names(self) -> None:
        logger.debug("_draw_towns_and_names")
        # draw towns and names
        city_pixmap = QtGui.QPixmap(constants.extend(constants.GRAPHICS_MAP_FOLDER, 'city.png'))
        for nation in self.scenario.server_scenario.nations():
            # get all provinces of this nation
            provinces = self.scenario.server_scenario.provinces_of_nation(nation)
            for province in provinces:
                column, row = self.scenario.server_scenario.province_property(province,
                                                                              constants.ProvinceProperty.TOWN_LOCATION)
                sx, sy = scene_position(column, row)
                # center city image on center of tile
                scene_utils.put_pixmap_in_tile_center(self.scene, city_pixmap, sx, sy, 6)
                # display province name below
                province_name = self.scenario.server_scenario.province_property(province,
                                                                                constants.ProvinceProperty.NAME)
                item = self.scene.addSimpleText(province_name)
                item.setPen(qt.TRANSPARENT_PEN)
                item.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
                x = (sx + 0.5) * constants.TILE_SIZE - item.boundingRect().width() / 2
                y = (sy + 1) * constants.TILE_SIZE - item.boundingRect().height()
                item.setPos(x, y)
                item.setZValue(6)
                # display rounded rectangle below province name
                bx = 8
                by = 4
                background = QtCore.QRectF(x - bx, y - by,
                                           item.boundingRect().width() + 2 * bx,
                                           item.boundingRect().height() + 2 * by)
                path = QtGui.QPainterPath()
                path.addRoundedRect(background, 50, 50)
                item = self.scene.addPath(path, pen=qt.TRANSPARENT_PEN,
                                          brush=QtGui.QBrush(QtGui.QColor(128, 128, 255, 64)))
                item.setZValue(5)

    def _draw_province_and_nation_borders(self) -> None:
        logger.debug("_draw_province_and_nation_borders")
        # draw province and nation borders
        # TODO the whole border drawing is a crude approximation, implement it the right way
        for border in self._borders:
            self.scene.removeItem(border)
            del border

        province_border_pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
        province_border_pen.setWidth(2)
        nation_border_pen = QtGui.QPen()
        nation_border_pen.setWidth(4)
        for nation in self.scenario.server_scenario.nations():
            # get nation color
            color = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.COLOR)
            nation_color = QtGui.QColor()
            nation_color.setNamedColor(color)
            # get all provinces
            provinces = self.scenario.server_scenario.provinces_of_nation(nation)
            nation_path = QtGui.QPainterPath()
            # get all tiles
            for province in provinces:
                province_path = QtGui.QPainterPath()
                tiles = self.scenario.server_scenario.province_property(province, constants.ProvinceProperty.TILES)
                for column, row in tiles:
                    sx, sy = scene_position(column, row)
                    province_path.addRect(sx * constants.TILE_SIZE, sy * constants.TILE_SIZE, constants.TILE_SIZE,
                                          constants.TILE_SIZE)
                province_path = province_path.simplified()
                item = self.scene.addPath(province_path, pen=province_border_pen)
                item.setZValue(4)
                nation_path.addPath(province_path)

                self._borders.append(item)
            nation_path = nation_path.simplified()
            nation_border_pen.setColor(nation_color)
            item = self.scene.addPath(nation_path, pen=nation_border_pen)
            item.setZValue(5)

            self._borders.append(item)

    def _draw_rivers(self) -> None:
        logger.debug("_draw_rivers")
        # draw rivers
        river_pen = QtGui.QPen(QtGui.QColor(64, 64, 255))
        river_pen.setWidth(5)
        # TODO get rivers via a method (generator)
        for river in self.scenario.server_scenario[constants.ScenarioProperty.RIVERS]:
            tiles = river['tiles']
            path = QtGui.QPainterPath()
            for tile in tiles:
                sx, sy = scene_position(tile[0], tile[1])
                x = (sx + 0.5) * constants.TILE_SIZE
                y = (sy + 0.5) * constants.TILE_SIZE
                if tile == tiles[0]:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            item = self.scene.addPath(path, pen=river_pen)
            item.setZValue(2)

    def _draw_roads(self) -> None:
        logger.debug("_draw_roads")
        for road_section in self.scenario.server_scenario.get_roads():
            self.draw_road(road_section[0], road_section[1])

    def _draw_structures(self) -> None:
        logger.debug("_draw_structures")
        for row, structure_in_row in self.scenario.server_scenario.get_structures().items():
            for column, structures in structure_in_row.items():
                for structure in structures:
                    self.draw_structure(row, column, structure)

    def draw_structure(self, row, column, structure) -> None:
        pixmap = self.scenario.get_structure_type_to_pixmap_mapper().get_pixmap_of_type(structure.get_type().value)
        if pixmap is None:
            logger.warning("No pixmap defined for type:%s, col:%s, row:%s", structure.get_type(), column, row)
            return

        logger.debug("Draw structure:%s, row:%s, col:%s", structure.get_type(), row, column)
        sx, sy = scene_position(column, row)
        # TODO draw same count of structures as structure level
        scene_utils.put_pixmap_in_tile_center(self.scene, pixmap, sx, sy, 20)

    def draw_road(self, start: (), stop: ()) -> None:
        logger.debug("Draw road from:%s, to:%s", start, stop)

        # TODO use proper icons/pixmaps
        road_pen = QtGui.QPen(QtGui.QColor(164, 64, 155))
        road_pen.setWidth(15)

        path = QtGui.QPainterPath()
        startx, starty = scene_position(start[1], start[0])
        startx = (startx + 0.5) * constants.TILE_SIZE
        starty = (starty + 0.5) * constants.TILE_SIZE
        path.moveTo(startx, starty)

        stopx, stopy = scene_position(stop[1], stop[0])
        stopx = (stopx + 0.5) * constants.TILE_SIZE
        stopy = (stopy + 0.5) * constants.TILE_SIZE
        path.lineTo(stopx, stopy)

        item = self.scene.addPath(path, pen=road_pen)
        item.setZValue(2)

    def visible_rect(self) -> QRectF:
        """
        Returns the visible part of the map view relative to the total scene rectangle as a rectangle with normalized
        values between 0 and 1, relative to the total size of the map.
        """
        logger.debug('visible_rect')

        # total rectangle of the scene (0, 0, width, height)
        s = self.scene.sceneRect()
        # visible rectangle of the view
        v = self.mapToScene(self.rect()).boundingRect()
        return QtCore.QRectF(v.x() / s.width(), v.y() / s.height(), v.width() / s.width(), v.height() / s.height())

    def set_center_position(self, x, y) -> None:
        """
        Changes the visible part of the view by centering the map on normalized positions [0,1) (x,y).
        """
        logger.debug('set_center_position x:%s, y:%s', x, y)

        # total rectangle of the scene (0, 0, width, height)
        s = self.scene.sceneRect()
        # visible rectangle of the view
        v = self.mapToScene(self.rect()).boundingRect()
        # adjust x, y to scene coordinates and find center
        x = x * s.width() + v.width() / 2
        y = y * s.height() + v.height() / 2
        # center on it
        self.centerOn(x, y)

    def mouseMoveEvent(self, event) -> None:  # noqa: N802
        """
        The mouse on the view has been moved. Emit signal mouse_position_changed if we now hover over a different tile.
        """
        if self.scenario.server_scenario is not None:
            # get mouse position in scene coordinates
            scene_position = self.mapToScene(event.pos()) / constants.TILE_SIZE
            column, row = self.scenario.server_scenario.map_position(scene_position.x(), scene_position.y())

            if column != self.current_column or row != self.current_row:
                self.current_column = column
                self.current_row = row
                self.mouse_move_event.emit(column, row)

        super().mouseMoveEvent(event)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        logger.debug("mousePressEvent")

        self.mouse_press_event.emit(self, event)

        super().mousePressEvent(event)
