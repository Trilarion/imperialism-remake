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

"""
    GUI and internal working of the scenario editor. This is also partly of the client but since the client should not
    know anything about the scenario, we put it in the server module.
"""

import os, math

from PySide import QtCore, QtGui

import constants as c
import tools as t
import lib.graphics as g
import client.graphics as cg
from server.scenario import Scenario

class EditorScenario(Scenario):
    """

    """

    everything_changed = QtCore.Signal()

    def load(self, file_name):
        super().load(file_name)
        self.everything_changed.emit()


class EditorMiniMap(QtGui.QWidget):
    """
        Small overview map
    """

    Fixed_Width = 300

    focus_moved = QtCore.Signal(float, float)

    def __init__(self, scenario):
        super().__init__()
        self.setObjectName('minimap')

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.scene = QtGui.QGraphicsScene()

        self.tracker = QtGui.QGraphicsRectItem()
        self.tracker.setCursor(QtCore.Qt.PointingHandCursor)
        self.tracker.setZValue(1000)
        self.tracker.hide()
        self.scene.addItem(self.tracker)

        self.tracker_bounds = None

        self.view = QtGui.QGraphicsView(self.scene)
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        layout.addWidget(self.view)

        self.view.setFixedWidth(self.Fixed_Width)
        self.view.setFixedHeight(math.floor(0.6 * self.Fixed_Width))

        self.toolbar = QtGui.QToolBar()
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(QtCore.QSize(20, 20))

        action_group = QtGui.QActionGroup(self.toolbar)

        action_political = QtGui.QAction(t.load_ui_icon('icon.mini.political.png'), 'Show political view', action_group)
        action_political.triggered.connect(self.switch_to_political)
        action_political.setCheckable(True)
        self.toolbar.addAction(action_political)

        action_geographical = QtGui.QAction(t.load_ui_icon('icon.mini.geographical.png'), 'Show geographical view', action_group)
        action_geographical.triggered.connect(self.switch_to_geographical)
        action_geographical.setCheckable(True)
        self.toolbar.addAction(action_geographical)

        l = QtGui.QHBoxLayout()
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(self.toolbar)
        l.addStretch()

        # layout.addWidget(self.toolbar)
        layout.addLayout(l)

        self.scenario = scenario
        self.map_mode = 'political'
        self.removable_items = []

    def redraw_map(self):
        # we do not draw anything if the scenario is not valid
        if not self.scenario.valid:
            return
        # adjust view height
        map_size = self.scenario['map-size']
        scale = self.Fixed_Width / map_size[0]
        height = math.floor(self.Fixed_Width / map_size[0] * map_size[1])
        self.view.setFixedHeight(height)
        self.view.setSceneRect(0, 0, self.Fixed_Width, height)

        # remove everything except tracker from the scene
        for item in self.removable_items:
            self.scene.removeItem(item)
        self.removable_items = []

        if self.map_mode is 'political':

            # fill the ground layer with a neutral color
            item = self.scene.addRect(0, 0, self.Fixed_Width, height)
            item.setBrush(QtCore.Qt.lightGray)
            item.setPen(g.TRANSPARENT_PEN)
            item.setZValue(0)
            self.removable_items.extend([item])

            # draw the nation borders and content (non-smooth)

            # for all nations
            for nation in self.scenario.all_nations():
                # get nation color
                color = self.scenario.get_nation_property(nation, 'color')
                c = QtGui.QColor()
                c.setNamedColor(color)
                # get all provinces
                provinces = self.scenario.get_provinces_of_nation(nation)
                tiles = []
                # get all tiles
                for province in provinces:
                    tiles.extend(self.scenario.get_province_property(province, 'tiles'))
                # get rectangular path for each tile
                path = QtGui.QPainterPath()
                for map_position in tiles:
                    sx, sy = self.scenario.scene_position(map_position[0], map_position[1])
                    path.addRect(sx * scale, sy * scale, scale, scale)
                # simply (creates outline)
                path = path.simplified()
                # create a brush from the color
                brush = QtGui.QBrush(c)
                item = self.scene.addPath(path, brush=brush) # will use the default pen for outline
                item.setZValue(1)
                self.removable_items.extend([item])

        elif self.map_mode is 'geographical':

            # fill the background with sea (blue)
            item = self.scene.addRect(0, 0, self.Fixed_Width, height)
            item.setBrush(QtCore.Qt.blue)
            item.setPen(g.TRANSPARENT_PEN)
            item.setZValue(0)
            self.removable_items.extend([item])

            # six terrains left, plains, hills, mountains, tundra, swamp, desert

            # go through each position
            paths = {}
            for t in range(1, 7):
                paths[t] = QtGui.QPainterPath()
            for column in range(0, map_size[0]):
                for row in range(0, map_size[1]):
                    t = self.scenario.terrain_at(column, row)
                    if t != 0:
                        # not for sea
                        sx, sy = self.scenario.scene_position(column, row)
                        paths[t].addRect(sx * scale, sy * scale, scale, scale)
            colors = {
                1: QtCore.Qt.green,
                2: QtCore.Qt.darkGreen,
                3: QtCore.Qt.darkGray,
                4: QtCore.Qt.white,
                5: QtCore.Qt.darkYellow,
                6: QtCore.Qt.yellow
            }
            for t in paths:
                path = paths[t]
                path = path.simplified()
                brush = QtGui.QBrush(colors[t])
                item = self.scene.addPath(path, brush=brush, pen=g.TRANSPARENT_PEN)
                item.setZValue(1)
                self.removable_items.extend([item])

    def switch_to_political(self):
        if self.map_mode is not 'political':
            self.map_mode = 'political'
            self.redraw_map()

    def switch_to_geographical(self):
        if self.map_mode is not 'geographical':
            self.map_mode = 'geographical'
            self.redraw_map()

    def mousePressEvent(self, event):
        super().mouseMoveEvent(event)

        # if the tracker is not yet visible, don't do anything
        if not self.tracker.isVisible():
            return

        # get normalized coordinates and subtract half width and length
        x = event.x() / self.view.width() - self.tracker_bounds.width() / 2
        y = event.y() / self.view.height() - self.tracker_bounds.height() / 2
        # apply min/max to keep inside the map area
        x = min(max(x, 0), 1 - self.tracker_bounds.width())
        y = min(max(y, 0), 1 - self.tracker_bounds.height())
        # check if they are different
        if x != self.tracker_bounds.x() or y != self.tracker_bounds.y():
            # they are different, update stored bounds, tracker and emit signal
            self.tracker_bounds.moveTo(x, y)
            self.tracker.setPos(x * self.view.width(), y * self.view.height())
            self.focus_moved.emit(x, y)

    def reset_tracker(self, bounds):
        """
            The main map tells us how large its view is (in terms of the game map) and where it is currently.
        """
        self.tracker_bounds = bounds
        self.tracker.setRect(bounds.x() * self.view.width(), bounds.y() * self.view.height(), bounds.width() * \
                             self.view.width(), bounds.height() * self.view.height())
        self.tracker.show()


