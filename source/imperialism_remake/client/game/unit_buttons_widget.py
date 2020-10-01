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

from PyQt5 import QtWidgets, QtCore

from imperialism_remake.base import tools, constants
from imperialism_remake.client.game.turn_manager import TurnManager

BUTTON_WIDTH = (constants.PANEL_VIEW_WIDTH - 32) // 5

logger = logging.getLogger(__name__)


class UnitButtonsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        logger.debug('__init__')

        buttons = QtWidgets.QToolBar()
        buttons.setFixedWidth(constants.PANEL_VIEW_WIDTH - 32)
        buttons.setFixedHeight(BUTTON_WIDTH)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.unit.disband.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._disband_clicked)

        buttons.addWidget(button)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.unit.next.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._next_unit_clicked)

        buttons.addWidget(button)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.unit.done.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._done_clicked)

        buttons.addWidget(button)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.unit.sleep.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._sleep_clicked)

        buttons.addWidget(button)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(buttons)
        layout.addStretch()

    def _disband_clicked(self):
        logger.debug("_disband_clicked")

    def _next_unit_clicked(self):
        logger.debug("_next_unit_clicked")

    def _done_clicked(self):
        logger.debug("_done_clicked")

    def _sleep_clicked(self):
        logger.debug("_sleep_clicked")