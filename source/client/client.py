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
from server.editor import  EditorScreen

class StartScreen(QtGui.QGraphicsView):
    def __init__(self, size, client):
        super().__init__()

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)

        self.setProperty('background', 'texture')
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
            'editor': client.show_editor_screen,
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

        version_item = QtGui.QGraphicsSimpleTextItem(t.options[c.O_VERSION])
        brush_white = QtGui.QBrush(QtCore.Qt.white)
        version_item.setBrush(brush_white)
        version_item.setZValue(5)
        pos = g.Relative_Positioner().east(20).south(20)
        version_item.setPos(pos.calculate(size, version_item.boundingRect()))
        self.scene.addItem(version_item)

class GameLobbyWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()

        layout = QtGui.QVBoxLayout(self)
        toolbar = QtGui.QToolBar()
        toolbar.setFloatable(False)
        toolbar.setMovable(False)

        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        action_help = QtGui.QAction(t.load_ui_icon('icon.help.png'), 'Show help', self)
        toolbar.addAction(action_help)

        layout.addWidget(toolbar)
        layout.addStretch()

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
        tab_layout = QtGui.QVBoxLayout(tab)

        # mute checkbox
        checkbox = QtGui.QCheckBox('Mute background music')
        self.register_checkbox(checkbox, 'music.background.mute')
        tab_layout.addWidget(checkbox)

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.addTab(tab, 'Music')

    def register_checkbox(self, checkbox, option):
        checkbox.setChecked(t.options[option])
        self.checkboxes.append((checkbox, option))

    def close_request(self, widget):
        # check if something was changed
        options_modified = any([box.isChecked() is not t.options[option] for (box, option) in self.checkboxes])
        if options_modified:
            answer = QtGui.QMessageBox.question(widget, 'Preferences', 'Save modified preferences', QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
            if answer == QtGui.QMessageBox.Yes:
                # all checkboxes
                for (box, option) in self.checkboxes:
                    t.options[option, box.isChecked()]
                # what else do we need to do?
                if t.options[c.OM_BG_MUTE]:
                    t.player.stop()
                else:
                    t.player.start()
        return True

class MainWindow(QtGui.QWidget):
    def __init__(self, full_screen_mode):
        super().__init__()
        if full_screen_mode:
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
            self.showFullScreen()
        else:
            self.resize(1024, 768)
            self.show()
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
        self.main_window = MainWindow(t.options[c.OG_FULLSCREEN])
        self.main_window.setWindowIcon(t.load_ui_icon('icon.ico'))
        self.main_window.setWindowTitle('Imperialism Remake')
        self.main_window.setStyleSheet('*[background="texture"] {background-image: url(data/artwork/graphics/ui/background_texture.png)}')

        self.help_browser_widget = BrowserWidget(QtCore.QUrl(c.Manual_Index), t.load_ui_icon)
        self.help_dialog = g.Dialog(self.main_window, title='Help')
        self.help_dialog.set_content(self.help_browser_widget)
        self.help_dialog.setFixedSize(QtCore.QSize(800, 600))

    def show_notification(self, text):
        # TODO queue in case more than one comes
        g.show_notification(self.main_window, text, positioner=g.Relative_Positioner().centerH().south(20))

    def show_help_browser(self, url=None):
        if url:
            self.help_browser_widget.displayPage(url)
        self.help_dialog.show()

    def show_start_screen(self):
        widget = StartScreen(self.main_window.size(), self)
        self.main_window.change_content_widget(widget)

    def show_game_lobby(self):
        lobby_widget = GameLobbyWidget()
        dialog = g.Dialog(self.main_window, title='Game Lobby', delete_on_close=True, modal=True)
        dialog.set_content(lobby_widget)
        dialog.setFixedSize(QtCore.QSize(800, 600))
        dialog.show()

    def show_editor_screen(self):
        widget = EditorScreen(self)
        self.main_window.change_content_widget(widget)

    def show_options(self):
        options_widget = OptionsContentWidget()
        dialog = g.Dialog(self.main_window, title='Preferences', delete_on_close=True, modal=True, close_callback=options_widget.close_request)
        dialog.set_content(options_widget)
        dialog.setFixedSize(QtCore.QSize(800, 600))
        dialog.show()

    def quit(self):
        self.main_window.close()

def start():

    app = QtGui.QApplication([])


    # TODO multiple screen support

    # test for desktop availability
    desktop = app.desktop()
    rect = desktop.screenGeometry()
    if rect.width() < c.Screen_Min_Size[0] or rect.height() < c.Screen_Min_Size[1]:
        QtGui.QMessageBox.warning(None, 'Warning', 'Actual screen size below minimal screen size {}.'.format(c.Screen_Min_Size))
        return

    # configure if never configured before
    if not t.option[c.OG_CONFIGURED]:
        t.options[c.OG_MW_GEOMETRY] = desktop.availableGeometry()
        t.options[c.OG_MAXIMIZED] = True


    client = Client()
    client.show_start_screen()

    # t.player = audio.Player()
    # t.player.song_title.connect(lambda title: client.show_notification('Playing {}'.format(title)))
    # t.player.set_playlist(audio.load_soundtrack_playlist())
    # if not t.options['music.background.mute']:
    #     t.player.start()

    t.log_info('client initialized, start Qt app execution')
    app.exec_()