class EditorMainMap(QtGui.QGraphicsView):
    """
        The big map holding the game map and everything.
    """

    tile_at_focus_changed = QtCore.Signal(object)

    def __init__(self, scenario):
        super().__init__()

        self.scene = QtGui.QGraphicsScene()
        self.setScene(self.scene)
        self.setObjectName('map')
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtGui.QGraphicsView.NoAnchor)
        self.setMouseTracking(True)
        self.current_map_position = (-1, -1)
        self.tile_size = 80
        self.scenario = scenario

    def redraw_map(self):
        """
            When a scenario is loaded anew we need to draw the whole map new.
        """
        self.scene.clear()

        map_size = self.scenario['map-size']

        width = (map_size[0] + 0.5) * self.tile_size
        height = map_size[1] * self.tile_size
        self.scene.setSceneRect(0, 0, width, height)

        # TODO should load only once and cache (universal cache)
        # load all textures
        textures = {}
        textures[0] = QtGui.QBrush(QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'texture_ocean.jpg')))
        textures[1] = QtGui.QBrush(QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'texture_plain.png')))
        textures[2] = QtGui.QBrush(QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'texture_plain.png')))
        textures[3] = QtGui.QBrush(QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'texture_plain.png')))
        textures[4] = QtGui.QBrush(QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'texture_tundra.png')))
        textures[5] = QtGui.QBrush(QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'texture_swamp.png')))
        textures[6] = QtGui.QBrush(QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'texture_desert.png')))

        # fill the ground layer with ocean
        item = self.scene.addRect(0, 0, width, height, brush=textures[0], pen=g.TRANSPARENT_PEN)
        item.setZValue(0)

        # fill plains, hills, mountains, tundra, swamp, desert with texture

        # go through each position
        paths = {}
        for t in range(1, 7):
            paths[t] = QtGui.QPainterPath()
        for column in range(0, map_size[0]):
            for row in range(0, map_size[1]):
                t = self.scenario.terrain_at(column, row)
                if t != 0:
                    # not for sea
                    sx, sy = self.scenario.scene_position(column, row)
                    paths[t].addRect(sx * self.tile_size, sy * self.tile_size, self.tile_size, self.tile_size)
        for t in paths:
            path = paths[t]
            path = path.simplified()
            item = self.scene.addPath(path, brush=textures[t], pen=g.TRANSPARENT_PEN)
            item.setZValue(1)

        # fill the half tiles which are not part of the map
        brush = QtGui.QBrush(QtCore.Qt.darkGray)
        for row in range(0, map_size[1]):
            if row % 2 == 0:
                item = self.scene.addRect(map_size[0] * self.tile_size, row * self.tile_size, self.tile_size / 2, self.tile_size, pen=g.TRANSPARENT_PEN)
            else:
                item = self.scene.addRect(0, row * self.tile_size, self.tile_size / 2, self.tile_size, pen=g.TRANSPARENT_PEN)
            item.setBrush(brush)
            item.setZValue(1)

        # draw province and nation borders
        # TODO the whole border drawing is a crude approximiation, implement it the right way
        province_border_pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.black))
        province_border_pen.setWidth(2)
        nation_border_pen = QtGui.QPen()
        nation_border_pen.setWidth(4)
        for nation in self.scenario.all_nations():
            # get nation color
            color = self.scenario.get_nation_property(nation, 'color')
            nation_color = QtGui.QColor()
            nation_color.setNamedColor(color)
            # get all provinces
            provinces = self.scenario.get_provinces_of_nation(nation)
            nation_path = QtGui.QPainterPath()
            # get all tiles
            for province in provinces:
                province_path = QtGui.QPainterPath()
                tiles = self.scenario.get_province_property(province, 'tiles')
                for column, row in tiles:
                    sx, sy = self.scenario.scene_position(column, row)
                    province_path.addRect(sx * self.tile_size, sy * self.tile_size, self.tile_size, self.tile_size)
                province_path = province_path.simplified()
                item = self.scene.addPath(province_path, pen=province_border_pen)
                item.setZValue(4)
                nation_path.addPath(province_path)
            nation_path = nation_path.simplified()
            nation_border_pen.setColor(nation_color)
            item = self.scene.addPath(nation_path, pen=nation_border_pen)
            item.setZValue(5)

        # draw towns and names
        city_pixmap = QtGui.QPixmap(c.extend(c.Graphics_Map_Folder, 'city.png'))
        for nation in self.scenario.all_nations():
            # get all provinces of this nation
            provinces = self.scenario.get_provinces_of_nation(nation)
            for province in provinces:
                column, row = self.scenario.get_province_property(province, 'town_location')
                sx, sy = self.scenario.scene_position(column, row)
                # center city image on center of tile
                x = (sx + 0.5) * self.tile_size - city_pixmap.width() / 2
                y = (sy + 0.5) * self.tile_size - city_pixmap.height() / 2
                item = self.scene.addPixmap(city_pixmap)
                item.setOffset(x, y)
                item.setZValue(6)
                # display province name below
                province_name = self.scenario.get_province_property(province, 'name')
                item = self.scene.addSimpleText(province_name)
                item.setPen(g.TRANSPARENT_PEN)
                item.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
                x = (sx + 0.5) * self.tile_size - item.boundingRect().width() / 2
                y = (sy + 1) * self.tile_size - item.boundingRect().height()
                item.setPos(x, y)
                item.setZValue(6)
                # display rounded rectangle below province name
                bx = 8
                by = 4
                background = QtCore.QRectF(x - bx, y - by, item.boundingRect().width() + 2 * bx, item.boundingRect().height() + 2 * by)
                path = QtGui.QPainterPath()
                path.addRoundRect(background, 50, 50)
                item = self.scene.addPath(path, pen=g.TRANSPARENT_PEN, brush=QtGui.QBrush(QtGui.QColor(128, 128, 255, 64)))
                item.setZValue(5)

        # draw the grid and the coordinates
        for column in range(0, map_size[0]):
            for row in range(0, map_size[1]):
                sx, sy = self.scenario.scene_position(column, row)
                #item = self.scene.addRect(sx * self.tile_size, sy * self.tile_size,  self.tile_size,  self.tile_size)
                #item.setZValue(1000)
                text = '({},{})'.format(column, row)
                item = QtGui.QGraphicsSimpleTextItem(text)
                item.setBrush(QtGui.QBrush(QtCore.Qt.black))
                item.setPos((sx + 0.5) * self.tile_size - item.boundingRect().width() / 2, sy * self.tile_size)
                item.setZValue(1001)
                self.scene.addItem(item)

    def get_bounds(self):
        # total rectangle of the scene (0, 0, width, height)
        s = self.scene.sceneRect()
        # visible rectangle of the view
        v = self.mapToScene(self.rect()).boundingRect()
        return QtCore.QRectF(v.x() / s.width(), v.y() / s.height(), v.width() / s.width(), v.height() / s.height())

    def set_position(self, x, y):
        # total rectangle of the scene (0, 0, width, height)
        s = self.scene.sceneRect()
        # visible rectangle of the view
        v = self.mapToScene(self.rect()).boundingRect()
        # adjust x, y to scene coordinates and find center
        x = x * s.width() + v.width() / 2
        y = y * s.height() + v.height() / 2
        # center on it
        self.centerOn(x, y)

    def mouseMoveEvent(self, event):
        if self.scenario:
            # get mouse position in scene coordinates
            scene_position = self.mapToScene(event.pos()) / self.tile_size
            map_position = self.scenario.map_position(scene_position.x(), scene_position.y())
            if map_position != self.current_map_position:
                self.current_map_position = map_position
                self.tile_at_focus_changed.emit(self.current_map_position)
        super().mouseMoveEvent(event)


