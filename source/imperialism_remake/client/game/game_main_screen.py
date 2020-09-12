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
from imperialism_remake.client.workforce.workforce_animated_widget import WorkforceAnimatedWidget
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.workforce.workforce_engineer import WorkforceEngineer
from imperialism_remake.server.workforce.workforce_geologist import WorkforceGeologist

logger = logging.getLogger(__name__)


class GameMainScreen(GenericScreen):
    """
        The whole screen (layout of single elements and interactions.
    """

    def __init__(self, client, scenario_file, selected_nation):
        logger.debug('create scenario_file:%s, selected_nation:%s', scenario_file, selected_nation)

        self.scenario = GameScenario()

        main_map = MainMap(self.scenario)

        super().__init__(client, self.scenario, main_map)

        self.scenario.load(scenario_file)

        self._selected_object = GameSelectedObject(self._info_panel)

        self._default_cursor = self.main_map.viewport().cursor()

        main_map.mouse_press_event.connect(self._main_map_mouse_press_event)
        main_map.mouse_move_event.connect(self._main_map_mouse_move_event)

        # !!! TODO this is just to test, remove me a little bit later!!!
        workforce_engineer01 = WorkforceEngineer(self.scenario.server_scenario, uuid.uuid4(), 4, 13)
        workforce_engineer01_widget = WorkforceAnimatedWidget(main_map, self._info_panel, workforce_engineer01)
        workforce_engineer01_widget.plan_action(4, 13, WorkforceAction.STAND)

        workforce_engineer01_widget.event_widget_selected.connect(self._selected_widget_object_event)
        workforce_engineer01_widget.event_widget_deselected.connect(self._deselected_widget_object_event)

        workforce_geologist01 = WorkforceGeologist(self.scenario.server_scenario, uuid.uuid4(), 8, 11)
        workforce_geologist01_widget = WorkforceAnimatedWidget(main_map, self._info_panel, workforce_geologist01)
        workforce_geologist01_widget.plan_action(8, 11, WorkforceAction.STAND)

        workforce_geologist01_widget.event_widget_selected.connect(self._selected_widget_object_event)
        workforce_geologist01_widget.event_widget_deselected.connect(self._deselected_widget_object_event)
        # !!! TODO remove above

    def _main_map_mouse_press_event(self, main_map, event: QtGui.QMouseEvent) -> None:
        scene_position = main_map.mapToScene(event.pos()) / constants.TILE_SIZE
        column, row = self.scenario.server_scenario.map_position(scene_position.x(), scene_position.y())

        logger.debug("_main_map_mouse_press_event x:%s, y:%s, button:%s, row:%s, col:%s", event.x(), event.y(),
                     event.button(), row,
                     column)

        if event.button() == QtCore.Qt.LeftButton:
            logger.debug("_main_map_mouse_press_event reset selected object and select other if it is there")
            self._selected_object.deselect_widget_object_rather_than(row, column)

        elif event.button() == QtCore.Qt.RightButton:
            logger.debug("_main_map_mouse_press_event do duty action or nothing")

            # TODO if this row and col is busy with other object -> do nothing
            # if scenario has object(workforce) in row, col for this x, y
            # then do nothing
            self._selected_object.do_action(row, column)

    def _main_map_mouse_move_event(self, column: int, row: int) -> None:
        self._update_cursor(row, column)

    def _update_cursor(self, row: int, column: int) -> None:
        if self._selected_object.is_selected():
            cursor = self._selected_object.get_workforce_to_action_cursor(row, column)

            if cursor is None:
                self._set_default_cursor()
            elif cursor != self.main_map.viewport().cursor():
                logger.debug("_update_cursor cursor changed cur_curs:%s, cursor:%s, row:%s, column:%s",
                             hex(id(self.main_map.viewport().cursor())), hex(id(cursor)), row, column)
                self.main_map.viewport().setCursor(cursor)
                # TODO should we change cursor when pointing workforce?
                # self._selected_object._selected_widget_object.setCursor(cursor)
        elif self._default_cursor != self.main_map.viewport().cursor():
            self._set_default_cursor()

    def _set_default_cursor(self):
        logger.debug("_set_default_cursor set default cursor")
        self.main_map.viewport().setCursor(self._default_cursor)

    def _selected_widget_object_event(self, widget_object: WorkforceAnimatedWidget) -> None:
        self._set_default_cursor()

        self._selected_object.select_widget_object(widget_object)

        row, col = widget_object.get_workforce().get_current_position()
        logger.debug("_selected_widget_object_event object type:%s, row:%s, col :%s",
                     widget_object.get_workforce().get_type(), row, col)

    def _deselected_widget_object_event(self, widget_object: WorkforceAnimatedWidget) -> None:
        logger.debug("_deselected_widget_object_event object type:%s", widget_object.get_workforce().get_type())
        self._set_default_cursor()
