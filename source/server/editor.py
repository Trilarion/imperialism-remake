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
import lib.graphics as g

class MiniMap(QtCore.QObject):

    def __init__(self):
        super().__init__()

        self.scene = QtGui.QGraphicsScene()
        self.widget = QtGui.QGraphicsView(self.scene)
        self.widget.setObjectName('mini_map')
        self.widget.setStyleSheet('#mini_map{background-color: black;border: 0px;}')
        self.widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        size = QtCore.QSize(300, 300)
        self.widget.setSceneRect(0, 0, size.width(), size.height())
        self.widget.setMinimumSize(size)

class Map(QtCore.QObject):

    def __init__(self):
        super().__init__()

        self.scene = QtGui.QGraphicsScene()
        self.widget = QtGui.QGraphicsView(self.scene)
        self.widget.setObjectName('map')
        self.widget.setStyleSheet('#map{background-color: black;border: 0px;}')
        self.widget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

class InfoBox(QtCore.QObject):

    def __init__(self):
        super().__init__()

        self.widget = QtGui.QLabel()
        self.widget.setObjectName('info_box')
        self.widget.setStyleSheet('#info_box{background-color: black;}')

class NewScenarioDialog(g.Dialog):

    def __init__(self, parent):
        super().__init__(parent, 'New Scenario Dialog')

        self.content = QtGui.QWidget()

        layout = QtGui.QVBoxLayout()

        edit_title = QtGui.QLineEdit()
        edit_title.setFixedWidth(200)
        layout.addWidget(edit_title)

        self.content.setLayout(layout)
        self.set_content_widget(self.content)


class EditorScreen():
    def __init__(self):
        super().__init__()
        self.widget = QtGui.QWidget()

        self.toolbar = QtGui.QToolBar()
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        action_new = QtGui.QAction(self.widget)
        action_new.triggered.connect(self.show_new_scenario_dialog)
        self.toolbar.addAction(action_new)

        spacer = QtGui.QWidget(self.toolbar)
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        action_help = QtGui.QAction(self.widget)
        self.toolbar.addAction(action_help)

        action_quit = QtGui.QAction(self.widget)
        action_quit.triggered.connect(self.quit.emit)
        self.toolbar.addAction(action_quit)

        self.mini_map = MiniMap()

        self.info_box = InfoBox()

        self.map = Map()

        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar, 0, 0, 1, 2)
        layout.addWidget(self.mini_map.widget, 1, 0)
        layout.addWidget(self.info_box.widget, 2, 0)
        layout.addWidget(self.map.widget, 1, 1, 2, 1)
        layout.setRowStretch(2, 1) # the info box will take all vertical space left
        layout.setColumnStretch(1, 1) # the map will take all horizontal space left
        self.widget.setLayout(layout)

    def screen_widget(self):
        return self.widget

    def show_new_scenario_dialog(self):
        dialog = NewScenarioDialog(self.widget)
        dialog.show()