class InfoBox(QtGui.QLabel):
    """
        Info box on the right side of the editor.
    """

    def __init__(self):
        super().__init__()
        self.setObjectName('infobox')
        self.setText('Info box')

    def new_map_position(self, map_position):
        self.setText('New position {}'.format(map_position))


class NewScenarioDialogWidget(QtGui.QWidget):
    """
        New scenario dialog.
    """
    create_scenario = QtCore.Signal(dict)

    def __init__(self):
        super().__init__()

        self.items = {}

        widget_layout = QtGui.QVBoxLayout(self)

        # title box
        box = QtGui.QGroupBox('Title')
        layout = QtGui.QVBoxLayout(box)
        edit = QtGui.QLineEdit()
        edit.setFixedWidth(300)
        self.items['title'] = edit
        layout.addWidget(edit)
        widget_layout.addWidget(box)

        # map size
        box = QtGui.QGroupBox('Map size')
        layout = QtGui.QHBoxLayout(box)

        layout.addWidget(QtGui.QLabel('Width'))
        edit = QtGui.QLineEdit()
        edit.setFixedWidth(50)
        edit.setPlaceholderText('100')
        edit.setValidator(QtGui.QIntValidator(0, 100))
        self.items['width'] = edit
        layout.addWidget(edit)

        layout.addWidget(QtGui.QLabel('Height'))
        edit = QtGui.QLineEdit()
        edit.setFixedWidth(50)
        edit.setPlaceholderText('100')
        edit.setValidator(QtGui.QIntValidator(0, 100))
        self.items['heigh'] = edit
        layout.addWidget(edit)
        layout.addStretch()

        widget_layout.addWidget(box)

        # vertical stretch
        widget_layout.addStretch()

        # add the button
        layout = QtGui.QHBoxLayout()
        toolbar = QtGui.QToolBar()
        action_create = QtGui.QAction(t.load_ui_icon('icon.confirm.png'), 'Create new scenario', toolbar)
        action_create.triggered.connect(self.create_scenario_clicked)
        toolbar.addAction(action_create)
        layout.addStretch()
        layout.addWidget(toolbar)
        widget_layout.addLayout(layout)

    def create_scenario_clicked(self):
        """
            Callback if indeed yes is clicked.
        """
        self.items['title'] = self.items['title'].text()
        # we close the parent window and emit the appropriate signal
        self.parent().close()
        self.create_scenario.emit(self.items)

