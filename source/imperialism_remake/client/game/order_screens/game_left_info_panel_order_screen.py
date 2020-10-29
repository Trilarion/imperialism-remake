# Imperialism remake
# Copyright (C) 2020 amtyurin
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
import logging

from PyQt5 import QtWidgets

from imperialism_remake.base import tools
from imperialism_remake.client.game.game_scenario import GameScenario

logger = logging.getLogger(__name__)


class GameLeftInfoPanel(QtWidgets.QWidget):
    def __init__(self, scenario: GameScenario, client):
        """
        Layout.
        """
        super().__init__()

        logger.debug('__init__')

        self._scenario = scenario
        self._client = client

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.back_to_startscreen.png'))
        button.clicked.connect(self._exit_clicked)
        button.setFixedSize(32, 32)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(button)
        layout.addStretch()

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(spacer)

    def _exit_clicked(self):
        logger.debug("_exit_clicked")

        self._client.widget_switcher.switch(self._client.game_widget)
