# Imperialism remake
# Copyright (C) 2014 Trilarion
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

from PySide import QtCore, QtGui
import constants as c, tools as t, lib.graphics as g

class MiniMap(QtGui.QGraphicsView):

    def __init__(self):
        super().__init__()

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.setObjectName('mini_map')
        self.setStyleSheet('#mini_map{background-color: gray;border: 0px;}')
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        size = QtCore.QSize(300, 300)
        self.setSceneRect(0, 0, size.width(), size.height())
        self.setMinimumSize(size)

class Map(QtGui.QGraphicsView):

    def __init__(self):
        super().__init__()

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.setObjectName('map')
        self.setStyleSheet('#map{background-color: gray;border: 0px;}')
        self.setProperty('background', 'texture')
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

class InfoBox(QtGui.QLabel):

    def __init__(self):
        super().__init__()

        self.setText('Info box')
        self.setObjectName('info_box')
        self.setStyleSheet('#info_box{background-color: gray;}')

class NewScenarioDialogWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()

        layout = QtGui.QVBoxLayout(self)

        edit_title = QtGui.QLineEdit()
        edit_title.setFixedWidth(200)
        layout.addWidget(edit_title)

        layout.addStretch()


class EditorScreen(QtGui.QWidget):
    def __init__(self, client):
        super().__init__()

        self.client = client

        self.toolbar = QtGui.QToolBar()
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        action_new = QtGui.QAction(t.load_ui_icon('button_empty.png'), 'Create new scenario', self)
        action_new.triggered.connect(self.show_new_scenario_dialog)
        self.toolbar.addAction(action_new)

        spacer = QtGui.QWidget(self.toolbar)
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        action_help = QtGui.QAction(t.load_ui_icon('button_empty.png'), 'Show help', self)
        action_help.triggered.connect(client.show_help_browser) # TODO with partial make reference to specific page
        self.toolbar.addAction(action_help)

        action_quit = QtGui.QAction(t.load_ui_icon('button_empty.png'), 'Exit to main menu', self)
        action_quit.triggered.connect(client.show_start_screen)
        self.toolbar.addAction(action_quit)

        self.mini_map = MiniMap()

        self.info_box = InfoBox()

        self.map = Map()

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.toolbar, 0, 0, 1, 2)
        layout.addWidget(self.mini_map, 1, 0)
        layout.addWidget(self.info_box, 2, 0)
        layout.addWidget(self.map, 1, 1, 2, 1)
        layout.setRowStretch(2, 1) # the info box will take all vertical space left
        layout.setColumnStretch(1, 1) # the map will take all horizontal space left

    def show_new_scenario_dialog(self):
        new_scenario_widget = NewScenarioDialogWidget()
        dialog = g.Dialog(self.client.main_window, title='New Scenario', delete_on_close=True, modal=True)
        # TODO close callback
        dialog.set_content(new_scenario_widget)
        dialog.setFixedSize(QtCore.QSize(600, 400))
        dialog.show()