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

from PyQt5 import QtWidgets, QtCore

from imperialism_remake.base import tools
from imperialism_remake.client.common.info_panel import InfoPanel
from imperialism_remake.client.common.mini_map import MiniMap
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


class GenericScreen(QtWidgets.QWidget):
    """
    The screen the contains the whole scenario editor. Is copied into the application main window if the user
    clicks on the editor pixmap in the client main screen.
    """

    def __init__(self, client, scenario, main_map):
        """
        Create and setup all the elements.
        """
        super().__init__()

        logger.debug('GenericScreen __init__')

        # store the client
        self._client = client

        self.scenario = scenario

        # toolbar on top of the window
        self._toolbar = QtWidgets.QToolBar()
        self._toolbar.setIconSize(QtCore.QSize(32, 32))

        self._toolbar.addSeparator()

        # spacer
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._toolbar.addWidget(spacer)

        clock = qt.ClockLabel()
        self._toolbar.addWidget(clock)

        # help and exit action
        a = QtWidgets.QAction(tools.load_ui_icon('icon.help.png'), 'Show help', self)
        a.triggered.connect(client.show_help_browser)  # TODO with partial make reference to specific page
        self._toolbar.addAction(a)

        a = QtWidgets.QAction(tools.load_ui_icon('icon.back_to_startscreen.png'), 'Exit to main menu', self)
        a.triggered.connect(client.switch_to_start_screen)
        # TODO ask if something is changed we should save.. (you might loose progress)
        self._toolbar.addAction(a)

        # info box widget
        self._info_panel = InfoPanel(scenario)

        # main map
        self.main_map = main_map
        self.main_map.focus_changed.connect(self._info_panel.update_tile_info)

        # mini map
        self._mini_map = MiniMap(scenario)
        self._mini_map.roi_changed.connect(self.main_map.set_center_position)

        # connect to scenario
        scenario.changed.connect(self.scenario_changed)

        # layout of widgets and toolbar
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self._toolbar, 0, 0, 1, 2)
        layout.addWidget(self._mini_map, 1, 0)
        layout.addWidget(self._info_panel, 2, 0)
        layout.addWidget(self.main_map, 1, 1, 2, 1)
        layout.setRowStretch(2, 1)  # the info box will take all vertical space left
        layout.setColumnStretch(1, 1)  # the main map will take all horizontal space left

    def scenario_changed(self):
        """
        Update the GUI in the right order.
        """

        logger.debug('scenario_changed')

        # first repaint the map
        self.main_map.redraw()

        # repaint the overview
        self._mini_map.redraw()

        # show the tracker rectangle in the overview with the right size
        self._mini_map.activate_tracker(self.main_map.visible_rect())
