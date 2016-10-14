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

from PyQt5 import QtWidgets

import base.tools as tools


class MiniMap(QtWidgets.QWidget):
    """
        Mini map on the left upper side.
    """

    def __init__(self):
        super().__init__()


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

    def __init__(self):
        super().__init__()


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

        action_quit = QtWidgets.QAction(tools.load_ui_icon('icon.back.startscreen.png'), 'Exit to main menu', self)
        action_quit.triggered.connect(client.switch_to_start_screen)
        self.toolbar.addAction(action_quit)

        # mini map
        self.mini_map = MiniMap()

        # info box
        self.info_box = InfoBox()

        # main map
        self.main_map = MainMap()

        # layout
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.toolbar, 0, 0)
        layout.addWidget(self.mini_map, 1, 0)
        layout.addWidget(self.info_box, 2, 0)
        layout.addWidget(self.main_map, 0, 1, 3, 1)
        layout.setRowStretch(2, 1)  # the info box will take all vertical space left
        layout.setColumnStretch(1, 1)  # the map will take all horizontal space left
