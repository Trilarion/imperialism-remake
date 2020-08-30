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

from imperialism_remake.base import constants
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


class ScenarioPropertiesWidget(QtWidgets.QWidget):
    """
    Modify general properties of a scenario dialog.
    """

    # TODO same mechanism like for preferences?
    def __init__(self, scenario):
        super().__init__()

        self.scenario = scenario

        widget_layout = QtWidgets.QVBoxLayout(self)

        # title
        # TODO validator for title, no empty string
        self.title_edit = QtWidgets.QLineEdit()
        self.title_edit.setFixedWidth(300)
        self.title_edit.setText(self.scenario.server_scenario[constants.ScenarioProperty.TITLE])
        widget_layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Title'), self.title_edit)))

        # description
        self.description_edit = QtWidgets.QLineEdit()
        self.description_edit.setFixedWidth(300)
        self.description_edit.setText(self.scenario.server_scenario[constants.ScenarioProperty.DESCRIPTION])
        widget_layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Description'), self.description_edit)))

        # game years
        game_range = self.scenario.server_scenario[constants.ScenarioProperty.GAME_YEAR_RANGE]
        self.game_year_from = QtWidgets.QLineEdit()
        self.game_year_from.setFixedWidth(100)
        self.game_year_from.setText(str(game_range[0]))
        self.game_year_to = QtWidgets.QLineEdit()
        self.game_year_to.setFixedWidth(100)
        self.game_year_to.setText(str(game_range[1]))
        widget_layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Time range from'), self.game_year_from,
                                                      QtWidgets.QLabel('to'), self.game_year_to)))

        # vertical stretch
        widget_layout.addStretch()

    def on_ok(self):
        """
        We may have changes to apply.
        """
        logger.debug('on_ok')

        pass

    def close_request(self, parent_widget):
        """
        Dialog will be closed, save data.
        """
        logger.debug('close_request')

        self.scenario.server_scenario[constants.ScenarioProperty.TITLE] = self.title_edit.text()
        self.scenario.server_scenario[constants.ScenarioProperty.DESCRIPTION] = self.description_edit.text()

        return True
