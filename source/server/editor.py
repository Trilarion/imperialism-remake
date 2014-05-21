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
import gui.graphics as g

class EditorScreen(g.Screen):
    def __init__(self):
        super().__init__()
        self.widget = QtGui.QWidget()

        self.toolbar = QtGui.QToolBar()
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        action_quit = QtGui.QAction(self.widget)
        action_quit.triggered.connect(self.quit.emit)
        self.toolbar.addAction(action_quit)

        spacer = QtGui.QWidget(self.toolbar)
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        action_help = QtGui.QAction(self.widget)
        self.toolbar.addAction(action_help)

        self.mini_map = QtGui.QLabel()
        self.mini_map.setStyleSheet('background-color:blue;')
        self.mini_map.resize(300, 200)

        self.info_box = QtGui.QLabel()
        self.info_box.setStyleSheet('background-color:green;')

        self.map = QtGui.QLabel()
        self.map.setStyleSheet('background-color:red;')

        layout = QtGui.QGridLayout()
        layout.addWidget(self.toolbar, 0, 0, 1, 2)
        layout.addWidget(self.mini_map, 1, 0)
        layout.addWidget(self.info_box, 1, 1)
        layout.addWidget(self.map, 1, 1, 2, 1)
        #layout.setRowStretch(2, 1) # the info box will take all vertical space left
        #layout.setColumnStretch(1, 1) # the map will take all horizontal space left
        self.widget.setLayout(layout)

    def screen_widget(self):
        return self.widget

app = QtGui.QApplication([])

s = EditorScreen()
s.screen_widget().resize(600, 500)
s.screen_widget().show()
s.quit.connect(app.quit)


app.exec_()