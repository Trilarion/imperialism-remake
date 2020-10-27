# Imperialism remake
# Copyright (C) 2016 Trilarion
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
Game lobby. Place for starting/loading games.
"""
import logging
from functools import partial

from PyQt5 import QtCore, QtWidgets

from imperialism_remake.base import constants, tools
from imperialism_remake.client.lobby.server_lobby import ServerLobby
from imperialism_remake.client.lobby.single_player_scenario_preview import SinglePlayerScenarioPreview
from imperialism_remake.client.lobby.single_player_scenario_title_selection import SinglePlayerScenarioTitleSelection
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


class GameLobbyWidget(QtWidgets.QWidget):
    """
    Content widget for the game lobby.
    """

    single_player_start = QtCore.pyqtSignal(str, int)

    def __init__(self, *args, **kwargs):
        """
        Create toolbar.
        """
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # create tool bar
        toolbar = QtWidgets.QToolBar()
        action_group = QtWidgets.QActionGroup(toolbar)

        # actions single player new/load
        a = qt.create_action(tools.load_ui_icon('icon.lobby.single.new.png'),
                             'Start new single player scenario', action_group,
                             toggle_connection=self.toggled_single_player_scenario_selection, checkable=True)
        toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.lobby.single.load.png'),
                             'Continue saved single player scenario', action_group,
                             toggle_connection=self.toggled_single_player_load_scenario, checkable=True)
        toolbar.addAction(a)

        toolbar.addSeparator()

        # actions multi player
        a = qt.create_action(tools.load_ui_icon('icon.lobby.network.png'),
                             'Show server lobby', action_group,
                             toggle_connection=self.toggled_server_lobby, checkable=True)
        toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.lobby.multiplayer-game.png'),
                             'Start or continue multiplayer scenario', action_group,
                             toggle_connection=self.toggled_multiplayer_scenario_selection, checkable=True)
        toolbar.addAction(a)

        self.layout.addWidget(toolbar, alignment=QtCore.Qt.AlignTop)

        self.content = None

    def change_content_widget(self, widget, alignment=None):
        """
        Another screen shall be displayed. Exchange the content widget with a new one.
        """
        if self.content:
            self.layout.removeWidget(self.content)
            self.content.deleteLater()

        self.content = widget

        if self.content:
            if alignment:
                self.layout.addWidget(widget, stretch=1, alignment=alignment)
            else:
                self.layout.addWidget(widget, stretch=1)

    def toggled_single_player_scenario_selection(self, checked):
        """
        Toolbar action switch to single player scenario selection.
        """

        if checked:
            # create single player scenario title selection widget
            widget = SinglePlayerScenarioTitleSelection()
            # TODO: remove line below?
            #           widget.title_selected.connect(self.single_player_scenario_selection_preview, QtCore.Qt.QueuedConnection)
            widget.title_selected.connect(self.single_player_scenario_selection_preview)

            # change content widget
            self.change_content_widget(widget, QtCore.Qt.AlignVCenter)

    def toggled_single_player_load_scenario(self, checked):
        """
        Toolbar action switch to single player load a scenario.
        """

        if checked:
            # noinspection PyCallByClass
            file_name = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Continue Single Player Scenario', constants.SCENARIO_FOLDER, 'Scenario Files (*.scenario)')[0]
            if file_name:
                self.single_player_scenario_selection_preview(file_name)

    def toggled_server_lobby(self, checked):
        """
        Toolbar action switch to server lobby.
        """
        if checked:
            # create new widget
            widget = ServerLobby()

            # change content widget
            self.change_content_widget(widget)

    def toggled_multiplayer_scenario_selection(self, checked):
        """
        Toolbar action switch to multiplayer scenario selection.
        """
        if checked:
            pass

    def single_player_scenario_selection_preview(self, scenario_file):
        """
        Single player scenario selection, a scenario title was selected, show preview.
        """

        # create single player scenario preview widget
        widget = SinglePlayerScenarioPreview(scenario_file)
        widget.nation_selected.connect(partial(self.single_player_start.emit, scenario_file))

        # change content widget
        self.change_content_widget(widget)
