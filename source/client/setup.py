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

# TODO queue notifications

import json
from PySide import QtCore, QtGui
import constants as c, tools as t, lib.graphics as g
import client.audio as audio
from lib.browser import BrowserWidget

class StartScreen(QtGui.QGraphicsView):
    def __init__(self, size, client):
        super().__init__()

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)

        self.setObjectName('start_screen')
        self.setStyleSheet('#start_screen{background-color: black;border: 0px;}')
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSceneRect(0, 0, size.width(), size.height())

        background = QtGui.QPixmap(c.extend(c.Graphics_UI_Folder, 'start.background.jpg'))
        background_item = QtGui.QGraphicsPixmapItem(background)
        pos = g.Relative_Positioner().centerH().centerV()
        background_item.setOffset(pos.calculate(size, background.size()))
        background_item.setZValue(1)
        self.scene.addItem(background_item)

        actions = {
            'exit': client.quit,
            'help': client.show_help_browser,
            'lobby': client.show_game_lobby,
            'editor': client.quit,
            'options': client.show_options
        }

        map_file = c.extend(c.Graphics_UI_Folder, 'start.overlay.info')
        with open(map_file, 'r') as f:
            map = json.load(f)

        if actions.keys() != map.keys():
            raise RuntimeError('Start screen hot map info file ({}) corrupt.'.format(map_file))

        for k, v in map.items():
            # add action from our predefined action dictionary
            pixmap = QtGui.QPixmap(c.extend(c.Graphics_UI_Folder, v['overlay']))
            pixmap_item = g.ExtendedGraphicsPixmapItem(pixmap)
            pixmap_item.setZValue(3)
            self.scene.addItem(pixmap_item)
            v['item'] = pixmap_item

            fade_animation = g.FadeAnimation(pixmap_item, 300)
            pixmap_item.entered.connect(fade_animation.fade_in)
            pixmap_item.left.connect(fade_animation.fade_out)
            pixmap_item.clicked.connect(actions[k])
            offset = v['offset']
            pixmap_item.setOffset(background_item.offset() + QtCore.QPointF(offset[0], offset[1]))

            v['animation'] = fade_animation

            frame_path = QtGui.QPainterPath()
            frame_path.addRect(pixmap_item.boundingRect())
            brush = QtGui.QBrush(QtGui.QColor(255,255,255, 64))
            # brush = QtGui.QBrush(QtGui.QColor(255,255,255, 128), bs=QtCore.Qt.Dense3Pattern)
            pen = QtGui.QPen(brush, 6, j=QtCore.Qt.BevelJoin)
            frame_item = self.scene.addPath(frame_path, pen)
            frame_item.setZValue(4)
        self.map = map

        version_item = QtGui.QGraphicsSimpleTextItem(t.options.get('general.version'))
        brush_white = QtGui.QBrush(QtCore.Qt.white)
        version_item.setBrush(brush_white)
        version_item.setZValue(5)
        pos = g.Relative_Positioner().east(20).south(20)
        version_item.setPos(pos.calculate(size, version_item.boundingRect()))
        self.scene.addItem(version_item)

class OptionsContentWidget(QtGui.QTabWidget):

    def __init__(self):
        super().__init__()

        # empty lists
        self.checkboxes = []

        # add tabs
        self.add_tab_general()
        self.add_tab_music()

    def add_tab_general(self):
        tab = QtGui.QWidget()
        tab_layout = QtGui.QVBoxLayout(tab)

        # Graphics box
        box = QtGui.QGroupBox('Graphics')
        checkbox = QtGui.QCheckBox('Full screen mode')
        self.register_checkbox(checkbox, 'graphics.full_screen_mode')
        layout = QtGui.QVBoxLayout(box)
        layout.addWidget(checkbox)
        tab_layout.addWidget(box)

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.addTab(tab, 'General')

    def add_tab_music(self):
        tab = QtGui.QWidget()
        layout = QtGui.QVBoxLayout(tab)

        # add tab
        self.addTab(tab, 'Music')

    def register_checkbox(self, checkbox, option):
        checkbox.setChecked(t.options.get(option))
        self.checkboxes.append((checkbox, option))

    def close_request(self, widget):
        return True

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super().__init__(f=QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.content = None

    def change_content_widget(self, widget):
        if self.content:
            self.layout.removeWidget(self.content)
            del(self.content)
        self.content = widget
        self.layout.addWidget(widget)

class Client():
    def __init__(self):
        self.main_window = MainWindow()
        # set icon

        content_widget = BrowserWidget(QtCore.QUrl(c.Manual_Index), t.load_ui_icon)
        self.help_dialog = g.Dialog(self.main_window, title='Help', size=QtCore.QSize(800, 600), content_widget=content_widget)

    def show_notification(self, text):
        g.show_notification(self.main_window, 'Playing {}'.format(text), positioner=g.Relative_Positioner().centerH().south(50))

    def show_help_browser(self, url=None):
        if url:
            pass
            # c.help_browser.displayPage(url)
        self.help_dialog.show()

    def show_start_screen(self):
        widget = StartScreen(self.main_window.size(), self)
        self.main_window.change_content_widget(widget)

    def show_game_lobby(self):
        pass

    def show_options(self):
        content_widget = OptionsContentWidget()
        dialog_window = g.Dialog(self.main_window, title='Preferences', size=QtCore.QSize(800, 600), content_widget=content_widget, close_callback=content_widget.close_request)
        print(len(self.main_window.findChildren(QtGui.QWidget)))
        print(dialog_window.testAttribute(QtCore.Qt.WA_DeleteOnClose))
        dialog_window.show()

    def quit(self):
        self.main_window.close()

def start():
    app = QtGui.QApplication([])

    client = Client()
    client.show_start_screen()

    playlist = audio.load_soundtrack_playlist()

    player = audio.Player()
    player.song_title.connect(client.show_notification)
    player.set_playlist(playlist)
    player.start()

    t.log_info('client initialized, start Qt app execution')
    app.exec_()
