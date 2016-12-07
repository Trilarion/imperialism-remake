# Imperialism remake
# Copyright (C) 2015-16 Trilarion
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
The main game screen.
"""

import math
from PyQt5 import QtWidgets, QtCore

from imperialism_remake.base import tools, constants
from imperialism_remake.lib import qt

# TODO merge with minimap of the editor
class MiniMap(QtWidgets.QWidget):
    """
    Mini map on the left upper side.
    """

    # Fixed width of 300 pixels
    VIEW_WIDTH = 300

    #: signal, emitted if the user clicks somewhere in the mini map and the ROI rectangle changes as a result, sends the normalized x and y position of the center of the new ROI
    roi_changed = QtCore.pyqtSignal(float, float)

    def __init__(self, *args, **kwargs):
        """
        Sets up the graphics view.
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


    def switch_to_political_view(self, checked):
        """
            The toolbar button for the political view has been toggled.
        """
        if checked:
            # mode should not be political
            self.mode = constants.OverviewMapMode.POLITICAL
            #self.redraw()


    def switch_to_geographical_view(self, checked):
        """
            The toolbar button for the geographical view has been toggled.
        """
        if checked:
            # mode should not be geographical
            self.mode = constants.OverviewMapMode.GEOGRAPHICAL
            #self.redraw()


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


class MainMap(QtWidgets.QGraphicsView):
    """
        Main map on the right side.
    """

    def __init__(self):
        super().__init__()


class InfoBox(QtWidgets.QWidget):
    """
    Info box on the left lower side.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GameMainScreen(QtWidgets.QWidget):
    """
        The whole screen (layout of single elements and interactions.
    """

    def __init__(self, client):
        super().__init__()

        self.toolbar = QtWidgets.QToolBar()
        action_help = QtWidgets.QAction(tools.load_ui_icon('icon.help.png'), 'Show help', self)
        action_help.triggered.connect(client.show_help_browser)  # TODO with partial make reference to specific page
        self.toolbar.addAction(action_help)

        action_quit = QtWidgets.QAction(tools.load_ui_icon('icon.back_to_startscreen.png'), 'Exit to main menu', self)
        action_quit.triggered.connect(client.switch_to_start_screen)
        self.toolbar.addAction(action_quit)

        # main map
        self.main_map = MainMap()

        # mini map
        self.mini_map = MiniMap()

        # info box
        self.info_box = InfoBox()

        # layout
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.toolbar, 0, 0)
        layout.addWidget(self.mini_map, 1, 0)
        layout.addWidget(self.info_box, 2, 0)
        layout.addWidget(self.main_map, 0, 1, 3, 1)
        layout.setRowStretch(2, 1)  # the info box will take all vertical space left
        layout.setColumnStretch(1, 1)  # the main map will take all horizontal space left
