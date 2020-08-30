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
from imperialism_remake.lib import qt, utils

logger = logging.getLogger(__name__)


class ProvincePropertiesWidget(QtWidgets.QWidget):
    """
    Modify provinces properties dialog.
    """

    def __init__(self, scenario, initial_province=None):
        super().__init__()

        self.scenario = scenario

        widget_layout = QtWidgets.QVBoxLayout(self)

        # toolbar
        toolbar = QtWidgets.QToolBar()
        a = qt.create_action(tools.load_ui_icon('icon.add.png'), 'Add province', toolbar, self.add_province)
        toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.delete.png'), 'Remove province', toolbar, self.remove_province)
        toolbar.addAction(a)
        widget_layout.addLayout(qt.wrap_in_boxlayout(toolbar))

        # provinces selection combo box
        label = QtWidgets.QLabel('Choose')
        self.provinces_combobox = QtWidgets.QComboBox()
        self.provinces_combobox.setFixedWidth(200)
        self.provinces_combobox.currentIndexChanged.connect(self.province_combobox_index_changed)
        widget_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, self.provinces_combobox)),
                                                    'provinces'))

        # province info panel
        layout = QtWidgets.QVBoxLayout()

        # nation
        self.nation_label = QtWidgets.QLabel('Nation')
        layout.addWidget(self.nation_label)

        widget_layout.addWidget(qt.wrap_in_groupbox(layout, 'Info'))

        # vertical stretch
        widget_layout.addStretch()

        # reset content
        self.reset_content()

        # if province is given, select it
        if initial_province:
            index = utils.index_of_element(self.provinces, initial_province)
            self.provinces_combobox.setCurrentIndex(index)

    def reset_content(self):
        """
        Resets the content.
        """
        logger.debug('reset_content')

        # get all province ids
        provinces = self.scenario.server_scenario.provinces()
        # get names for all provinces
        name_of_province = [
            (self.scenario.server_scenario.province_property(province, constants.ProvinceProperty.NAME), province)
            for province in provinces]
        if name_of_province:
            name_of_province = sorted(name_of_province)  # by first element, which is the name
            province_names, self.provinces = zip(*name_of_province)
        else:
            province_names = []
            self.provinces = []
        self.provinces_combobox.clear()
        self.provinces_combobox.addItems(province_names)

    def province_combobox_index_changed(self, index):
        """

        :param index:
        """
        logger.debug('province_combobox_index_changed index:%s', index)

        province = self.provinces[index]
        nation = self.scenario.server_scenario.province_property(province, constants.ProvinceProperty.NATION)
        if nation:
            self.nation_label.setText(
                self.scenario.server_scenario.nation_property(nation, constants.NationProperty.NAME))
        else:
            self.nation_label.setText('None')

    def add_province(self):
        """
        Adds a province.
        """
        logger.debug('add_province')

        name, ok = QtWidgets.QInputDialog.getText(self, 'Add Province', 'Name')
        if ok:
            # TODO what if province with the same name already exists
            # TODO check for sanity of name (no special letters, minimal number of letters)
            province = self.scenario.server_scenario.add_province()
            self.scenario.server_scenario.set_province_property(province, constants.ProvinceProperty.NAME, name)

            # reset content
            self.reset_content()

    def remove_province(self):
        """
        Removes a province.
        """
        logger.debug('remove_province')

        index = self.provinces_combobox.currentIndex()
        name = self.provinces_combobox.currentText()
        answer = QtWidgets.QMessageBox.question(self, 'Warning', 'Remove {}'.format(name),
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.Yes)
        if answer == QtWidgets.QMessageBox.Yes:
            province = self.provinces[index]
            self.scenario.server_scenario.remove_province(province)  # there is no going back on this one

            # reset content
            self.reset_content()
