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
import os

from PyQt5 import QtCore, QtWidgets

from imperialism_remake.base import tools, constants
from imperialism_remake.client.common.generic_screen import GenericScreen
from imperialism_remake.client.editor.change_terrain_widget import ChangeTerrainWidget
from imperialism_remake.client.editor.editor_mainmap import EditorMainMap
from imperialism_remake.client.editor.editor_scenario import EditorScenario
from imperialism_remake.client.editor.nation_properties_widget import NationPropertiesWidget
from imperialism_remake.client.editor.new_scenario_widget import NewScenarioWidget
from imperialism_remake.client.editor.province_property_widget import ProvincePropertiesWidget
from imperialism_remake.client.editor.scenario_properties_widget import ScenarioPropertiesWidget
from imperialism_remake.client.graphics.game_dialog import GameDialog
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


class EditorScreen(GenericScreen):
    """
    The screen the contains the whole scenario editor. Is copied into the application main window if the user
    clicks on the editor pixmap in the client main screen.
    """

    def __init__(self, client):
        """
        Create and setup all the elements.
        """
        self.scenario = EditorScenario()

        super().__init__(client, self.scenario, EditorMainMap(self.scenario))

        # new, load, save scenario actions
        a = qt.create_action(tools.load_ui_icon('icon.scenario.new.png'), 'Create new scenario', self,
                             self.new_scenario_dialog)
        self._toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.scenario.load.png'), 'Load scenario', self,
                             self.load_scenario_dialog)
        self._toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.scenario.save.png'), 'Save scenario', self,
                             self.save_scenario_dialog)
        self._toolbar.addAction(a)

        # main map
        self.main_map.change_terrain.connect(self.map_change_terrain)
        self.main_map.province_info.connect(self.provinces_dialog)
        self.main_map.nation_info.connect(self.nations_dialog)

        # edit properties (general, nations, provinces) actions
        a = qt.create_action(tools.load_ui_icon('icon.editor.general.png'), 'Edit general properties', self,
                             self.general_properties_dialog)
        self._toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.editor.nations.png'), 'Edit nations', self, self.nations_dialog)
        self._toolbar.addAction(a)
        a = qt.create_action(tools.load_ui_icon('icon.editor.provinces.png'), 'Edit provinces', self,
                             self.provinces_dialog)
        self._toolbar.addAction(a)

    def new_scenario_dialog(self):
        """
        Shows the dialog for creation of a new scenario dialog and connect the "create new scenario" signal.
        """
        content_widget = NewScenarioWidget()
        content_widget.finished.connect(self.scenario.create)
        dialog = GameDialog(self._client.main_window, content_widget, title='New Scenario',
                            delete_on_close=True, help_callback=self._client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(600, 400))
        dialog.show()

    def load_scenario_dialog(self):
        """
        Show the load a scenario dialog. Then loads it if the user has selected one.
        """
        # noinspection PyCallByClass
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Load Scenario', constants.SCENARIO_FOLDER,
                                                          'Scenario Files (*.scenario)')[0]
        if file_name:
            self.scenario.load(file_name)
            # TODO: on fast PC notification is shown after loading and leads to black screen
            # self.client.schedule_notification('Loaded scenario {}'
            #                                  .format(editor_scenario.scenario[constants.ScenarioProperty.TITLE]))

    def save_scenario_dialog(self):
        """
            Show the save a scenario dialog. Then saves it.
        """
        # noinspection PyCallByClass
        file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Scenario', constants.SCENARIO_FOLDER,
                                                          'Scenario Files (*.scenario)')[0]
        if file_name:
            self.scenario.server_scenario.save(file_name)
            path, name = os.path.split(file_name)
            self._client.schedule_notification('Saved to {}'.format(name))

    def map_change_terrain(self, column, row):
        """
        :param column:
        :param row:
        """
        content_widget = ChangeTerrainWidget(self, column, row)
        dialog = GameDialog(self._client.main_window, content_widget, title='Change terrain',
                            delete_on_close=True, help_callback=self._client.show_help_browser)
        # dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()

    def general_properties_dialog(self):
        """
        Display the modify general properties dialog.
        """
        if not self.scenario.server_scenario:
            return

        content_widget = ScenarioPropertiesWidget(self.scenario)
        dialog = GameDialog(self._client.main_window, content_widget, title='General Properties',
                            delete_on_close=True, help_callback=self._client.show_help_browser,
                            close_callback=content_widget.close_request)
        # TODO derive meaningful size depending on screen size
        dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()

    def nations_dialog(self, nation=None):
        """
        Show the modify nations dialog.
        """
        if not self.scenario.server_scenario:
            return

        content_widget = NationPropertiesWidget(self.scenario, nation)
        dialog = GameDialog(self._client.main_window, content_widget, title='Nations', delete_on_close=True,
                            help_callback=self._client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()

    def provinces_dialog(self, province=None):
        """
            Display the modify provinces dialog.
        """
        if not self.scenario.server_scenario:
            return

        content_widget = ProvincePropertiesWidget(self.scenario, province)
        dialog = GameDialog(self._client.main_window, content_widget, title='Provinces', delete_on_close=True,
                            help_callback=self._client.show_help_browser)
        dialog.setFixedSize(QtCore.QSize(900, 700))
        dialog.show()
