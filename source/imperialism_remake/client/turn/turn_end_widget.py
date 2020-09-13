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

from imperialism_remake.base import tools
from imperialism_remake.client.turn.turn_manager import TurnManager

logger = logging.getLogger(__name__)


class TurnEndWidget(QtWidgets.QWidget):
    def __init__(self, turn_manager: TurnManager):
        super().__init__()

        button = QtWidgets.QPushButton( "", self)
        button.setIcon(tools.load_ui_icon('icon.end_turn.png'))
        button.setIconSize(QtCore.QSize(24, 24))
        button.clicked.connect(self._turn_end_clicked)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(button)

        self._turn_manager = turn_manager

    def _turn_end_clicked(self):
        logger.debug("_turn_end_clicked")

        self._turn_manager.make_turn()
