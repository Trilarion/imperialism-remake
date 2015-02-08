# Imperialism remake
# Copyright (C) 2015 Trilarion
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
"""

from PySide import QtGui

import base.tools as t

class MiniMap(QtGui.QWidget):

    def __init__(self):
        super().__init__()

class MainMap(QtGui.QGraphicsView):

    def __init__(self):
        super().__init__()

class InfoBox(QtGui.QWidget):

    def __init__(self):
        super().__init__()

class GameMainScreen(QtGui.QWidget):

    def __init__(self, client):
        super().__init__()

        self.toolbar = QtGui.QToolBar()
        action_help = QtGui.QAction(t.load_ui_icon('icon.help.png'), 'Show help', self)
        action_help.triggered.connect(client.show_help_browser)  # TODO with partial make reference to specific page
        self.toolbar.addAction(action_help)

        action_quit = QtGui.QAction(t.load_ui_icon('icon.back.startscreen.png'), 'Exit to main menu', self)
        # action_quit.triggered.connect(client.switch_to_start_screen)
        self.toolbar.addAction(action_quit)

        # mini map
        self.mini_map = MiniMap()

        # info box
        self.info_box = InfoBox()

        # main map
        self.main_map = MainMap()

        # layout
        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.toolbar, 0, 0)
        layout.addWidget(self.mini_map, 1, 0)
        layout.addWidget(self.info_box, 2, 0)
        layout.addWidget(self.main_map, 0, 1, 3, 1)
        layout.setRowStretch(2, 1)  # the info box will take all vertical space left
        layout.setColumnStretch(1, 1)  # the map will take all horizontal space left


