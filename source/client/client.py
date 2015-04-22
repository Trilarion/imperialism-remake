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

# TODO automatic placement of help dialog depending on if another dialog is open

from functools import partial

from PySide import QtGui, QtCore

import lib.graphics as g
import lib.utils as u
from lib.browser import BrowserWidget
import base.tools as t
import base.constants as c
import base.network as net
from base.constants import PropertyKeyNames as k, NationPropertyKeyNames as kn
from client.graphics import MiniMapNationItem
import client.graphics as cg
import client.audio as audio
from client.main_screen import GameMainScreen
from server.editor import EditorScreen
from server.monitor import ServerMonitorWidget

"""
    Starts the client and delivers most of the code reponsible for the main client screen and the diverse dialogs.
"""

network_client = net.NetworkClient()
network_client.set_socket()


class MapItem(QtCore.QObject):
    """
        Holds together a clickable QPixmapItem, a description text and a reference to a label that shows the text

        TODO use signals to show the text instead
    """
    description_change = QtCore.Signal(str)

    def __init__(self, parent, pixmap, label, description):
        super().__init__(parent)
        # store label and description
        self.label = label
        self.description = description

        # create clickable pixmap item and create fade animation
        self.item = g.ClickablePixmapItem(pixmap)
        self.fade = g.FadeAnimation(self.item)
        self.fade.set_duration(300)

        # wire to fade in/out
        self.item.entered.connect(self.fade.fadein)
        self.item.left.connect(self.fade.fadeout)

        # wire to show/hide connection
        self.item.entered.connect(self.show_description)
        self.item.left.connect(self.hide_description)

    def show_description(self):
        self.label.setText('<font color=#ffffff size=6>{}</font>'.format(self.description))

    def hide_description(self):
        self.label.setText('')


class StartScreen(QtGui.QWidget):
    """
        Creates the start screen

        TODO convert to simple method which does it, no need to be a class
    """

    frame_pen = QtGui.QPen(QtGui.QBrush(QtGui.QColor(255, 255, 255, 64)), 6, j=QtCore.Qt.BevelJoin)

    def __init__(self, client):
        super().__init__()

        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setProperty('background', 'texture')

        layout = g.RelativeLayout(self)

        start_image = QtGui.QPixmap(c.extend(c.Graphics_UI_Folder, 'start.background.jpg'))
        start_image_item = QtGui.QGraphicsPixmapItem(start_image)
        start_image_item.setZValue(1)

        scene = QtGui.QGraphicsScene(self)
        scene.addItem(start_image_item)

        view = QtGui.QGraphicsView(scene)
        view.resize(start_image.size())
        view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        view.setSceneRect(0, 0, start_image.width(), start_image.height())
        view.layout_constraint = g.RelativeLayoutConstraint().center_horizontal().center_vertical()
        layout.addWidget(view)

        subtitle = QtGui.QLabel('')
        subtitle.layout_constraint = g.RelativeLayoutConstraint((0.5, -0.5, 0),
                                                                (0.5, -0.5, start_image.height() / 2 + 20))
        layout.addWidget(subtitle)

        actions = {
            'exit': client.quit,
            'help': client.show_help_browser,
            'lobby': client.show_game_lobby_dialog,
            'editor': client.switch_to_editor_screen,
            'options': client.show_options_dialog
        }

        image_map_file = c.extend(c.Graphics_UI_Folder, 'start.overlay.info')
        image_map = u.read_as_yaml(image_map_file)

        # security check, they have to be the same
        if actions.keys() != image_map.keys():
            raise RuntimeError('Start screen hot map info file ({}) corrupt.'.format(image_map_file))

        for k, v in image_map.items():
            # add action from our predefined action dictionary
            pixmap = QtGui.QPixmap(c.extend(c.Graphics_UI_Folder, v['overlay']))
            mapitem = MapItem(view, pixmap, label=subtitle, description=v['label'])
            mapitem.item.setZValue(3)
            offset = v['offset']
            mapitem.item.setOffset(QtCore.QPointF(offset[0], offset[1]))
            mapitem.item.clicked.connect(actions[k])

            frame_path = QtGui.QPainterPath()
            frame_path.addRect(mapitem.item.boundingRect())
            frame_item = scene.addPath(frame_path, StartScreen.frame_pen)
            frame_item.setZValue(4)
            scene.addItem(mapitem.item)

        version_label = QtGui.QLabel('<font color=#ffffff>{}</font>'.format(t.get_option(c.O.VERSION)))
        version_label.layout_constraint = g.RelativeLayoutConstraint().east(20).south(20)
        layout.addWidget(version_label)


