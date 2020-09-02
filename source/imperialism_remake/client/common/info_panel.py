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

from imperialism_remake.base import constants
from imperialism_remake.client.common.generic_scenario import GenericScenario

logger = logging.getLogger(__name__)


class InfoPanel(QtWidgets.QWidget):
    """
    Info box on the right side of the editor.
    """

    def __init__(self, scenario: GenericScenario):
        """
        Layout.
        """
        super().__init__()

        logger.debug('GenericScreen __init__')

        self.scenario = scenario

        self.setObjectName('info-box-widget')
        layout = QtWidgets.QVBoxLayout(self)

        self.tile_label = QtWidgets.QLabel()
        self.tile_label.setTextFormat(QtCore.Qt.RichText)
        layout.addWidget(self.tile_label)

        self.province_label = QtWidgets.QLabel()
        layout.addWidget(self.province_label)

        self.nation_label = QtWidgets.QLabel()
        layout.addWidget(self.nation_label)

        self.workforce_label = QtWidgets.QLabel()
        layout.addWidget(self.workforce_label)

        layout.addStretch()

    def update_tile_info(self, column, row):
        """
        Displays data of a new tile (hovered or clicked in the main map).

        :param column: The tile column.
        :param row: The tile row.
        """
        logger.debug('update_tile_info column:%s, row:%s', column, row)

        text = 'Position ({}, {})'.format(column, row)
        terrain = self.scenario.server_scenario.terrain_at(column, row)
        terrain_name = self.scenario.server_scenario.terrain_name(terrain)
        text += '<br>Terrain: {}'.format(terrain_name)
        province = self.scenario.server_scenario.province_at(column, row)
        if province is not None:
            name = self.scenario.server_scenario.province_property(province, constants.ProvinceProperty.NAME)
            text += '<br>Province: {}'.format(name)

        self.tile_label.setText(text)

    def update_workforce_info(self, name):
        if name is None:
            self.workforce_label.setText('')
        else:
            self.workforce_label.setText('<br>Worker: {}'.format(name))
