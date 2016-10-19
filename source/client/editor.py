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

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

import client.graphics as graphics
from base import constants, tools
from lib import qt, utils
from server.scenario import Scenario


class OverviewMap(QtWidgets.QWidget):
    """
    Small overview map
    """

    # TODO fixed width -> make it selectable from outside

    # Fixed width of 300 pixels
    VIEW_WIDTH = 300

    #: signal, emitted if the user clicks somewhere in the mini map and the ROI rectangle changes as a result, sends the normalized x and y position of the center of the new ROI
    roi_changed = QtCore.pyqtSignal(float, float)

    def __init__(self):
        """
        Sets up the graphics view, the toolbar and the tracker rectangle.
        """
        super().__init__()
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
        a = qt.create_action(tools.load_ui_icon('icon.mini.political.png'), 'Show political view', action_group, toggle_connection=self.switch_to_political_view, checkable=True)
        self.toolbar.addAction(a)
        # geographical view
        a = qt.create_action(tools.load_ui_icon('icon.mini.geographical.png'), 'Show geographical view', action_group, toggle_connection=self.switch_to_geographical_view, checkable=True)
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
        columns = editor_scenario.scenario[constants.ScenarioProperties.MAP_COLUMNS]
        rows = editor_scenario.scenario[constants.ScenarioProperties.MAP_ROWS]

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
                color_string = editor_scenario.scenario.nation_property(nation, 'color')
                color = QtGui.QColor()
                color.setNamedColor(color_string)
                # get all provinces
                provinces = editor_scenario.scenario.provinces_of_nation(nation)
                tiles = []
                # get all tiles
                for province in provinces:
                    tiles.extend(editor_scenario.scenario.province_property(province, 'tiles'))
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

    def mousePressEvent(self, event):
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


class EditorMap(QtWidgets.QGraphicsView):
    """
    The big map holding the game map and everything.
    """

    #: signal, emitted if the tile at the mouse pointer (focus) changes
    focus_changed = QtCore.pyqtSignal(int, int)

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

        columns = editor_scenario.scenario[constants.ScenarioProperties.MAP_COLUMNS]
        rows = editor_scenario.scenario[constants.ScenarioProperties.MAP_ROWS]

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
        for river in editor_scenario.scenario._properties['rivers']:
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
            color = editor_scenario.scenario.nation_property(nation, 'color')
            nation_color = QtGui.QColor()
            nation_color.setNamedColor(color)
            # get all provinces
            provinces = editor_scenario.scenario.provinces_of_nation(nation)
            nation_path = QtGui.QPainterPath()
            # get all tiles
            for province in provinces:
                province_path = QtGui.QPainterPath()
                tiles = editor_scenario.scenario.province_property(province, 'tiles')
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
                column, row = editor_scenario.scenario.province_property(province, 'town_location')
                sx, sy = editor_scenario.scenario.scene_position(column, row)
                # center city image on center of tile
                x = (sx + 0.5) * self.TILE_SIZE - city_pixmap.width() / 2
                y = (sy + 0.5) * self.TILE_SIZE - city_pixmap.height() / 2
                item = self.scene.addPixmap(city_pixmap)
                item.setOffset(x, y)
                item.setZValue(6)
                # display province name below
                province_name = editor_scenario.scenario.province_property(province, 'name')
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
                background = QtCore.QRectF(x - bx, y - by, item.boundingRect().width() + 2 * bx,
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

    def mouseMoveEvent(self, event):
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

    def contextMenuEvent(self, event):
        """

        """
        menu = QtWidgets.QMenu(self)
        change_terrain = QtWidgets.QAction(tools.load_ui_icon('icon.help.png'), '', self)
        menu.addAction(change_terrain)
        change_terrain = QtWidgets.QAction(tools.load_ui_icon('icon.help.png'), '', self)
        menu.addAction(change_terrain)
        menu.exec(event.globalPos())


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
            name = editor_scenario.scenario.province_property(province, 'name')
            text += '<br>Province: {}'.format(name)

        self.tile_label.setText(text)


class NewScenarioWidget(QtWidgets.QWidget):
    """
    New scenario dialog.
    """

    #: signal, emitted if this dialog finishes successfully and transmits parameters in the dictionary
    finished = QtCore.pyqtSignal(dict)

    def __init__(self):
        """
        Sets up all the input elements of the create new scenario dialog.
        """
        super().__init__()

        self.parameters = {}
        widget_layout = QtWidgets.QVBoxLayout(self)

        # title box
        box = QtWidgets.QGroupBox('Title')
        layout = QtWidgets.QVBoxLayout(box)
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        edit.setPlaceholderText('Unnamed')
        self.parameters[constants.ScenarioProperties.TITLE] = edit
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
        self.parameters[constants.ScenarioProperties.MAP_COLUMNS] = edit
        layout.addWidget(edit)

        layout.addWidget(QtWidgets.QLabel('Height'))
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(50)
        edit.setValidator(QtGui.QIntValidator(1, 1000))
        edit.setPlaceholderText('60')
        self.parameters[constants.ScenarioProperties.MAP_ROWS] = edit
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
        key = constants.ScenarioProperties.TITLE
        p[key] = get_text(self.parameters[key])

        # number of columns
        key = constants.ScenarioProperties.MAP_COLUMNS
        p[key] = int(get_text(self.parameters[key]))

        # number of rows
        key = constants.ScenarioProperties.MAP_ROWS
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


class GeneralPropertiesWidget(QtWidgets.QWidget):
    """
    Modify general properties of a scenario dialog.
    """

    def __init__(self):
        super().__init__()
        widget_layout = QtWidgets.QVBoxLayout(self)

        # title box
        # TODO validator for title, no empty string
        self.edit = QtWidgets.QLineEdit()
        self.edit.setFixedWidth(300)
        self.edit.setText(editor_scenario.scenario[constants.ScenarioProperties.TITLE])
        widget_layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Title'), self.edit)))

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
        editor_scenario.scenario[constants.ScenarioProperties.TITLE] = self.edit.text()
        return True


class NationPropertiesWidget(QtWidgets.QWidget):
    """
    Modify nation properties dialog
    """

    def __init__(self):
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
        combobox = QtWidgets.QComboBox()
        combobox.setFixedWidth(200)

        # get all nation ids
        nations = editor_scenario.scenario.nations()
        # get names for all nations
        name_of_nation = [(editor_scenario.scenario.nation_property(nation, constants.NationProperties.NAME), nation) for nation in nations]
        name_of_nation = sorted(name_of_nation)  # by first element, which is the name
        nation_names, self.nations_sorted = zip(*name_of_nation)
        combobox.addItems(nation_names)
        widget_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, combobox)), 'Nations'))

        # nation info panel
        layout = QtWidgets.QVBoxLayout()

        # name
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        edit.setText('Test')
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Name'), edit)))

        # description
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        edit.setText('Test')
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Description'), edit)))

        # color
        # TODO color and color selection

        # capital province
        combobox = QtWidgets.QComboBox()
        combobox.setFixedWidth(300)
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Capital'), combobox)))

        # all provinces
        combobox = QtWidgets.QComboBox()
        combobox.setFixedWidth(300)
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Provinces ({})'.format(4)), combobox)))

        widget_layout.addWidget(qt.wrap_in_groupbox(layout, "Info"))

        # vertical stretch
        widget_layout.addStretch()

    def add_nation(self):
        """
        Adds a nation.
        """
        pass


    def remove_nation(self):
        """
        Adds a nation.
        """
        pass