class GameLobbyWidget(QtGui.QWidget):
    """
        Content widget for the game lobby.
    """

    single_player_start = QtCore.Signal(str, str)

    def __init__(self):
        """
            Create toolbar and invoke pressing of first tab.
        """
        super().__init__()

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # create tool bar
        toolbar = QtGui.QToolBar()
        action_group = QtGui.QActionGroup(toolbar)

        toolbar.addAction(g.create_action(t.load_ui_icon('icon.lobby.single.new.png'), 'Start new single player scenario', action_group, toggle_connection=self.toggled_single_player_scenario_selection, checkable=True))
        toolbar.addAction(g.create_action(t.load_ui_icon('icon.lobby.single.load.png'), 'Continue saved single player scenario', action_group, toggle_connection=self.toggled_single_player_load_scenario, checkable=True))

        toolbar.addSeparator()

        toolbar.addAction(g.create_action(t.load_ui_icon('icon.lobby.network.png'), 'Show server lobby', action_group, toggle_connection=self.toggled_server_lobby, checkable=True))
        toolbar.addAction(g.create_action(t.load_ui_icon('icon.lobby.multiplayer-game.png'), 'Start or continue multiplayer scenario', action_group, toggle_connection=self.toggled_multiplayer_scenario_selection, checkable=True))

        layout.addWidget(toolbar)

        content = QtGui.QWidget()
        self.content_layout = QtGui.QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(content)

    def toggled_single_player_scenario_selection(self, checked):
        """
            Toolbar action switch to single player scenario selection.

            Because of the Action being part of an ActionGroup, this can only be called if before another action was executed.
        """

        if checked is True:
            # create new widget
            widget = SinglePlayerScenarioTitleSelection()
            widget.title_selected.connect(self.single_player_scenario_selection_preview, QtCore.Qt.QueuedConnection)

            # add to layout
            self.content_layout.addWidget(widget)
            self.content_layout.itemAt(0).setAlignment(QtCore.Qt.AlignCenter)

    def single_player_scenario_selection_preview(self, scenario_file):
        """
            Single player scenario selection, a scenario title was selected, show preview.
        """

        # remove SinglePlayerScenarioTitleSelection widget
        item = self.content_layout.takeAt(0)  # QLayoutItem we know it's only one
        widget = item.widget()  # widget from item
        widget.setParent(None)  # no parent

        # create new widget
        widget = SinglePlayerScenarioPreview(scenario_file)
        widget.nation_selected.connect(partial(self.single_player_start.emit, scenario_file))
        self.content_layout.addWidget(widget)

    def toggled_single_player_load_scenario(self, checked):
        """
            Toolbar action switch to single player load a scenario.
        """

        if checked is True:

            # noinspection PyCallByClass
            file_name = QtGui.QFileDialog.getOpenFileName(self, 'Continue Single Player Scenario', c.Scenario_Folder,
                                                          'Scenario Files (*.scenario)')[0]
            if file_name:
                # TODO check that it is a valid single player scenario in play
                pass

    def toggled_server_lobby(self, checked):
        """
            Toolbar action switch to server lobby.
        """
        if checked is True:
            pass

    def toggled_multiplayer_scenario_selection(self, checked):
        """
            Toolbar action switch to multiplayer scenario selection.
        """
        if checked is True:
            pass


