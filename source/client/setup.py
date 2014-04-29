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
import constants, tools
import gui.browser as browser

def start():
    app = QtGui.QApplication([])

    scene = QtGui.QGraphicsScene()

    background = QtGui.QPixmap(constants.extend(constants.Graphics_UI_Folder, 'start.background.jpg'))
    background_item = QtGui.QGraphicsPixmapItem(background)
    background_item.setZValue(1)
    scene.addItem(background_item)


    view = QtGui.QGraphicsView(scene)
    view.setStyleSheet('background-color: black;')
    view.resize(1200, 900)
    view.show()

    home_url = QtCore.QUrl(constants.Manual_Index)
    help = browser.BrowserWindow(home_url, tools.load_icon, parent=view)
    help.setStyleSheet('background-color: white;')
    help.show()

    app.exec_()
