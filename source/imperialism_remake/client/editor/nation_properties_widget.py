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


class NationPropertiesWidget(QtWidgets.QWidget):
    """
    Modify nation properties dialog
    """

    # TODO when exiting redraw the big map

    def __init__(self, scenario, initial_nation=None):
        super().__init__()

        logger.debug('__init__ initial_nation:%s', initial_nation)

        self.scenario = scenario

        widget_layout = QtWidgets.QVBoxLayout(self)

        # toolbar
        toolbar = QtWidgets.QToolBar()
        a = qt.create_action(tools.load_ui_icon('icon.add.png'), 'Add nation', toolbar, self.add_nation)
        toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.delete.png'), 'Remove nation', toolbar, self.remove_nation)
        toolbar.addAction(a)
        widget_layout.addLayout(qt.wrap_in_boxlayout(toolbar))

        # nation selection combo box
        label = QtWidgets.QLabel('Choose')
        self.nation_combobox = QtWidgets.QComboBox()
        self.nation_combobox.setFixedWidth(200)
        self.nation_combobox.currentIndexChanged.connect(self.nation_selected)
        widget_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, self.nation_combobox)), 'Nations'))

        # nation info panel
        layout = QtWidgets.QVBoxLayout()

        # description
        self.description_edit = QtWidgets.QLineEdit()
        self.description_edit.setFixedWidth(300)
        self.description_edit.setText('Test')
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Description'), self.description_edit)))

        # color
        self.color_picker = QtWidgets.QPushButton()
        self.color_picker.setFixedSize(24, 24)
        self.color_picker.clicked.connect(self.show_color_picker)
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Color'), self.color_picker)))

        # capital province
        self.capital_province_edit = QtWidgets.QLineEdit()
        self.capital_province_edit.setFixedWidth(300)
        layout.addLayout(qt.wrap_in_boxlayout((QtWidgets.QLabel('Capital'), self.capital_province_edit)))

        # all provinces
        self.provinces_combobox = QtWidgets.QComboBox()
        self.provinces_combobox.setFixedWidth(300)
        self.number_provinces_label = QtWidgets.QLabel()
        layout.addLayout(qt.wrap_in_boxlayout((self.number_provinces_label, self.provinces_combobox)))

        widget_layout.addWidget(qt.wrap_in_groupbox(layout, 'Info'))

        # vertical stretch
        widget_layout.addStretch()

        # reset content
        self.reset_content()

        # select initial nation if given
        if initial_nation:
            index = utils.index_of_element(self.nations, initial_nation)
            self.nation_combobox.setCurrentIndex(index)

    def show_color_picker(self):
        """
        Selects a color
        """
        logger.debug('show_color_picker')

        new_color = QtWidgets.QColorDialog.getColor(self.color, parent=self)
        # isValid() returns True if dialog wasn't cancelled
        if new_color.isValid():
            index = self.nation_combobox.currentIndex()
            nation = self.nations[index]
            self.scenario.server_scenario.set_nation_property(nation, constants.NationProperty.COLOR, new_color.name())

            self.nation_selected(index)

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
        self.description_edit.setText(self.scenario.server_scenario.nation_property(nation,
                                                                                    constants.NationProperty.DESCRIPTION))

        province = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.CAPITAL_PROVINCE)
        self.capital_province_edit.setText(self.scenario.server_scenario.province_property(province,
                                                                                           constants.ProvinceProperty.NAME))

        # color
        color_name = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.COLOR)
        self.color = QtGui.QColor(color_name)
        self.color_picker.setStyleSheet('QPushButton { background-color: ' + color_name + '; }')

        provinces = self.scenario.server_scenario.nation_property(nation, constants.NationProperty.PROVINCES)
        provinces_names = [self.scenario.server_scenario.province_property(p, constants.ProvinceProperty.NAME)
                           for p in provinces]
        self.number_provinces_label.setText('Provinces ({})'.format(len(provinces)))
        self.provinces_combobox.clear()
        self.provinces_combobox.addItems(provinces_names)

    def add_nation(self):
        """
        Adds a nation.
        """
        logger.debug('add_nation')

        name, ok = QtWidgets.QInputDialog.getText(self, 'Add Nation', 'Name')
        if ok:
            # TODO what if nation with the same name already exists
            # TODO check for sanity of name (no special letters, minimal number of letters)
            nation = self.scenario.server_scenario.add_nation()
            self.scenario.server_scenario.set_nation_property(nation, constants.NationProperty.NAME, name)
            # reset content
            self.reset_content()

    def remove_nation(self):
        """
        Removes a nation.
        """
        logger.debug('remove_nation')

        index = self.nation_combobox.currentIndex()
        name = self.nation_combobox.currentText()
        answer = QtWidgets.QMessageBox.question(self, 'Warning', 'Remove {}'.format(name),
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.Yes)
        if answer == QtWidgets.QMessageBox.Yes:
            nation = self.nations[index]

            # there is no going back on this one
            self.scenario.server_scenario.remove_nation(nation)

            # reset content
            self.reset_content()