class SinglePlayerScenarioPreview(QtGui.QWidget):
    """
        Displays the preview of a single player scenario in the game lobby.

        If a nation is selected the nation_selected signal is emitted with the nation name.
    """

    CH_PREVIEW = 'SP.scenario-selection.preview'

    nation_selected = QtCore.Signal(str)

    def __init__(self, scenario_file):
        """
            Given a scenario file name, get the preview from the server.
            TODO move the network communication outside this class.
        """
        super().__init__()

        # add a channel for us
        network_client.connect_to_channel(self.CH_PREVIEW, self.received_preview)

        # send a message and ask for preview
        network_client.send(c.CH_SCENARIO_PREVIEW, {'scenario': scenario_file, 'reply-to': self.CH_PREVIEW})

        self.selected_nation = None

    def received_preview(self, client, message):
        """
            Populates the widget after the network reply comes from the server with the preview.
        """
        # immediately close the channel, we do not want to get this message twice
        network_client.remove_channel(self.CH_PREVIEW)

        # fill the widget with useful stuff
        layout = QtGui.QGridLayout(self)

        # selection list for nations
        self.nations_list = QtGui.QListWidget()
        self.nations_list.setFixedWidth(200)
        self.nations_list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.nations_list.itemSelectionChanged.connect(self.nations_list_selection_changed)
        layout.addWidget(g.wrap_in_groupbox(self.nations_list, 'Nations'), 0, 0)

        # map view (no scroll bars)
        self.map_scene = QtGui.QGraphicsScene()
        self.map_view = g.FitSceneInViewGraphicsView(self.map_scene)
        self.map_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.map_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.map_view.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        layout.addWidget(g.wrap_in_groupbox(self.map_view, 'Map'), 0, 1)

        # scenario description
        self.description = QtGui.QTextEdit()
        self.description.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.description.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.description.setReadOnly(True)
        self.description.setFixedHeight(60)
        layout.addWidget(g.wrap_in_groupbox(self.description, 'Description'), 1, 0, 1, 2)  # goes over two columns

        # nation description
        self.nation_info = QtGui.QTextEdit()
        self.nation_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.nation_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.nation_info.setReadOnly(True)
        self.nation_info.setFixedHeight(100)
        layout.addWidget(g.wrap_in_groupbox(self.nation_info, 'Nation Info'), 2, 0, 1, 2)

        # stretching of the elements
        layout.setRowStretch(0, 1)  # nation list and map get all the available height
        layout.setColumnStretch(1, 1)  # map gets all the available width

        # add the start button
        toolbar = QtGui.QToolBar()
        toolbar.addAction(g.create_action(t.load_ui_icon('icon.confirm.png'), 'Start selected scenario', toolbar,
                                          trigger_connection=self.start_scenario_clicked))
        layout.addWidget(toolbar, 3, 0, 1, 2, alignment=QtCore.Qt.AlignRight)

        # set the content from the message
        self.description.setText(message[k.DESCRIPTION])

        nations = [[message['nations'][key]['name'], key] for key in message['nations']]
        nations = sorted(nations)  # by first element, which is the name
        nation_names, self.nation_ids = zip(*nations)
        self.nations_list.addItems(nation_names)

        # draw the map
        columns = message[k.MAP_COLUMNS]
        rows = message[k.MAP_ROWS]
        self.map_scene.setSceneRect(0, 0, columns, rows)

        # fill the ground layer with a neutral color
        item = self.map_scene.addRect(0, 0, columns, rows)
        item.setBrush(QtCore.Qt.lightGray)
        item.setPen(g.TRANSPARENT_PEN)
        item.setZValue(0)

        # text display
        self.map_name_item = self.map_scene.addSimpleText('')
        self.map_name_item.setPen(g.TRANSPARENT_PEN)
        self.map_name_item.setBrush(QtGui.QBrush(QtCore.Qt.darkRed))
        self.map_name_item.setZValue(3)
        self.map_name_item.setPos(0, 0)

        # for all nations
        for nation_id, nation in message['nations'].items():

            # get nation color
            color_string = nation['color']
            color = QtGui.QColor()
            color.setNamedColor(color_string)

            # get nation name
            nation_name = nation['name']

            # get nation outline
            path = QtGui.QPainterPath()
            # TODO traversing everything is quite slow go only once and add to paths
            for column in range(0, columns):
                for row in range(0, rows):
                    if nation_id == message['map'][column + row * columns]:
                        path.addRect(column, row, 1, 1)
            path = path.simplified()

            item = MiniMapNationItem(path, 1, 2)
            item.clicked.connect(partial(self.map_selected_nation, u.find_in_list(nation_names, nation_name)))
            item.entered.connect(partial(self.change_map_name, nation_name))
            item.left.connect(partial(self.change_map_name, ''))
            brush = QtGui.QBrush(color)
            item.setBrush(brush)

            self.map_scene.addItem(item)
            # item = self.map_scene.addPath(path, brush=brush) # will use the default pen for outline

        self.preview = message

    def change_map_name(self, nation_name, event):
        """
           Display of hoovered nation name.

            TODO not looking nice so far. Improve, display somewhere else (not in the scene).
        """
        self.map_name_item.setText(nation_name)

    def map_selected_nation(self, nation_row, event):
        """
            Clicked on a nation in the map. Just selects the corresponding row in the nation table.
        """
        self.nations_list.setCurrentRow(nation_row)

    def nations_list_selection_changed(self):
        """
            A nation was selected in the nations table, fill nation description and set it selected.
        """
        row = self.nations_list.currentRow()
        id = self.nation_ids[row]
        self.selected_nation = self.preview['nations'][id][kn.NAME]
        nation_description = self.preview['nations'][id][kn.DESCRIPTION]
        self.nation_info.setText(nation_description)

    def start_scenario_clicked(self):
        """
            Start scenario button is clicked. Only react if a nation is already selected.
        """
        if self.selected_nation is not None:
            self.nation_selected.emit(self.selected_nation)

    def stop(self):
        """
            Interruption. Clean up network channels and the like.
        """
        # network channel might still be open
        network_client.remove_channel(self.CH_PREVIEW, ignore_not_existing=True)


