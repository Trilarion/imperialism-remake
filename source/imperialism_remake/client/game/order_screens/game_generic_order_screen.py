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
from imperialism_remake.client.game.game_scenario import GameScenario
from imperialism_remake.client.game.order_screens.game_left_info_panel_order_screen import GameLeftInfoPanel
from imperialism_remake.client.game.order_screens.game_order_diplomacy_screen import GameOrderDiplomacyScreen
from imperialism_remake.client.game.order_screens.game_order_industry_screen import GameOrderIndustryScreen
from imperialism_remake.client.game.order_screens.game_order_market_screen import GameOrderMarketScreen
from imperialism_remake.client.game.order_screens.game_order_transport_screen import GameOrderTransportScreen
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


class GameGenericOrderScreen(QtWidgets.QGraphicsView):
    """
    The screen the contains the whole scenario editor. Is copied into the application main window if the user
    clicks on the editor pixmap in the client main screen.
    """

    def __init__(self, scenario: GameScenario, client):
        """
        Create and setup all the elements.
        """
        super().__init__()

        logger.debug('__init__')

        self.scenario = scenario
        self.client = client

        # toolbar on top of the window
        self._toolbar = QtWidgets.QToolBar()
        self._toolbar.setIconSize(QtCore.QSize(32, 32))

        self._add_order_buttons_on_top()

        self._layout = QtWidgets.QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addWidget(self._toolbar, 0, 0, 1, 2)
        self._layout.addWidget(GameLeftInfoPanel(self.scenario, self.client), 1, 0)

        self._layout.setRowStretch(1, 1)
        self._layout.setColumnStretch(1, 1)

        self._screen = None

    def _add_order_buttons_on_top(self):
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._toolbar.addWidget(spacer)

        self._transport_top_button = QtWidgets.QAction(tools.load_ui_icon('icon.order_screen.transport.png'), 'Transport', self)
        self._transport_top_button.triggered.connect(self._transport_clicked)
        self._toolbar.addAction(self._transport_top_button)

        self._industry_top_button = QtWidgets.QAction(tools.load_ui_icon('icon.order_screen.industry.png'), 'Industry', self)
        self._industry_top_button.triggered.connect(self._industry_clicked)
        self._toolbar.addAction(self._industry_top_button)

        self._market_top_button = QtWidgets.QAction(tools.load_ui_icon('icon.order_screen.market.png'), 'Market', self)
        self._market_top_button.triggered.connect(self._market_clicked)
        self._toolbar.addAction(self._market_top_button)

        self._diplomacy_top_button = QtWidgets.QAction(tools.load_ui_icon('icon.order_screen.diplomacy.png'), 'Diplomacy', self)
        self._diplomacy_top_button.triggered.connect(self._diplomacy_clicked)
        self._toolbar.addAction(self._diplomacy_top_button)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._toolbar.addWidget(spacer)

        self._toolbar.addSeparator()

        clock = qt.ClockLabel()
        self._toolbar.addWidget(clock)

    def set_transport_screen(self):
        self._set_screen(GameOrderTransportScreen)

        self._transport_top_button.setDisabled(True)
        self._industry_top_button.setDisabled(False)
        self._market_top_button.setDisabled(False)
        self._diplomacy_top_button.setDisabled(False)

    def set_industry_screen(self):
        self._set_screen(GameOrderIndustryScreen)

        self._transport_top_button.setDisabled(False)
        self._industry_top_button.setDisabled(True)
        self._market_top_button.setDisabled(False)
        self._diplomacy_top_button.setDisabled(False)

    def set_market_screen(self):
        self._set_screen(GameOrderMarketScreen)

        self._transport_top_button.setDisabled(False)
        self._industry_top_button.setDisabled(False)
        self._market_top_button.setDisabled(True)
        self._diplomacy_top_button.setDisabled(False)

    def set_diplomacy_screen(self):
        self._set_screen(GameOrderDiplomacyScreen)

        self._transport_top_button.setDisabled(False)
        self._industry_top_button.setDisabled(False)
        self._market_top_button.setDisabled(False)
        self._diplomacy_top_button.setDisabled(True)

    def _set_screen(self, type_screen):
        if self._screen:
            self._layout.removeWidget(self._screen)

        self._screen = type_screen(self.scenario, self.client)
        self._layout.addWidget(self._screen, 1, 1)

    def _transport_clicked(self):
        self.set_transport_screen()

    def _industry_clicked(self):
        self.set_industry_screen()

    def _market_clicked(self):
        self.set_market_screen()

    def _diplomacy_clicked(self):
        self.set_diplomacy_screen()
