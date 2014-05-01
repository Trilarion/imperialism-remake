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
from client import audio
from gui import browser, graphics

def show_notification(text):
    graphics.show_notification(main_window, text)

def start():
    app = QtGui.QApplication([])

    main_window = QtGui.QWidget(f=QtCore.Qt.FramelessWindowHint)
    main_window.showFullScreen()
    main_window.show()
    size = main_window.size()

    #child = QtGui.QWidget(main_window)
    #child.setAttribute(QtCore.Qt.WA_StyledBackground)
    #child.setAutoFillBackground(True)
    #child.setStyleSheet('background-color:green;')
    #child.show()

    start_scene = QtGui.QGraphicsScene()

    start_screen = QtGui.QGraphicsView(start_scene, main_window)
    start_screen.setObjectName('start_screen')
    start_screen.setStyleSheet('#start_screen{background-color: black;border: 0px;}')
    start_screen.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    start_screen.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
    #start_screen.setContentsMargins(0, 0, 0, 0)
    #start_screen.setViewportMargins(0, 0, 0, 0)
    start_screen.setSceneRect(0, 0, size.width(), size.height())

    background = QtGui.QPixmap(constants.extend(constants.Graphics_UI_Folder, 'start.background.jpg'))
    background_item = QtGui.QGraphicsPixmapItem(background)
    background_item.setOffset(graphics.relative_layout_centered(size, background.size()))
    background_item.setZValue(1)
    start_scene.addItem(background_item)

    layout = QtGui.QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    layout.addWidget(start_screen)
    main_window.setLayout(layout)
    start_screen.show()

    home_url = QtCore.QUrl(constants.Manual_Index)
    help = browser.BrowserWindow(home_url, tools.load_icon, parent=main_window)
    help.show()


    playlist = audio.load_soundtrack_playlist()

    player = audio.Player()
    player.song_title.connect(show_notification)
    player.set_playlist(playlist)
    player.start()


    app.exec_()
