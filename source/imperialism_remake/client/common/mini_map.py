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

from PyQt5 import QtCore, QtGui, QtWidgets

from imperialism_remake.base import constants, tools
from imperialism_remake.client.utils.scene_utils import scene_position
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


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

    def __init__(self, scenario):
        """
        Sets up the graphics view, the toolbar and the tracker rectangle.
        """
        super().__init__()

        logger.debug('__init__')

        self.scenario = scenario

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
        tl = QtWidgets.QHBoxLayout()
        tl.setContentsMargins(0, 0, 0, 0)
        tl.addWidget(self.toolbar)
        tl.addStretch()

        # add layout containing tool bar
        layout.addLayout(tl)

        # graphics items in scene (except the tracker)
        self.scene_items = []

    def redraw(self):
        """
        The scenario has changed or the mode has changed. Redraw the overview map.
        """
        logger.debug('redraw')

        # get number of columns and rows from the scenario
        columns = self.scenario.server_scenario[constants.ScenarioProperty.MAP_COLUMNS]
        rows = self.scenario.server_scenario[constants.ScenarioProperty.MAP_ROWS]

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
            for nation in self.scenario.server_scenario.nations():
                # get nation color
                color_string = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.COLOR)
                color = QtGui.QColor()
                color.setNamedColor(color_string)
                # get all provinces
                provinces = self.scenario.server_scenario.provinces_of_nation(nation)
                tiles = []
                # get all tiles
                for province in provinces:
                    tiles.extend(self.scenario.server_scenario.province_property(province,
                                                                                 constants.ProvinceProperty.TILES))
                # get rectangular path for each tile
                path = QtGui.QPainterPath()
                for tile in tiles:
                    sx, sy = scene_position(*tile)
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
            for t in range(1, len(self.scenario.server_scenario.get_terrain_settings())):
                paths[t] = QtGui.QPainterPath()
            for column in range(0, columns):
                for row in range(0, rows):
                    t = self.scenario.server_scenario.terrain_at(column, row)
                    if t != 0:
                        # not for sea
                        sx, sy = scene_position(column, row)
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
        logger.debug('switch_to_political_view checked:%s', checked)

        if checked:
            # mode should not be political
            self.mode = constants.OverviewMapMode.POLITICAL
            self.redraw()

    def switch_to_geographical_view(self, checked):
        """
            The toolbar button for the geographical view has been toggled.
        """
        logger.debug('switch_to_geographical_view checked:%s', checked)

        if checked:
            # mode should not be geographical
            self.mode = constants.OverviewMapMode.GEOGRAPHICAL
            self.redraw()

    def mousePressEvent(self, event):  # noqa: N802
        """
        The mouse has been pressed inside the view. Center the tracker rectangle.
        """
        super().mousePressEvent(event)

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
