# Imperialism remake
# Copyright (C) 2015-16 Trilarion
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

"""
The main game screen.
"""
import logging
import uuid

from PyQt5 import QtGui, QtCore

from imperialism_remake.base import constants
from imperialism_remake.client.common.generic_screen import GenericScreen
from imperialism_remake.client.common.main_map import MainMap
from imperialism_remake.client.game.game_scenario import GameScenario
from imperialism_remake.client.game.game_selected_object import GameSelectedObject
from imperialism_remake.client.workforce.workforce_geologist import WorkforceGeologist
from imperialism_remake.client.workforce.workforce_widget import WorkforceWidget
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.client.workforce.workforce_engineer import WorkforceEngineer

logger = logging.getLogger(__name__)


class GameMainScreen(GenericScreen):
    """
        The whole screen (layout of single elements and interactions.
    """

    def __init__(self, client, scenario_file, selected_nation):
        logger.debug('create scenario_file:%s, selected_nation:%s', scenario_file, selected_nation)

        self.scenario = GameScenario()

        main_map = MainMap(self.scenario)
        main_map.mouse_press_event.connect(self._main_map_mouse_press_event)

        super().__init__(client, self.scenario, main_map)

        self.scenario.load(scenario_file)

        self._selected_object = GameSelectedObject(self.info_panel)

        # !!! TODO this is just to test, remove me a little bit later!!!
        workforce_engineer01 = WorkforceEngineer(self.scenario.server_scenario, uuid.uuid4(), 4, 13)
        workforce_engineer01_widget = WorkforceWidget(main_map, self.info_panel, workforce_engineer01)
        workforce_engineer01_widget.plan_action(4, 13, WorkforceAction.STAND)

        workforce_engineer01_widget.event_widget_selected.connect(self._selected_object.select_widget_object)

        workforce_geologist01 = WorkforceGeologist(self.scenario.server_scenario, uuid.uuid4(), 8, 11)
        workforce_geologist01_widget = WorkforceWidget(main_map, self.info_panel, workforce_geologist01)
        workforce_geologist01_widget.plan_action(8, 11, WorkforceAction.STAND)

        workforce_geologist01_widget.event_widget_selected.connect(self._selected_object.select_widget_object)
        # !!! TODO remove above

    def _main_map_mouse_press_event(self, main_map, event: QtGui.QMouseEvent) -> None:
        scene_position = main_map.mapToScene(event.pos()) / constants.TILE_SIZE
        column, row = self.scenario.server_scenario.map_position(scene_position.x(), scene_position.y())

        logger.debug("mousePressEvent x:%s, y:%s, button:%s, row:%s, col:%s", event.x(), event.y(), event.button(), row, column)

        if event.button() == QtCore.Qt.LeftButton:
            logger.debug("mousePressEvent reset selected object and select other if it is there")
            self._selected_object.deselect_widget_object_rather_than(row, column)

        elif event.button() == QtCore.Qt.RightButton:
            logger.debug("mousePressEvent do duty action or nothing")

            # TODO if this row and col is busy with other object -> do nothing
            # if scenario has object(workforce) in row, col for this x, y
            # then do nothing
            self._selected_object.do_action(row, column)