class ProvincePropertiesWidget(QtWidgets.QWidget):
    """
    Modify provinces properties dialog.
    """

    def __init__(self):
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
        combobox = QtWidgets.QComboBox()
        combobox.setFixedWidth(200)

        # get all province ids
        provinces = editor_scenario.scenario.provinces()
        # get names for all provinces
        name_of_province = [(editor_scenario.scenario.province_property(province, constants.ProvinceProperties.NAME), province) for province in provinces]
        name_of_province = sorted(name_of_province)  # by first element, which is the name
        province_names, self.provinces_sorted = zip(*name_of_province)
        combobox.addItems(province_names)
        widget_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, combobox)), 'provinces'))

        # vertical stretch
        widget_layout.addStretch()

    def add_province(self):
        """

        """
        pass


    def remove_province(self):
        """

        """
        pass

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
        self.scenario[constants.ScenarioProperties.TITLE] = properties[constants.ScenarioProperties.TITLE]
        self.scenario.create_empty_map(properties[constants.ScenarioProperties.MAP_COLUMNS],
            properties[constants.ScenarioProperties.MAP_ROWS])

        # standard rules
        self.scenario['rules'] = 'standard.rules'
        # self.scenario.load_rules()
        # TODO rules as extra?
        rule_file = constants.extend(constants.SCENARIO_RULESET_FOLDER, self.scenario._properties['rules'])
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

        # main map and overview map widgets
        self.map = EditorMap()
        self.map.focus_changed.connect(self.info_panel.update_tile_info)

        self.overview = OverviewMap()
        self.overview.roi_changed.connect(self.map.set_center_position)

        # connect to editor_scenario
        editor_scenario.changed.connect(self.scenario_changed)

        # layout of widgets and toolbar
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.toolbar, 0, 0, 1, 2)
        layout.addWidget(self.overview, 1, 0)
        layout.addWidget(self.info_panel, 2, 0)
        layout.addWidget(self.map, 1, 1, 2, 1)
        layout.setRowStretch(2, 1)  # the info box will take all vertical space left
        layout.setColumnStretch(1, 1)  # the map will take all horizontal space left

    def scenario_changed(self):
        """
        Update the GUI in the right order.
        """

        # first repaint the map
        self.map.redraw()

        # repaint the overview
        self.overview.redraw()

        # show the tracker rectangle in the overview with the right size
        self.overview.activate_tracker(self.map.visible_rect())

    def new_scenario_dialog(self):
        """
        Shows the dialog for creation of a new scenario dialog and connect the "create new scenario" signal.
        """
        content_widget = NewScenarioWidget()
        content_widget.finished.connect(editor_scenario.create)
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='New Scenario', delete_on_close=True,
            help_callback=self.client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(500, 400))
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
            self.client.schedule_notification(
                'Loaded scenario {}'.format(editor_scenario.scenario[constants.ScenarioProperties.TITLE]))

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

        content_widget = GeneralPropertiesWidget()
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='General Properties',
            delete_on_close=True, help_callback=self.client.show_help_browser,
            close_callback=content_widget.close_request)
        dialog.setFixedSize(QtCore.QSize(800, 600))
        dialog.show()

    def nations_dialog(self):
        """
        Show the modify nations dialog.
        """
        if not editor_scenario.scenario:
            return

        content_widget = NationPropertiesWidget()
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='Nations', delete_on_close=True,
            help_callback=self.client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(800, 600))
        dialog.show()

    def provinces_dialog(self):
        """
            Display the modify provinces dialog.
        """
        content_widget = ProvincePropertiesWidget()
        dialog = graphics.GameDialog(self.client.main_window, content_widget, title='Provinces', delete_on_close=True,
            help_callback=self.client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(800, 600))
        dialog.show()
