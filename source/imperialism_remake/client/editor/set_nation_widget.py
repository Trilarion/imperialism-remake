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

from PyQt5 import QtWidgets, QtGui

from imperialism_remake.base import tools, constants
from imperialism_remake.lib import qt, utils

logger = logging.getLogger(__name__)


class SetNationWidget(QtWidgets.QWidget):
    """
    Modify nation properties dialog
    """

    # TODO when exiting redraw the big map

    def __init__(self, scenario, main_map, row, column, nation, province):
        super().__init__()

        logger.debug(f'__init__ at {row}, {column}')

        self.scenario = scenario

        self._main_map = main_map
        self._row = row
        self._column = column

        widget_layout = QtWidgets.QVBoxLayout(self)

        # nation selection combo box
        label = QtWidgets.QLabel('Choose')
        self.nation_combobox = QtWidgets.QComboBox()
        self.nation_combobox.setFixedWidth(200)
        self.nation_combobox.currentIndexChanged.connect(self.nation_selected)
        widget_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, self.nation_combobox)), 'Nations'))

        # nation info panel
        layout = QtWidgets.QVBoxLayout()

        # color
        self.color_picker = QtWidgets.QPushButton()
        self.color_picker.setFixedSize(24, 24)
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Color'), self.color_picker)))

        # all provinces
        self.provinces_combobox = QtWidgets.QComboBox()
        self.provinces_combobox.setFixedWidth(300)
        self.provinces_combobox.currentIndexChanged.connect(self.province_selected)
        self.number_provinces_label = QtWidgets.QLabel()
        layout.addLayout(qt.wrap_in_boxlayout((self.number_provinces_label, self.provinces_combobox)))

        widget_layout.addWidget(qt.wrap_in_groupbox(layout, 'Info'))

        # vertical stretch
        widget_layout.addStretch()

        # reset content
        self.reset_content()

        # select initial nation if given
        if nation:
            index = utils.index_of_element(self.nations, nation)
            self.nation_combobox.setCurrentIndex(index)
        elif self.nations:
            index = utils.index_of_element(self.nations, self.nations[0])
            self.nation_combobox.setCurrentIndex(index)

        if province:
            provinces = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.PROVINCES)
            index = utils.index_of_element(provinces, province)
            self.provinces_combobox.setCurrentIndex(index)

    def reset_content(self):
        """
        With data.

        """
        logger.debug('reset_content')

        # get all nation ids
        nations = self.scenario.server_scenario.nations()
        # get names for all nations
        name_of_nation = [(self.scenario.server_scenario.nation_property(nation, constants.NationProperty.NAME), nation)
                          for nation in nations]
        if name_of_nation:
            name_of_nation = sorted(name_of_nation)  # by first element, which is the name
            nation_names, self.nations = zip(*name_of_nation)
        else:
            nation_names = []
            self.nations = []

        self.nation_combobox.clear()
        self.nation_combobox.addItems(nation_names)

    def nation_selected(self, index):
        """
        A nation is selected

        :param index:
        """
        logger.debug('nation_selected index:%s', index)

        nation = self.nations[index]

        # color
        color_name = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.COLOR)
        self.color_picker.setStyleSheet('QPushButton { background-color: ' + color_name + '; }')

        provinces = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.PROVINCES)
        provinces_names = [self.scenario.server_scenario.province_property(p, constants.ProvinceProperty.NAME)
                           for p in provinces]
        self.number_provinces_label.setText('Provinces ({})'.format(len(provinces)))
        self.provinces_combobox.clear()
        self.provinces_combobox.addItems(provinces_names)

        self._main_map.change_nation_tile(self._row, self._column, provinces[0])

    def province_selected(self, index):
        logger.debug('province_selected index:%s', index)

        nation = self.nations[self.nation_combobox.currentIndex()]
        provinces = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.PROVINCES)

        self._main_map.change_nation_tile(self._row, self._column, provinces[index])
