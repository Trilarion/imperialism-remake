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
GUI and internal working of the scenario editor. This is also partly of the client but since the client should not
know anything about the scenario, we put it in the server module.
"""

import math
import os
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

from imperialism_remake.client import graphics
from imperialism_remake.base import constants, tools
from imperialism_remake.lib import qt, utils
from imperialism_remake.server.scenario import Scenario


class MiniMap(QtWidgets.QWidget):
    """
    Small overview map
    """

    # TODO fixed width -> make it selectable from outside

    # Fixed width of 300 pixels
    VIEW_WIDTH = 300

    #: signal, emitted if the user clicks somewhere in the mini map and the ROI rectangle changes as a result, sends
    #    the normalized x and y position of the center of the new ROI
    roi_changed = QtCore.pyqtSignal(float, float)

    def __init__(self, *args, **kwargs):
        """
        Sets up the graphics view, the toolbar and the tracker rectangle.
        """
        super().__init__(*args, **kwargs)
        self.setObjectName('mini-map-widget')

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # the content is a scene
        self.scene = QtWidgets.QGraphicsScene()

        # tracker rectangle that tracks the view of the map, initially hidden
        self.tracker = QtWidgets.QGraphicsRectItem()
        self.tracker.setCursor(QtCore.Qt.PointingHandCursor)
        self.tracker.setZValue(1000)
        self.tracker.hide()
        self.scene.addItem(self.tracker)

        # the view on the scene (no scroll bars)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.view)

        # the width and height (fixed width throughout the game)
        # TODO make this adjustable
        self.view.setFixedWidth(self.VIEW_WIDTH)
        view_height = math.floor(0.6 * self.VIEW_WIDTH)
        self.view.setFixedHeight(view_height)

        # tool bar below the mini map
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(20, 20))

        # action group (only one of them can be checked at each time)
        action_group = QtWidgets.QActionGroup(self.toolbar)
        # political view in the beginning
        a = qt.create_action(tools.load_ui_icon('icon.mini.political.png'), 'Show political view', action_group,
                             toggle_connection=self.switch_to_political_view, checkable=True)
        self.toolbar.addAction(a)
        # geographical view
        a = qt.create_action(tools.load_ui_icon('icon.mini.geographical.png'), 'Show geographical view', action_group,
                             toggle_connection=self.switch_to_geographical_view, checkable=True)
        self.toolbar.addAction(a)
        self.mode = constants.OverviewMapMode.POLITICAL

        # wrap tool bar into horizontal layout with stretch
        l = QtWidgets.QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(self.toolbar)
        l.addStretch()

        # add layout containing tool bar
        layout.addLayout(l)

        # graphics items in scene (except the tracker)
        self.scene_items = []

    def redraw(self):
        """
        The scenario has changed or the mode has changed. Redraw the overview map.
        """

        # get number of columns and rows from the scenario
        columns = editor_scenario.scenario[constants.ScenarioProperty.MAP_COLUMNS]
        rows = editor_scenario.scenario[constants.ScenarioProperty.MAP_ROWS]

        # compute tile size (we assume square tiles)
        tile_size = self.view.width() / columns

        # adjust view height for aspect ratio of the scenario map, assuming square tiles
        view_height = math.floor(tile_size * rows)
        self.view.setFixedHeight(view_height)

        # remove everything except the tracker from the scene
        for item in self.scene_items:
            self.scene.removeItem(item)
        self.scene_items = []

        # set scene rect
        self.scene.setSceneRect(0, 0, columns * tile_size, rows * tile_size)
        self.view.fitInView(self.scene.sceneRect())
        # by design there should be almost no scaling or anything else

        if self.mode == constants.OverviewMapMode.POLITICAL:
            # political mode

            # fill the ground layer with a neutral color
            item = self.scene.addRect(0, 0, columns * tile_size, rows * tile_size)
            item.setBrush(QtCore.Qt.lightGray)
            item.setPen(qt.TRANSPARENT_PEN)
            item.setZValue(0)
            self.scene_items.extend([item])

            # draw the nation borders and content (non-smooth)

            # for all nations
            for nation in editor_scenario.scenario.nations():
                # get nation color
                color_string = editor_scenario.scenario.nation_property(nation, constants.NationProperty.COLOR)
                color = QtGui.QColor()
                color.setNamedColor(color_string)
                # get all provinces
                provinces = editor_scenario.scenario.provinces_of_nation(nation)
                tiles = []
                # get all tiles
                for province in provinces:
                    tiles.extend(editor_scenario.scenario.province_property(province,
                                                                            constants.ProvinceProperty.TILES))
                # get rectangular path for each tile
                path = QtGui.QPainterPath()
                for tile in tiles:
                    sx, sy = editor_scenario.scenario.scene_position(*tile)
                    path.addRect(sx * tile_size, sy * tile_size, tile_size, tile_size)
                # simply (creates outline)
                path = path.simplified()
                # create a brush from the color
                brush = QtGui.QBrush(color)
                item = self.scene.addPath(path, brush=brush)  # will use the default pen for outline
                item.setZValue(1)
                self.scene_items.extend([item])

        elif self.mode == constants.OverviewMapMode.GEOGRAPHICAL:

            # fill the background with sea (blue)
            item = self.scene.addRect(0, 0, columns * tile_size, rows * tile_size)
            item.setBrush(QtCore.Qt.blue)
            item.setPen(qt.TRANSPARENT_PEN)
            item.setZValue(0)
            self.scene_items.extend([item])

            # six terrains left, plains, hills, mountains, tundra, swamp, desert

            # go through each position
            paths = {}
            for t in range(1, 7):
                paths[t] = QtGui.QPainterPath()
            for column in range(0, columns):
                for row in range(0, rows):
                    t = editor_scenario.scenario.terrain_at(column, row)
                    if t != 0:
                        # not for sea
                        sx, sy = editor_scenario.scenario.scene_position(column, row)
                        paths[t].addRect(sx * tile_size, sy * tile_size, tile_size, tile_size)
            colors = {1: QtCore.Qt.green, 2: QtCore.Qt.darkGreen, 3: QtCore.Qt.darkGray, 4: QtCore.Qt.white,
                      5: QtCore.Qt.darkYellow, 6: QtCore.Qt.yellow}
            for t in paths:
                path = paths[t]
                path = path.simplified()
                brush = QtGui.QBrush(colors[t])
                item = self.scene.addPath(path, brush=brush, pen=qt.TRANSPARENT_PEN)
                item.setZValue(1)
                self.scene_items.extend([item])

    def switch_to_political_view(self, checked):
        """
            The toolbar button for the political view has been toggled.
        """
        if checked:
            # mode should not be political
            self.mode = constants.OverviewMapMode.POLITICAL
            self.redraw()

    def switch_to_geographical_view(self, checked):
        """
            The toolbar button for the geographical view has been toggled.
        """
        if checked:
            # mode should not be geographical
            self.mode = constants.OverviewMapMode.GEOGRAPHICAL
            self.redraw()

    def mousePressEvent(self, event):  # noqa: N802
        """
        The mouse has been pressed inside the view. Center the tracker rectangle.
        """
        super().mouseMoveEvent(event)

        # if the tracker is not yet visible, don't do anything
        if not self.tracker.isVisible():
            return

        # get coordinates as scene coordinates and subtract half the tracker width and height
        tracker_rect = self.tracker.rect()
        x = event.x() - tracker_rect.width() / 2
        y = event.y() - tracker_rect.height() / 2

        # apply min/max to keep inside the map area
        x = min(max(x, 0), self.scene.width() - tracker_rect.width())
        y = min(max(y, 0), self.scene.width() - tracker_rect.height())

        # check if position of tracker should change
        if x != tracker_rect.x() or y != tracker_rect.y():
            # it should, move tracker and emit signal
            tracker_rect.moveTo(x, y)
            self.tracker.setRect(tracker_rect)
            # normalize position before
            x = x / self.scene.width()
            y = y / self.scene.height()
            self.roi_changed.emit(x, y)

    def activate_tracker(self, bounds: QtCore.QRectF):
        """
        The main map tells us how large its view is (in terms of the game map) and where it is currently.

        :param bounds:
        """
        # scale to scene width and height
        w = self.scene.width()
        h = self.scene.height()
        bounds = QtCore.QRectF(bounds.x() * w, bounds.y() * h, bounds.width() * w, bounds.height() * h)

        # set bounds of tracker and show
        self.tracker.setRect(bounds)
        self.tracker.show()


class MainMap(QtWidgets.QGraphicsView):
    """
    The big map holding the game map and everything.
    """

    #: signal, emitted if the tile at the mouse pointer (focus) changes
    focus_changed = QtCore.pyqtSignal(int, int)

    #: signal, emitted if the change terrain context menu action is called on a terrain
    change_terrain = QtCore.pyqtSignal(int, int)

    #: signal, emitted if a province info is requested
    province_info = QtCore.pyqtSignal(int)

    #: signal, emitted if a nation info is requested
    nation_info = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()

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

        # TODO hardcore tile size somewhere else (and a bit less hard)
        self.TILE_SIZE = 80

    def redraw(self):
        """
        Whenever a scenario is been created or loaded new we need to draw the whole map.
        """
        self.scene.clear()

        columns = editor_scenario.scenario[constants.ScenarioProperty.MAP_COLUMNS]
        rows = editor_scenario.scenario[constants.ScenarioProperty.MAP_ROWS]

        width = (columns + 0.5) * self.TILE_SIZE
        height = rows * self.TILE_SIZE
        self.scene.setSceneRect(0, 0, width, height)

        # TODO should load only once and cache (universal cache), should be soft coded somewhere
        # load all textures
        brushes = {0: QtGui.QBrush(QtGui.QColor(64, 64, 255)), 1: QtGui.QBrush(QtGui.QColor(64, 255, 64)),
                   2: QtGui.QBrush(QtGui.QColor(64, 255, 64)), 3: QtGui.QBrush(QtGui.QColor(64, 255, 64)),
                   4: QtGui.QBrush(QtGui.QColor(222, 222, 222)), 5: QtGui.QBrush(QtGui.QColor(0, 128, 0)),
                   6: QtGui.QBrush(QtGui.QColor(222, 222, 0))}

        # fill the ground layer with ocean
        item = self.scene.addRect(0, 0, width, height, brush=brushes[0], pen=qt.TRANSPARENT_PEN)
        item.setZValue(0)

        # fill plains, hills, mountains, tundra, swamp, desert with texture

        # go through each position
        paths = {}
        for t in range(1, 7):
            paths[t] = QtGui.QPainterPath()
        for column in range(0, columns):
            for row in range(0, rows):
                t = editor_scenario.scenario.terrain_at(column, row)
                if t != 0:
                    # not for sea
                    sx, sy = editor_scenario.scenario.scene_position(column, row)
                    paths[t].addRect(sx * self.TILE_SIZE, sy * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
        for t in paths:
            path = paths[t]
            path = path.simplified()
            item = self.scene.addPath(path, brush=brushes[t], pen=qt.TRANSPARENT_PEN)
            item.setZValue(1)

        # fill the half tiles which are not part of the map
        brush = QtGui.QBrush(QtCore.Qt.darkGray)
        for row in range(0, rows):
            if row % 2 == 0:
                item = self.scene.addRect(columns * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE / 2,
                                          self.TILE_SIZE, pen=qt.TRANSPARENT_PEN)
            else:
                item = self.scene.addRect(0, row * self.TILE_SIZE, self.TILE_SIZE / 2, self.TILE_SIZE,
                                          pen=qt.TRANSPARENT_PEN)
            item.setBrush(brush)
            item.setZValue(1)

        # draw rivers
        river_pen = QtGui.QPen(QtGui.QColor(64, 64, 255))
        river_pen.setWidth(5)
        # TODO get rivers via a method (generator)
        for river in editor_scenario.scenario[constants.ScenarioProperty.RIVERS]:
            tiles = river['tiles']
            path = QtGui.QPainterPath()
            for tile in tiles:
                sx, sy = editor_scenario.scenario.scene_position(tile[0], tile[1])
                x = (sx + 0.5) * self.TILE_SIZE
                y = (sy + 0.5) * self.TILE_SIZE
                if tile == tiles[0]:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)
            item = self.scene.addPath(path, pen=river_pen)
            item.setZValue(2)

        # draw province and nation borders
        # TODO the whole border drawing is a crude approximation, implement it the right way
        province_border_pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
        province_border_pen.setWidth(2)
        nation_border_pen = QtGui.QPen()
        nation_border_pen.setWidth(4)
        for nation in editor_scenario.scenario.nations():
            # get nation color
            color = editor_scenario.scenario.nation_property(nation, constants.NationProperty.COLOR)
            nation_color = QtGui.QColor()
            nation_color.setNamedColor(color)
            # get all provinces
            provinces = editor_scenario.scenario.provinces_of_nation(nation)
            nation_path = QtGui.QPainterPath()
            # get all tiles
            for province in provinces:
                province_path = QtGui.QPainterPath()
                tiles = editor_scenario.scenario.province_property(province, constants.ProvinceProperty.TILES)
                for column, row in tiles:
                    sx, sy = editor_scenario.scenario.scene_position(column, row)
                    province_path.addRect(sx * self.TILE_SIZE, sy * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                province_path = province_path.simplified()
                item = self.scene.addPath(province_path, pen=province_border_pen)
                item.setZValue(4)
                nation_path.addPath(province_path)
            nation_path = nation_path.simplified()
            nation_border_pen.setColor(nation_color)
            item = self.scene.addPath(nation_path, pen=nation_border_pen)
            item.setZValue(5)

        # draw towns and names
        city_pixmap = QtGui.QPixmap(constants.extend(constants.GRAPHICS_MAP_FOLDER, 'city.png'))
        for nation in editor_scenario.scenario.nations():
            # get all provinces of this nation
            provinces = editor_scenario.scenario.provinces_of_nation(nation)
            for province in provinces:
                column, row = editor_scenario.scenario.province_property(province,
                                                                         constants.ProvinceProperty.TOWN_LOCATION)
                sx, sy = editor_scenario.scenario.scene_position(column, row)
                # center city image on center of tile
                x = (sx + 0.5) * self.TILE_SIZE - city_pixmap.width() / 2
                y = (sy + 0.5) * self.TILE_SIZE - city_pixmap.height() / 2
                item = self.scene.addPixmap(city_pixmap)
                item.setOffset(x, y)
                item.setZValue(6)
                # display province name below
                province_name = editor_scenario.scenario.province_property(province, constants.ProvinceProperty.NAME)
                item = self.scene.addSimpleText(province_name)
                item.setPen(qt.TRANSPARENT_PEN)
                item.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
                x = (sx + 0.5) * self.TILE_SIZE - item.boundingRect().width() / 2
                y = (sy + 1) * self.TILE_SIZE - item.boundingRect().height()
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

        # draw the grid and the coordinates
        for column in range(0, columns):
            for row in range(0, rows):
                sx, sy = editor_scenario.scenario.scene_position(column, row)
                # item = self.scene.addRect(sx * self.tile_size, sy * self.tile_size,  self.tile_size,  self.tile_size)
                # item.setZValue(1000)
                text = '({},{})'.format(column, row)
                item = QtWidgets.QGraphicsSimpleTextItem(text)
                item.setBrush(QtGui.QBrush(QtCore.Qt.black))
                item.setPos((sx + 0.5) * self.TILE_SIZE - item.boundingRect().width() / 2, sy * self.TILE_SIZE)
                item.setZValue(1001)
                self.scene.addItem(item)

        # emit focus changed with -1, -1
        self.focus_changed.emit(-1, -1)

    def visible_rect(self):
        """
        Returns the visible part of the map view relative to the total scene rectangle as a rectangle with normalized
        values between 0 and 1, relative to the total size of the map.
        """
        # total rectangle of the scene (0, 0, width, height)
        s = self.scene.sceneRect()
        # visible rectangle of the view
        v = self.mapToScene(self.rect()).boundingRect()
        return QtCore.QRectF(v.x() / s.width(), v.y() / s.height(), v.width() / s.width(), v.height() / s.height())

    def set_center_position(self, x, y):
        """
        Changes the visible part of the view by centering the map on normalized positions [0,1) (x,y).
        """
        # total rectangle of the scene (0, 0, width, height)
        s = self.scene.sceneRect()
        # visible rectangle of the view
        v = self.mapToScene(self.rect()).boundingRect()
        # adjust x, y to scene coordinates and find center
        x = x * s.width() + v.width() / 2
        y = y * s.height() + v.height() / 2
        # center on it
        self.centerOn(x, y)

    def mouseMoveEvent(self, event):  # noqa: N802
        """
        The mouse on the view has been moved. Emit signal focus_changed if we now hover over a different tile.
        """
        if editor_scenario.scenario is not None:
            # get mouse position in scene coordinates
            scene_position = self.mapToScene(event.pos()) / self.TILE_SIZE
            column, row = editor_scenario.scenario.map_position(scene_position.x(), scene_position.y())

            if column != self.current_column or row != self.current_row:
                self.current_column = column
                self.current_row = row
                self.focus_changed.emit(column, row)
        super().mouseMoveEvent(event)

    def contextMenuEvent(self, event):  # noqa: N802
        """
        Right click (context click) on a tile. Shows the context menu, depending on the tile position
        """

        # if there is no scenario existing, don't process the context click
        if not editor_scenario.scenario:
            return

        # get mouse position in scene coordinates
        scene_position = self.mapToScene(event.pos()) / self.TILE_SIZE
        column, row = editor_scenario.scenario.map_position(scene_position.x(), scene_position.y())

        # create context menu
        menu = QtWidgets.QMenu(self)

        # change terrain
        a = qt.create_action(tools.load_ui_icon('icon.editor.change_terrain.png'), 'Set terrain', self,
                             partial(self.change_terrain.emit, column, row))
        menu.addAction(a)

        # is there a province
        province = editor_scenario.scenario.province_at(column, row)
        if province:
            a = qt.create_action(tools.load_ui_icon('icon.editor.province_info.png'), 'Province info', self,
                                 partial(self.province_info.emit, province))
            menu.addAction(a)

            # is there also nation
            nation = editor_scenario.scenario.province_property(province, constants.ProvinceProperty.NATION)
            if nation:
                a = qt.create_action(tools.load_ui_icon('icon.editor.nation_info.png'), 'Nation info', self,
                                     partial(self.nation_info.emit, nation))
                menu.addAction(a)

        menu.exec(event.globalPos())


class ChangeTerrainWidget(QtWidgets.QGraphicsView):
    """

    """

    #: signal, if emitted a new terrain has been chosen
    terrain_selected = QtCore.pyqtSignal(int)

    def __init__(self, column, row):
        super().__init__()

        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # TODO see EditorMap redraw
        brushes = {0: QtGui.QBrush(QtGui.QColor(64, 64, 255)), 1: QtGui.QBrush(QtGui.QColor(64, 255, 64)),
                   2: QtGui.QBrush(QtGui.QColor(64, 255, 64)), 3: QtGui.QBrush(QtGui.QColor(64, 255, 64)),
                   4: QtGui.QBrush(QtGui.QColor(222, 222, 222)), 5: QtGui.QBrush(QtGui.QColor(0, 128, 0)),
                   6: QtGui.QBrush(QtGui.QColor(222, 222, 0))}

        # TODO hardcore tile size somewhere else (and a bit less hard)
        self.TILE_SIZE = 80

        for i in range(0, 6):
            y = i // 4
            x = i % 4
            self.scene.addRect(x * self.TILE_SIZE, y * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE,
                               brush=brushes[i], pen=qt.TRANSPARENT_PEN)


class InfoPanel(QtWidgets.QWidget):
    """
    Info box on the right side of the editor.
    """

    def __init__(self):
        """
        Layout.
        """
        super().__init__()
        self.setObjectName('info-box-widget')
        layout = QtWidgets.QVBoxLayout(self)

        self.tile_label = QtWidgets.QLabel()
        self.tile_label.setTextFormat(QtCore.Qt.RichText)
        layout.addWidget(self.tile_label)

        self.province_label = QtWidgets.QLabel()
        layout.addWidget(self.province_label)

        self.nation_label = QtWidgets.QLabel()
        layout.addWidget(self.nation_label)

        layout.addStretch()

    def update_tile_info(self, column, row):
        """
        Displays data of a new tile (hovered or clicked in the main map).

        :param column: The tile column.
        :param row: The tile row.
        """
        text = 'Position ({}, {})'.format(column, row)
        terrain = editor_scenario.scenario.terrain_at(column, row)
        terrain_name = editor_scenario.scenario.terrain_name(terrain)
        text += '<br>Terrain: {}'.format(terrain_name)
        province = editor_scenario.scenario.province_at(column, row)
        if province is not None:
            name = editor_scenario.scenario.province_property(province, constants.ProvinceProperty.NAME)
            text += '<br>Province: {}'.format(name)

        self.tile_label.setText(text)


class NewScenarioWidget(QtWidgets.QWidget):
    """
    New scenario dialog.
    """

    #: signal, emitted if this dialog finishes successfully and transmits parameters in the dictionary
    finished = QtCore.pyqtSignal(object)
    # see also: https://stackoverflow.com/questions/43964766/pyqt-emit-signal-with-dict
    # and https://www.riverbankcomputing.com/pipermail/pyqt/2017-May/039175.html
    # may be changed back to dict with a later PyQt5 version

    def __init__(self, *args, **kwargs):
        """
        Sets up all the input elements of the create new scenario dialog.
        """
        super().__init__(*args, **kwargs)

        self.parameters = {}
        widget_layout = QtWidgets.QVBoxLayout(self)

        # title box
        box = QtWidgets.QGroupBox('Title')
        layout = QtWidgets.QVBoxLayout(box)
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        edit.setPlaceholderText('Unnamed')
        self.parameters[constants.ScenarioProperty.TITLE] = edit
        layout.addWidget(edit)
        widget_layout.addWidget(box)

        # map size
        box = QtWidgets.QGroupBox('Map size')
        layout = QtWidgets.QHBoxLayout(box)

        layout.addWidget(QtWidgets.QLabel('Width'))
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(50)
        edit.setValidator(QtGui.QIntValidator(1, 1000))
        edit.setPlaceholderText('100')
        self.parameters[constants.ScenarioProperty.MAP_COLUMNS] = edit
        layout.addWidget(edit)

        layout.addWidget(QtWidgets.QLabel('Height'))
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(50)
        edit.setValidator(QtGui.QIntValidator(1, 1000))
        edit.setPlaceholderText('60')
        self.parameters[constants.ScenarioProperty.MAP_ROWS] = edit
        layout.addWidget(edit)
        layout.addStretch()

        widget_layout.addWidget(box)

        # vertical stretch
        widget_layout.addStretch()

        # add confirmation button
        layout = QtWidgets.QHBoxLayout()
        toolbar = QtWidgets.QToolBar()
        a = qt.create_action(tools.load_ui_icon('icon.confirm.png'), 'Create new scenario', toolbar, self.on_ok)
        toolbar.addAction(a)
        layout.addStretch()
        layout.addWidget(toolbar)
        widget_layout.addLayout(layout)

    def on_ok(self):
        """
        "Create scenario" has been clicked.
        """
        p = {}

        # title
        key = constants.ScenarioProperty.TITLE
        p[key] = get_text(self.parameters[key])

        # number of columns
        key = constants.ScenarioProperty.MAP_COLUMNS
        p[key] = int(get_text(self.parameters[key]))

        # number of rows
        key = constants.ScenarioProperty.MAP_ROWS
        p[key] = int(get_text(self.parameters[key]))

        # TODO conversion can fail, (ValueError) give error message
        # we close the parent window and emit the appropriate signal
        self.parent().close()
        self.finished.emit(p)


def get_text(edit: QtWidgets.QLineEdit):
    """
    Returns the text of a line edit. However, if it is empty, it returns the place holder text (whatever there is).

    :param edit: The line edit
    :return: The text
    """
    if edit.text():
        return edit.text()
    else:
        return edit.placeholderText()


class ScenarioPropertiesWidget(QtWidgets.QWidget):
    """
    Modify general properties of a scenario dialog.
    """

    # TODO same mechanism like for preferences?
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget_layout = QtWidgets.QVBoxLayout(self)

        # title
        # TODO validator for title, no empty string
        self.title_edit = QtWidgets.QLineEdit()
        self.title_edit.setFixedWidth(300)
        self.title_edit.setText(editor_scenario.scenario[constants.ScenarioProperty.TITLE])
        widget_layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Title'), self.title_edit)))

        # description
        self.description_edit = QtWidgets.QLineEdit()
        self.description_edit.setFixedWidth(300)
        self.description_edit.setText(editor_scenario.scenario[constants.ScenarioProperty.DESCRIPTION])
        widget_layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Description'), self.description_edit)))

        # game years
        game_range = editor_scenario.scenario[constants.ScenarioProperty.GAME_YEAR_RANGE]
        self.game_year_from = QtWidgets.QLineEdit()
        self.game_year_from.setFixedWidth(100)
        self.game_year_from.setText(str(game_range[0]))
        self.game_year_to = QtWidgets.QLineEdit()
        self.game_year_to.setFixedWidth(100)
        self.game_year_to.setText(str(game_range[1]))
        widget_layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Time range from'), self.game_year_from,
                                                      QtWidgets.QLabel('to'), self.game_year_to)))

        # vertical stretch
        widget_layout.addStretch()

    def on_ok(self):
        """
        We may have changes to apply.
        """
        pass

    def close_request(self, parent_widget):
        """
        Dialog will be closed, save data.
        """
        editor_scenario.scenario[constants.ScenarioProperty.TITLE] = self.title_edit.text()
        editor_scenario.scenario[constants.ScenarioProperty.DESCRIPTION] = self.description_edit.text()

        return True


class NationPropertiesWidget(QtWidgets.QWidget):
    """
    Modify nation properties dialog
    """
    # TODO when exiting redraw the big map

    def __init__(self, initial_nation=None):
        super().__init__()

        widget_layout = QtWidgets.QVBoxLayout(self)

        # toolbar
        toolbar = QtWidgets.QToolBar()
        a = qt.create_action(tools.load_ui_icon('icon.add.png'), 'Add nation', toolbar, self.add_nation)
        toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.delete.png'), 'Remove nation', toolbar, self.remove_nation)
        toolbar.addAction(a)
        widget_layout.addLayout(qt.wrap_in_boxlayout(toolbar))

        # nation selection combo box
        label = QtWidgets.QLabel('Choose')
        self.nation_combobox = QtWidgets.QComboBox()
        self.nation_combobox.setFixedWidth(200)
        self.nation_combobox.currentIndexChanged.connect(self.nation_selected)
        widget_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, self.nation_combobox)), 'Nations'))

        # nation info panel
        layout = QtWidgets.QVBoxLayout()

        # description
        self.description_edit = QtWidgets.QLineEdit()
        self.description_edit.setFixedWidth(300)
        self.description_edit.setText('Test')
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Description'), self.description_edit)))

        # color
        self.color_picker = QtWidgets.QPushButton()
        self.color_picker.setFixedSize(24, 24)
        self.color_picker.clicked.connect(self.show_color_picker)
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Color'), self.color_picker)))

        # capital province
        self.capital_province_edit = QtWidgets.QLineEdit()
        self.capital_province_edit.setFixedWidth(300)
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Capital'), self.capital_province_edit)))

        # all provinces
        self.provinces_combobox = QtWidgets.QComboBox()
        self.provinces_combobox.setFixedWidth(300)
        self.number_provinces_label = QtWidgets.QLabel()
        layout.addLayout(qt.wrap_in_boxlayout((self.number_provinces_label, self.provinces_combobox)))

        widget_layout.addWidget(qt.wrap_in_groupbox(layout, 'Info'))

        # vertical stretch
        widget_layout.addStretch()

        # reset content
        self.reset_content()

        # select initial nation if given
        if initial_nation:
            index = utils.index_of_element(self.nations, initial_nation)
            self.nation_combobox.setCurrentIndex(index)

    def show_color_picker(self):
        """
        Selects a color
        """
        new_color = QtWidgets.QColorDialog.getColor(self.color, parent=self)
        # isValid() returns True if dialog wasn't cancelled
        if new_color.isValid():

            index = self.nation_combobox.currentIndex()
            nation = self.nations[index]
            editor_scenario.scenario.set_nation_property(nation, constants.NationProperty.COLOR, new_color.name())

            self.nation_selected(index)

    def reset_content(self):
        """
        With data.

        """
        # get all nation ids
        nations = editor_scenario.scenario.nations()
        # get names for all nations
        name_of_nation = [(editor_scenario.scenario.nation_property(nation, constants.NationProperty.NAME), nation)
                          for nation in nations]
        if name_of_nation:
            name_of_nation = sorted(name_of_nation)  # by first element, which is the name
            nation_names, self.nations = zip(*name_of_nation)
        else:
            nation_names = []
            self.nations = []
        self.nation_combobox.clear()
        self.nation_combobox.addItems(nation_names)

    def nation_selected(self, index):
        """
        A nation is selected

        :param index:
        """
        nation = self.nations[index]
        self.description_edit.setText(editor_scenario.scenario.nation_property(nation,
                                                                               constants.NationProperty.DESCRIPTION))

        province = editor_scenario.scenario.nation_property(nation, constants.NationProperty.CAPITAL_PROVINCE)
        self.capital_province_edit.setText(editor_scenario.scenario.province_property(province,
                                                                                      constants.ProvinceProperty.NAME))

        # color
        color_name = editor_scenario.scenario.nation_property(nation, constants.NationProperty.COLOR)
        self.color = QtGui.QColor(color_name)
        self.color_picker.setStyleSheet('QPushButton { background-color: ' + color_name + '; }')

        provinces = editor_scenario.scenario.nation_property(nation, constants.NationProperty.PROVINCES)
        provinces_names = [editor_scenario.scenario.province_property(p, constants.ProvinceProperty.NAME)
                           for p in provinces]
        self.number_provinces_label.setText('Provinces ({})'.format(len(provinces)))
        self.provinces_combobox.clear()
        self.provinces_combobox.addItems(provinces_names)

    def add_nation(self):
        """
        Adds a nation.
        """
        name, ok = QtWidgets.QInputDialog.getText(self, 'Add Nation', 'Name')
        if ok:
            # TODO what if nation with the same name already exists
            # TODO check for sanity of name (no special letters, minimal number of letters)
            nation = editor_scenario.scenario.add_nation()
            editor_scenario.scenario.set_nation_property(nation, constants.NationProperty.NAME, name)
            # reset content
            self.reset_content()

    def remove_nation(self):
        """
        Removes a nation.
        """
        index = self.nation_combobox.currentIndex()
        name = self.nation_combobox.currentText()
        answer = QtWidgets.QMessageBox.question(self, 'Warning', 'Remove {}'.format(name),
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.Yes)
        if answer == QtWidgets.QMessageBox.Yes:
            nation = self.nations[index]

            # there is no going back on this one
            editor_scenario.scenario.remove_nation(nation)

            # reset content
            self.reset_content()


class ProvincePropertiesWidget(QtWidgets.QWidget):
    """
    Modify provinces properties dialog.
    """

    def __init__(self, initial_province=None):
        super().__init__()

        widget_layout = QtWidgets.QVBoxLayout(self)

        # toolbar
        toolbar = QtWidgets.QToolBar()
        a = qt.create_action(tools.load_ui_icon('icon.add.png'), 'Add province', toolbar, self.add_province)
        toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.delete.png'), 'Remove province', toolbar, self.remove_province)
        toolbar.addAction(a)
        widget_layout.addLayout(qt.wrap_in_boxlayout(toolbar))

        # provinces selection combo box
        label = QtWidgets.QLabel('Choose')
        self.provinces_combobox = QtWidgets.QComboBox()
        self.provinces_combobox.setFixedWidth(200)
        self.provinces_combobox.currentIndexChanged.connect(self.province_combobox_index_changed)
        widget_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, self.provinces_combobox)),
                                                    'provinces'))

        # province info panel
        layout = QtWidgets.QVBoxLayout()

        # nation
        self.nation_label = QtWidgets.QLabel('Nation')
        layout.addWidget(self.nation_label)

        widget_layout.addWidget(qt.wrap_in_groupbox(layout, 'Info'))

        # vertical stretch
        widget_layout.addStretch()

        # reset content
        self.reset_content()

        # if province is given, select it
        if initial_province:
            index = utils.index_of_element(self.provinces, initial_province)
            self.provinces_combobox.setCurrentIndex(index)

    def reset_content(self):
        """
        Resets the content.
        """

        # get all province ids
        provinces = editor_scenario.scenario.provinces()
        # get names for all provinces
        name_of_province = [
            (editor_scenario.scenario.province_property(province, constants.ProvinceProperty.NAME), province)
            for province in provinces]
        if name_of_province:
            name_of_province = sorted(name_of_province)  # by first element, which is the name
            province_names, self.provinces = zip(*name_of_province)
        else:
            province_names = []
            self.provinces = []
        self.provinces_combobox.clear()
        self.provinces_combobox.addItems(province_names)

    def province_combobox_index_changed(self, index):
        """

        :param index:
        """
        province = self.provinces[index]
        nation = editor_scenario.scenario.province_property(province, constants.ProvinceProperty.NATION)
        if nation:
            self.nation_label.setText(editor_scenario.scenario.nation_property(nation, constants.NationProperty.NAME))
        else:
            self.nation_label.setText('None')

    def add_province(self):
        """
        Adds a province.
        """
        name, ok = QtWidgets.QInputDialog.getText(self, 'Add Province', 'Name')
        if ok:
            # TODO what if province with the same name already exists
            # TODO check for sanity of name (no special letters, minimal number of letters)
            province = editor_scenario.scenario.add_province()
            editor_scenario.scenario.set_province_property(province, constants.ProvinceProperty.NAME, name)

            # reset content
            self.reset_content()

    def remove_province(self):
        """
        Removes a province.
        """
        index = self.provinces_combobox.currentIndex()
        name = self.provinces_combobox.currentText()
        answer = QtWidgets.QMessageBox.question(self, 'Warning', 'Remove {}'.format(name),
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.Yes)
        if answer == QtWidgets.QMessageBox.Yes:
            province = self.provinces[index]
            editor_scenario.scenario.remove_province(province)  # there is no going back on this one

            # reset content
            self.reset_content()


class EditorScenario(QtCore.QObject):
    """
    Wrap around the Scenario file to get notified of recreations
    """

    #: signal, scenario has changed completely
    changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.scenario = None

    def load(self, file_name):
        """

        :param file_name:
        """
        # TODO what if file name does not exist or is not a valid scenario file
        self.scenario = Scenario.from_file(file_name)
        self.changed.emit()

    def create(self, properties):
        """
        Create new scenario (from the create new scenario dialog).

        :param properties:
        """
        self.scenario = Scenario()
        self.scenario[constants.ScenarioProperty.TITLE] = properties[constants.ScenarioProperty.TITLE]
        self.scenario.create_empty_map(properties[constants.ScenarioProperty.MAP_COLUMNS],
                                       properties[constants.ScenarioProperty.MAP_ROWS])

        # standard rules
        self.scenario[constants.ScenarioProperty.RULES] = 'standard.rules'
        # self.scenario.load_rules()
        # TODO rules as extra?
        rule_file = constants.extend(constants.SCENARIO_RULESET_FOLDER,
                                     self.scenario[constants.ScenarioProperty.RULES])
        self.scenario._rules = utils.read_as_yaml(rule_file)

        # emit that everything has changed
        self.changed.emit()


#: static single instance of the editor scenario
editor_scenario = EditorScenario()


class EditorScreen(QtWidgets.QWidget):
    """
    The screen the contains the whole scenario editor. Is copied into the application main window if the user
    clicks on the editor pixmap in the client main screen.
    """

    def __init__(self, client):
        """
        Create and setup all the elements.
        """
        super().__init__()

        # store the client
        self.client = client

        # toolbar on top of the window
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setIconSize(QtCore.QSize(32, 32))

        # new, load, save scenario actions
        a = qt.create_action(tools.load_ui_icon('icon.scenario.new.png'), 'Create new scenario', self,
                             self.new_scenario_dialog)
        self.toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.scenario.load.png'), 'Load scenario', self,
                             self.load_scenario_dialog)
        self.toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.scenario.save.png'), 'Save scenario', self,
                             self.save_scenario_dialog)
        self.toolbar.addAction(a)
        self.toolbar.addSeparator()

        # edit properties (general, nations, provinces) actions
        a = qt.create_action(tools.load_ui_icon('icon.editor.general.png'), 'Edit general properties', self,
                             self.general_properties_dialog)
        self.toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.editor.nations.png'), 'Edit nations', self, self.nations_dialog)
        self.toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.editor.provinces.png'), 'Edit provinces', self,
                             self.provinces_dialog)
        self.toolbar.addAction(a)

        # spacer
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        clock = qt.ClockLabel()
        self.toolbar.addWidget(clock)

        # help and exit action
        a = QtWidgets.QAction(tools.load_ui_icon('icon.help.png'), 'Show help', self)
        a.triggered.connect(client.show_help_browser)  # TODO with partial make reference to specific page
        self.toolbar.addAction(a)
        a = QtWidgets.QAction(tools.load_ui_icon('icon.back_to_startscreen.png'), 'Exit to main menu', self)
        a.triggered.connect(client.switch_to_start_screen)
        # TODO ask if something is changed we should save.. (you might loose progress)
        self.toolbar.addAction(a)

        # info box widget
        self.info_panel = InfoPanel()

        # main map
        self.main_map = MainMap()
        self.main_map.focus_changed.connect(self.info_panel.update_tile_info)
        self.main_map.change_terrain.connect(self.map_change_terrain)
        self.main_map.province_info.connect(self.provinces_dialog)
        self.main_map.nation_info.connect(self.nations_dialog)

        # mini map
        self.mini_map = MiniMap()
        self.mini_map.roi_changed.connect(self.main_map.set_center_position)

        # connect to editor_scenario
        editor_scenario.changed.connect(self.scenario_changed)

        # layout of widgets and toolbar
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.toolbar, 0, 0, 1, 2)
        layout.addWidget(self.mini_map, 1, 0)
        layout.addWidget(self.info_panel, 2, 0)
        layout.addWidget(self.main_map, 1, 1, 2, 1)
        layout.setRowStretch(2, 1)  # the info box will take all vertical space left
        layout.setColumnStretch(1, 1)  # the main map will take all horizontal space left

    def map_change_terrain(self, column, row):
        """

        :param column:
        :param row:
        """
        content_widget = ChangeTerrainWidget(column, row)
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='Change terrain',
                                     delete_on_close=True, help_callback=self.client.show_help_browser)
        #dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()

    def scenario_changed(self):
        """
        Update the GUI in the right order.
        """

        # first repaint the map
        self.main_map.redraw()

        # repaint the overview
        self.mini_map.redraw()

        # show the tracker rectangle in the overview with the right size
        self.mini_map.activate_tracker(self.main_map.visible_rect())

    def new_scenario_dialog(self):
        """
        Shows the dialog for creation of a new scenario dialog and connect the "create new scenario" signal.
        """
        content_widget = NewScenarioWidget()
        content_widget.finished.connect(editor_scenario.create)
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='New Scenario',
                                     delete_on_close=True, help_callback=self.client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(600, 400))
        dialog.show()

    def load_scenario_dialog(self):
        """
        Show the load a scenario dialog. Then loads it if the user has selected one.
        """
        # noinspection PyCallByClass
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Scenario', constants.SCENARIO_FOLDER,
                                                          'Scenario Files (*.scenario)')[0]
        if file_name:
            editor_scenario.load(file_name)
            self.client.schedule_notification('Loaded scenario {}'
                                              .format(editor_scenario.scenario[constants.ScenarioProperty.TITLE]))

    def save_scenario_dialog(self):
        """
            Show the save a scenario dialog. Then saves it.
        """
        # noinspection PyCallByClass
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Scenario', constants.SCENARIO_FOLDER,
                                                          'Scenario Files (*.scenario)')[0]
        if file_name:
            editor_scenario.scenario.save(file_name)
            path, name = os.path.split(file_name)
            self.client.schedule_notification('Saved to {}'.format(name))

    def general_properties_dialog(self):
        """
        Display the modify general properties dialog.
        """
        if not editor_scenario.scenario:
            return

        content_widget = ScenarioPropertiesWidget()
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='General Properties',
                                     delete_on_close=True, help_callback=self.client.show_help_browser,
                                     close_callback=content_widget.close_request)
        # TODO derive meaningful size depending on screen size
        dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()

    def nations_dialog(self, nation=None):
        """
        Show the modify nations dialog.
        """
        if not editor_scenario.scenario:
            return

        content_widget = NationPropertiesWidget(nation)
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='Nations', delete_on_close=True,
                                     help_callback=self.client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()

    def provinces_dialog(self, province=None):
        """
            Display the modify provinces dialog.
        """
        if not editor_scenario.scenario:
            return

        content_widget = ProvincePropertiesWidget(province)
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='Provinces', delete_on_close=True,
                                     help_callback=self.client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()
