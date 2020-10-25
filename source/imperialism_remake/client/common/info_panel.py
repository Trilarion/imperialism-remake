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
from imperialism_remake.client.game.unit_buttons_widget import UnitButtonsWidget
from imperialism_remake.server.models.prospector_resource_state import ProspectorResourceState

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

        logger.debug('__init__')

        self.scenario = scenario

        self.setObjectName('info-box-widget')
        layout = QtWidgets.QVBoxLayout(self)

        self._unit_buttons_widget = UnitButtonsWidget(self.scenario)
        layout.addWidget(self._unit_buttons_widget)
        self._unit_buttons_widget.hide()

        self.tile_label = QtWidgets.QLabel()
        self.tile_label.setTextFormat(QtCore.Qt.RichText)
        layout.addWidget(self.tile_label)

        self.resource_label = QtWidgets.QLabel()
        self.resource_label.setTextFormat(QtCore.Qt.RichText)
        layout.addWidget(self.resource_label)

        self.province_label = QtWidgets.QLabel()
        layout.addWidget(self.province_label)

        self.nation_label = QtWidgets.QLabel()
        layout.addWidget(self.nation_label)

        self.workforce_label = QtWidgets.QLabel()
        layout.addWidget(self.workforce_label)

        self.selected_object_label = QtWidgets.QLabel()
        layout.addWidget(self.selected_object_label)

        layout.addStretch()

        self.nation_asset_label = QtWidgets.QLabel()
        layout.addWidget(self.nation_asset_label)

    def get_unit_buttons_widget(self):
        return self._unit_buttons_widget

    def update_tile_info(self, column, row):
        """
        Displays data of a new tile (hovered or clicked in the main map).

        :param column: The tile column.
        :param row: The tile row.
        """
        # logger.debug('update_tile_info column:%s, row:%s', column, row)

        text = 'Position ({}, {})'.format(column, row)

        terrain = self.scenario.server_scenario.terrain_at(column, row)
        terrain_name = self.scenario.server_scenario.terrain_name(terrain)
        text += '<br>Terrain: {}'.format(terrain_name)

        nation = self.scenario.server_scenario.nation_at(row, column)
        if nation:
            name = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.NAME)
            text += '<br>Nation: {}'.format(name)

        province = self.scenario.server_scenario.province_at(column, row)
        if province:
            name = self.scenario.server_scenario.province_property(province, constants.ProvinceProperty.NAME)
            text += '<br>Province: {}'.format(name)

        self._update_resource_info(column, row)

        self.tile_label.setText(text)

    def _update_resource_info(self, column, row):
        resource = self.scenario.server_scenario.terrain_resource_at(column, row)
        if resource > 0:
            resource_name = self.scenario.server_scenario.terrain_resource_name(resource)
            resource_text = 'Resource: {}'.format(resource_name)
            self.resource_label.setText(resource_text)
        else:
            resource_text = ''
            player_nation = self.scenario.server_scenario.get_player_nation()
            if player_nation:
                for prospector_resource_id, prospector_resource_state in self.scenario.server_scenario.get_nation_prospector_resource_state(
                        self.scenario.server_scenario.get_player_nation(), row, column).items():
                    if prospector_resource_state == ProspectorResourceState.REVEALED or prospector_resource_state == ProspectorResourceState.PROCESSED:
                        resource_name = self.scenario.server_scenario.terrain_resource_name(prospector_resource_id)
                        if resource_text == '':
                            resource_text = 'Resource: {}'.format(resource_name)
                        else:
                            resource_text = ', {}'.format(resource_name)

            self.resource_label.setText(resource_text)

    def update_workforce_info(self, name):
        if name is None:
            self.workforce_label.setText('')
        else:
            self.workforce_label.setText('<br>Worker: {}'.format(name))

    def update_selected_object_info(self, name):
        if name is None:
            self.selected_object_label.setText('')
        else:
            self.selected_object_label.setText('<br>Selected: {}'.format(name))

    def refresh_nation_asset_info(self):
        asset_text = self._print_data_using_value(self.scenario.server_scenario.get_nation_asset(
            self.scenario.server_scenario.get_player_nation()).get_raw_resources(),
                                                  self.scenario.server_scenario.raw_resource_name)

        asset_text += self._print_data(self.scenario.server_scenario.get_nation_asset(
            self.scenario.server_scenario.get_player_nation()).get_materials(),
                                       self.scenario.server_scenario.material_name)

        asset_text += self._print_data(self.scenario.server_scenario.get_nation_asset(
            self.scenario.server_scenario.get_player_nation()).get_goods(),
                                       self.scenario.server_scenario.good_name)
        self.nation_asset_label.setText(asset_text)

    def _print_data_using_value(self, resources, name_getter):
        asset_text = '<br>==='
        i = 0
        for name, resource in resources.items():
            if i % 3 == 0:
                asset_text += '<br>{}: {} '.format(name_getter(name.value), resource)
            else:
                asset_text += '{}: {} '.format(name_getter(name.value), resource)
            i += 1
        return asset_text

    def _print_data(self, resources, name_getter):
        asset_text = '<br>==='
        i = 0
        for name, resource in resources.items():
            if i % 3 == 0:
                asset_text += '<br>{}: {} '.format(name_getter(name), resource)
            else:
                asset_text += '{}: {} '.format(name_getter(name), resource)
            i += 1
        return asset_text

    def show_unit_buttons(self, workforce):
        logger.debug('show_unit_buttons, workforce type: %s', workforce.get_type())
        self._unit_buttons_widget.show()

    def hide_unit_buttons(self, workforce):
        logger.debug('hide_unit_buttons, workforce type: %s', workforce.get_type())
        self._unit_buttons_widget.hide()
