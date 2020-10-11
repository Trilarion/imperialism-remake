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

from imperialism_remake.base import tools, constants

BUTTON_WIDTH = constants.PANEL_VIEW_WIDTH // 5

logger = logging.getLogger(__name__)


class OrderButtonsWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        logger.debug('__init__')

        buttons = QtWidgets.QToolBar()
        buttons.setFixedWidth(constants.PANEL_VIEW_WIDTH)
        buttons.setFixedHeight(BUTTON_WIDTH)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.transport.button.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._transport_clicked)

        buttons.addWidget(button)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.industry.button.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._industry_clicked)

        buttons.addWidget(button)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.market.button.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._market_clicked)

        buttons.addWidget(button)

        button = QtWidgets.QPushButton("", self)
        button.setIcon(tools.load_ui_icon('icon.diplomacy.button.png'))
        button.setFixedSize(BUTTON_WIDTH, BUTTON_WIDTH)
        button.clicked.connect(self._diplomacy_clicked)

        buttons.addWidget(button)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(buttons)
        layout.addStretch()

    def _transport_clicked(self):
        logger.debug("_transport_clicked")

    def _industry_clicked(self):
        logger.debug("_industry_clicked")

    def _market_clicked(self):
        logger.debug("_market_clicked")

    def _diplomacy_clicked(self):
        logger.debug("_diplomacy_clicked")