class EditorScreen(QtGui.QWidget):
    """
        The screen the contains the whole scenario editor. Is copied into the application main window if the user
        clicks on the editor pixmap in the client main screen.
    """

    def __init__(self, client):
        """
            Create and setup all the elements.
        """
        super().__init__()

        self.client = client
        self.scenario = EditorScenario()
        self.scenario.everything_changed.connect(self.scenario_change)

        self.toolbar = QtGui.QToolBar()
        self.toolbar.setFloatable(False)
        self.toolbar.setMovable(False)

        action_new = QtGui.QAction(t.load_ui_icon('icon.scenario.new.png'), 'Create new scenario', self)
        action_new.triggered.connect(self.show_new_scenario_dialog)
        self.toolbar.addAction(action_new)

        action_load = QtGui.QAction(t.load_ui_icon('icon.scenario.load.png'), 'Load scenario', self)
        action_load.triggered.connect(self.load_scenario_dialog)
        self.toolbar.addAction(action_load)

        action_save = QtGui.QAction(t.load_ui_icon('icon.scenario.save.png'), 'Save scenario', self)
        action_save.triggered.connect(self.save_scenario_dialog)
        self.toolbar.addAction(action_save)

        self.toolbar.addSeparator()
        action_nations = QtGui.QAction(t.load_ui_icon('icon.editor.nations.png'), 'Modify Nations', self)
        action_nations.triggered.connect(self.show_nations_dialog)
        self.toolbar.addAction(action_nations)

        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)

        clock = g.ClockLabel()
        self.toolbar.addWidget(clock)

        action_help = QtGui.QAction(t.load_ui_icon('icon.help.png'), 'Show help', self)
        action_help.triggered.connect(client.show_help_browser)  # TODO with partial make reference to specific page
        self.toolbar.addAction(action_help)

        action_quit = QtGui.QAction(t.load_ui_icon('icon.back.startscreen.png'), 'Exit to main menu', self)
        action_quit.triggered.connect(client.switch_to_start_screen)
        # TODO ask if something is changed we should save.. (you might loose progress)
        self.toolbar.addAction(action_quit)

        # info box
        self.info_box = InfoBox()

        # the main map
        self.map = EditorMainMap(self.scenario)
        self.map.tile_at_focus_changed.connect(self.info_box.new_map_position)

        # the mini map
        self.mini_map = EditorMiniMap(self.scenario)
        self.mini_map.focus_moved.connect(self.map.set_position)

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.toolbar, 0, 0, 1, 2)
        layout.addWidget(self.mini_map, 1, 0)
        layout.addWidget(self.info_box, 2, 0)
        layout.addWidget(self.map, 1, 1, 2, 1)
        layout.setRowStretch(2, 1)  # the info box will take all vertical space left
        layout.setColumnStretch(1, 1)  # the map will take all horizontal space left

    def show_new_scenario_dialog(self):
        """
            Show the dialog for creation of a new scenario dialog.
        """
        new_scenario_widget = NewScenarioDialogWidget()
        dialog = cg.GameDialog(self.client.main_window, new_scenario_widget, title='New Scenario', delete_on_close=True,
                               help_callback=self.client.show_help_browser)
        # TODO close callback
        dialog.setFixedSize(QtCore.QSize(500, 400))
        dialog.show()

    def load_scenario_dialog(self):
        """
            Show the load a scenario dialog. Then loads it if the user has selected one.
        """
        file_name = \
            QtGui.QFileDialog.getOpenFileName(self, 'Load Scenario', c.Scenario_Folder, 'Scenario Files (*.scenario)')[0]
        if file_name:
            # TODO what if file name does not exist or is not a valid scenario file
            self.scenario.load(file_name)
            self.client.schedule_notification('Loaded scenario {}'.format(self.scenario['title']))

    def save_scenario_dialog(self):
        """
            Show the save a scenario dialog. Then saves it.
        """
        file_name = \
            QtGui.QFileDialog.getSaveFileName(self, 'Save Scenario', c.Scenario_Folder, 'Scenario Files (*.scenario)')[
                0]
        if file_name:
            self.scenario.save(file_name)
            path, name = os.path.split(file_name)
            self.client.schedule_notification('Saved to {}'.format(name))

    def scenario_change(self):
        """
            Whenever the scenario changes completely (new scenario, scenario loaded, ...)
        """
        self.map.redraw_map()
        self.mini_map.redraw_map()
        self.mini_map.reset_tracker(self.map.get_bounds())

    def show_nations_dialog(self):
        """
            Show the modify nations dialog.
        """
        pass