class SinglePlayerScenarioTitleSelection(QtGui.QGroupBox):
    """
        Displays a widget with all available scenario titles for starting new single player scenarios.

        If a title is selected, emits the title_selected signal.
    """

    title_selected = QtCore.Signal(str)  # make sure to only connect with QtCore.Qt.QueuedConnection to this signal

    CH_TITLES = 'SP.scenario-selection.titles'

    def __init__(self):
        """

        """
        super().__init__()
        self.setTitle('Select Scenario')
        QtGui.QVBoxLayout(self)  # just set a standard layout

        # add a channel for us
        network_client.connect_to_channel(self.CH_TITLES, self.received_titles)

        # send message and ask for scenario titles
        network_client.send(c.CH_CORE_SCENARIO_TITLES, {'reply-to': self.CH_TITLES})

    def received_titles(self, client, message):
        """
            Received all available scenario titles as a list together with the file names
            which act as unique identifiers. The list is sorted by title.
        """

        # immediately close the channel, we do not want to get this message twice
        network_client.remove_channel(self.CH_TITLES)

        # unpack message
        scenario_titles, self.scenario_files = zip(*message['scenarios'])

        # create list widget
        self.list = QtGui.QListWidget()
        self.list.itemSelectionChanged.connect(self.selection_changed)
        self.list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.addItems(scenario_titles)
        # set size fixed to content, width at least 200px
        self.list.setFixedSize(max(self.list.sizeHintForColumn(0) + 2 * self.list.frameWidth(), 200),
                               self.list.sizeHintForRow(0) * self.list.count() + 2 * self.list.frameWidth())

        self.layout().addWidget(self.list)

        # TODO if the height is higher than the window we may have to enable scroll bars, not now with one scenario though

    def selection_changed(self):
        """
            A scenario title has been selected in the list.
        """
        # get selected file
        row = self.list.currentRow()  # only useful if QListWidget does not sort by itself
        scenario_file = self.scenario_files[row]
        # emit title selected signal
        self.title_selected.emit(scenario_file)

    def stop(self):
        """
            Interruption. Clean up network channels and the like.
        """
        # network channel might still be open
        network_client.remove_channel(self.CH_TITLES, ignore_not_existing=True)


class OptionsContentWidget(QtGui.QWidget):
    """
        Content widget for the options/preferences dialog window, based on QTabWidget.

        TODO add option to go back to default settings
    """

    def __init__(self):
        """
            Create and add all tabs
        """
        super().__init__()

        toolbar = QtGui.QToolBar()
        toolbar.setIconSize(QtCore.QSize(32, 32))
        action_group = QtGui.QActionGroup(toolbar)

        action_preferences_general = g.create_action(t.load_ui_icon('icon.preferences.general.png'), 'Show general preferences', action_group, toggle_connection=self.toggled_general, checkable=True)
        toolbar.addAction(action_preferences_general)
        toolbar.addAction(g.create_action(t.load_ui_icon('icon.preferences.network.png'), 'Show network preferences', action_group, toggle_connection=self.toggled_network, checkable=True))
        toolbar.addAction(g.create_action(t.load_ui_icon('icon.preferences.graphics.png'), 'Show graphics preferences', action_group, toggle_connection=self.toggled_graphics, checkable=True))
        toolbar.addAction(g.create_action(t.load_ui_icon('icon.preferences.music.png'), 'Show music preferences', action_group, toggle_connection=self.toggled_music, checkable=True))


        self.stacked_layout = QtGui.QStackedLayout()

        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(toolbar)
        layout.addLayout(self.stacked_layout)

        # empty lists
        self.checkboxes = []
        self.lineedits = []

        # add tabs
        self.create_options_widget_general()
        self.create_options_widget_graphics()
        self.create_options_widget_music()
        self.create_options_widget_network()

        # show general preferences
        action_preferences_general.setChecked(True)

    def toggled_general(self, checked):
        """
            Toolbar button for general preferences toggled.
        """
        if checked is True:
            self.stacked_layout.setCurrentWidget(self.tab_general)

    def create_options_widget_general(self):
        """
            Create general options widget.
        """
        tab = QtGui.QWidget()
        tab_layout = QtGui.QVBoxLayout(tab)

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_general = tab
        self.stacked_layout.addWidget(tab)

    def toggled_graphics(self, checked):
        """
            Toolbar button for graphical preferences toggled.
        """
        if checked is True:
            self.stacked_layout.setCurrentWidget(self.tab_graphics)

    def toggled_network(self, checked):
        """
            Toolbar button for network preferences toggled.
        """
        if checked is True:
            self.stacked_layout.setCurrentWidget(self.tab_network)

    def create_options_widget_graphics(self):
        """
            Create graphical options widget.
        """

        tab = QtGui.QWidget()
        tab_layout = QtGui.QVBoxLayout(tab)

        # full screen mode
        checkbox = QtGui.QCheckBox('Full screen mode')
        self.register_checkbox(checkbox, c.O.FULLSCREEN)
        tab_layout.addWidget(checkbox)

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_graphics = tab
        self.stacked_layout.addWidget(tab)

    def toggled_music(self, checked):
        """
            Toolbar button for music preferences toggled.
        """
        if checked is True:
            self.stacked_layout.setCurrentWidget(self.tab_music)

    def create_options_widget_music(self):
        """
            Create music options widget.
        """
        tab = QtGui.QWidget()
        tab_layout = QtGui.QVBoxLayout(tab)

        # mute checkbox
        checkbox = QtGui.QCheckBox('Mute background music')
        self.register_checkbox(checkbox, c.O.BG_MUTE)
        tab_layout.addWidget(checkbox)

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_music = tab
        self.stacked_layout.addWidget(tab)

    def create_options_widget_network(self):
        """
            Create network options widget.
        """
        tab = QtGui.QWidget()
        tab_layout = QtGui.QVBoxLayout(tab)

        l = QtGui.QVBoxLayout()
        l.addWidget(QtGui.QLabel('Connected to ...'))
        button_connect = QtGui.QPushButton('Connect to nonlocal server')
        l.addWidget(button_connect)
        tab_layout.addWidget(g.wrap_in_groupbox(l, 'Connected Server'))

        l = QtGui.QVBoxLayout()
        checkbox = QtGui.QCheckBox('Accepts incoming connections')
        self.register_checkbox(checkbox, c.O.LS_OPEN)
        l.addWidget(checkbox)
        l2 = QtGui.QHBoxLayout()
        l2.addWidget(QtGui.QLabel('Alias'))
        edit = QtGui.QLineEdit()
        edit.setFixedWidth(300)
        l2.addWidget(edit)
        l2.addStretch()
        self.register_lineedit(edit, c.O.LS_NAME)
        l.addLayout(l2)
        l2 = QtGui.QHBoxLayout()
        toolbar = QtGui.QToolBar()
        toolbar.setIconSize(QtCore.QSize(24, 24))
        toolbar.addAction(g.create_action(t.load_ui_icon('icon.preferences.network.png'), 'Show network preferences', toolbar))

        # button_local_server_monitor = QtGui.QPushButton('Monitor local server')
        l2.addWidget(toolbar)
        l2.addStretch()
        l.addLayout(l2)
        tab_layout.addWidget(g.wrap_in_groupbox(l, 'Local Server'))

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_network = tab
        self.stacked_layout.addWidget(tab)

    def register_checkbox(self, checkbox, option):
        """
            Takes an option identifier (str) where the option value must be True/False and sets a checkbox according
            to the current value. Stores the checkbox, option pair in a list.
        """
        checkbox.setChecked(t.get_option(option))
        self.checkboxes.append((checkbox, option))

    def register_lineedit(self, edit, option):
        """

        """
        edit.setText(t.get_option(option))
        self.lineedits.append((edit, option))

    def close_request(self, parent_widget):
        """
            User wants to close the dialog, check if an option has been changed. If an option has been changed, ask for
            okay from user and update the options.

            Also react on some updated options (others might only take affect after a restart of the application).
            We immediately : start/stop music (mute option)
        """
        # check if something was changed
        options_modified = any([box.isChecked() is not t.get_option(option) for (box, option) in self.checkboxes])
        if options_modified:
            answer = QtGui.QMessageBox.question(parent_widget, 'Preferences', 'Save modified preferences',
                                                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
            if answer == QtGui.QMessageBox.Yes:
                # all checkboxes
                for (box, option) in self.checkboxes:
                    t.set_option(option, box.isChecked())
                # what else do we need to do?
                if t.get_option(c.O.BG_MUTE):
                    # t.player.stop()
                    pass
                else:
                    # t.player.start()
                    pass
        return True


class MainWindow(QtGui.QWidget):
    """
        The main window (widget) which is the top level window of the application. It can be full screen or not and hold
        a single widget in a margin-less layout.

        TODO should we make this as small as possible, used only once put in Client
    """

    def __init__(self):
        """
            All the necessary initializations. Is shown at the end.
        """
        super().__init__()
        # set geometry
        self.setGeometry(t.get_option(c.O.MW_BOUNDS))
        # set icon
        self.setWindowIcon(t.load_ui_icon('icon.ico'))
        # set title
        self.setWindowTitle('Imperialism Remake')

        # just a layout but nothing else
        self.layout = QtGui.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.content = None

        # show in full screen, maximized or normal
        if t.get_option(c.O.FULLSCREEN):
            self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
            self.showFullScreen()
        elif t.get_option(c.O.MW_MAXIMIZED):
            self.showMaximized()
        else:
            self.show()

        # loading animation
        # TODO animation right and start, stop in client
        self.animation = QtGui.QMovie(c.extend(c.Graphics_UI_Folder, 'loading.gif'))
        # self.animation.start()
        self.loading_label = QtGui.QLabel(self, f=QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        self.loading_label.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.loading_label.setMovie(self.animation)
        # self.loading_label.show()

    def change_content_widget(self, widget):
        """
            Another screen shall be displayed. Exchange the content widget with a new one.
        """
        if self.content:
            self.layout.removeWidget(self.content)
            self.content.deleteLater()
        self.content = widget
        self.layout.addWidget(widget)


class Client():
    """
        Main class of the client, holds the help browser, the main window (full screen or not), the content of the main
        window, the audio player
    """

    def __init__(self):
        """
            Create the main window, the help browser dialog, the audio player, ...
        """
        # main window
        self.main_window = MainWindow()

        # help browser
        self.help_browser_widget = BrowserWidget(QtCore.QUrl(c.Manual_Index), t.load_ui_icon)
        self.help_dialog = cg.GameDialog(self.main_window, self.help_browser_widget, title='Help')
        self.help_dialog.setFixedSize(QtCore.QSize(800, 600))
        # move to lower right border, so that overlap with other windows is not that strong
        self.help_dialog.move(self.main_window.x() + self.main_window.width() - 800,
                              self.main_window.y() + self.main_window.height() - 600)

        # add help browser keyboard shortcut
        action = QtGui.QAction(self.main_window)
        action.setShortcut(QtGui.QKeySequence('F1'))
        action.triggered.connect(self.show_help_browser)
        self.main_window.addAction(action)

        # add server monitor keyboard shortcut
        action = QtGui.QAction(self.main_window)
        action.setShortcut(QtGui.QKeySequence('F2'))
        action.triggered.connect(self.show_server_monitor)
        self.main_window.addAction(action)

        # for the notifications
        self.pending_notifications = []
        self.notification_position_constraint = g.RelativeLayoutConstraint().center_horizontal().south(20)
        self.notification = None

        # audio player
        self.player = audio.Player()
        self.player.next.connect(self.audio_notification)
        self.player.set_playlist(audio.load_soundtrack_playlist())
        # start audio player if wished
        if not t.get_option(c.O.BG_MUTE):
            self.player.start()

        # after the player starts, the main window is not active anymore
        # set it active again or it doesn't get keyboard focus
        self.main_window.activateWindow()

    def audio_notification(self, title):
        """
            Special kind of notification from the audio system.
        """
        text = 'Playing {}'.format(title)
        self.schedule_notification(text)

    def schedule_notification(self, text):
        """
            Generic scheduling of a notification. Will be shown immediately if no other notification is shown, otherwise
            it will be shown as soon at the of the current list of notifications to be shown.
        """
        self.pending_notifications.append(text)
        if self.notification is None:
            self.show_next_notification()

    def show_next_notification(self):
        """
            Will be called whenever a notification is shown and was cleared. Tries to show the next one if there is one.
        """
        if len(self.pending_notifications) > 0:
            message = self.pending_notifications.pop(0)
            self.notification = g.Notification(self.main_window, message,
                                               position_constraint=self.notification_position_constraint)
            self.notification.finished.connect(self.show_next_notification)
            self.notification.show()
        else:
            self.notification = None

    def show_help_browser(self, url=None):
        """
            Displays the help browser somewhere on screen. Can set a special page if needed.
        """
        # we sometimes wire signals that send parameters for url (mouseevents for example) which we do not like
        if isinstance(url, QtCore.QUrl):
            self.help_browser_widget.displayPage(url)
        self.help_dialog.show()

    def show_server_monitor(self):
        """
            Displays the server monitor as a modal window.

            TODO Do we want that non-modal?

            Is invoked when pressing F2.
        """
        monitor_widget = ServerMonitorWidget()
        dialog = cg.GameDialog(self.main_window, monitor_widget, delete_on_close=True, title='Server Monitor')
        dialog.setFixedSize(QtCore.QSize(800, 600))
        dialog.show()

    def switch_to_start_screen(self):
        """
            Switches the content of the main window to the start screen.
        """
        widget = StartScreen(self)
        self.main_window.change_content_widget(widget)

    def show_game_lobby_dialog(self):
        """
            Shows the game lobby dialog.
        """
        lobby_widget = GameLobbyWidget()
        dialog = cg.GameDialog(self.main_window, lobby_widget, delete_on_close=True, title='Game Lobby',
                               help_callback=self.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(800, 600))
        lobby_widget.single_player_start.connect(partial(self.single_player_start, dialog))
        dialog.show()

    def single_player_start(self, lobby_dialog, scenario_file, selected_nation):
        """
            Shows the main game screen which will start a scenario file and a selected nation.
        """
        lobby_dialog.close()
        widget = GameMainScreen(self)
        self.main_window.change_content_widget(widget)

    def switch_to_editor_screen(self):
        """
            Switches the content of the main window to the editor screen.
        """
        widget = EditorScreen(self)
        self.main_window.change_content_widget(widget)

    def show_options_dialog(self):
        """
            Shows the preferences dialog.
        """
        options_widget = OptionsContentWidget()
        dialog = cg.GameDialog(self.main_window, options_widget, delete_on_close=True, title='Preferences',
                               help_callback=self.show_help_browser, close_callback=options_widget.close_request)
        dialog.setFixedSize(QtCore.QSize(800, 600))
        dialog.show()

    def quit(self):
        """
            Cleans up and closes the main window which causes app.exec_() to finish.
        """
        # store state in options
        t.set_option(c.O.MW_BOUNDS, self.main_window.normalGeometry())
        t.set_option(c.O.MW_MAXIMIZED, self.main_window.isMaximized())

        # audio
        # self.player.stop()

        # close the main window
        self.main_window.close()


def network_start():
    """
        Starts the local server and connects the local client to it.
    """

    # start local server
    from server.network import server_manager
    # TODO in own thread
    server_manager.server.start(c.Network_Port)

    # connect network client of client
    network_client.connect_to_host(c.Network_Port)

    # TODO must be run at the end before app finishes
    # disconnect client
    # network_client.disconnectFromHost()

    # stop server
    # server_manager.server.stop()


def start():
    """
        Creates the Qt application and shows the main window.
    """

    # create app
    app = QtGui.QApplication([])

    # TODO multiple screen support?

    # test for desktop availability
    desktop = app.desktop()
    rect = desktop.screenGeometry()
    if rect.width() < c.Screen_Min_Size[0] or rect.height() < c.Screen_Min_Size[1]:
        # noinspection PyTypeChecker
        QtGui.QMessageBox.warning(None, 'Warning',
                                  'Actual screen size below minimal screen size {}.'.format(c.Screen_Min_Size))
        return

    # if no bounds are set, set resonable bounds
    if t.get_option(c.O.MW_BOUNDS) is None:
        t.set_option(c.O.MW_BOUNDS, desktop.availableGeometry().adjusted(50, 50, -100, -100))
        t.set_option(c.O.MW_MAXIMIZED, True)
        t.log_info('No previous bounds of the main window stored, start maximized')

    # load global stylesheet to app
    with open(c.Global_Stylesheet, 'r', encoding='utf-8') as file:
        style_sheet = file.read()
    app.setStyleSheet(style_sheet)

    # create client object and switch to start screen
    client = Client()
    client.switch_to_start_screen()

    t.log_info('client initialized, start Qt app execution')
    # TODO is this necessary to run as event?
    QtCore.QTimer.singleShot(0, network_start)
    app.exec_()