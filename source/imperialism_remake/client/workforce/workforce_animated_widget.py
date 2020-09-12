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

from PyQt5 import QtGui, QtCore

from imperialism_remake.client.common.info_panel import InfoPanel
from imperialism_remake.client.common.main_map import MainMap
from imperialism_remake.client.graphics.mappers.workforce_to_action_cursor_mapper import WorkforceToActionCursorMapper
from imperialism_remake.client.utils import scene_utils
from imperialism_remake.lib.blinking_animated_widget import BlinkingAnimatedWidget
from imperialism_remake.server.models.workforce import Workforce
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.workforce.workforce_common import WorkforceCommon

logger = logging.getLogger(__name__)


class WorkforceAnimatedWidget(BlinkingAnimatedWidget):
    event_widget_selected = QtCore.pyqtSignal(object)
    event_widget_deselected = QtCore.pyqtSignal(object)

    def __init__(self, main_map: MainMap, info_panel: InfoPanel, workforce_common: WorkforceCommon):
        super().__init__(main_map.scenario.get_workforce_to_texture_mapper().get_pixmap_of_type(
            workforce_common.get_type().value,
            WorkforceAction.STAND))

        self.setMouseTracking(True)

        self.setStyleSheet("background-color: rgba(0,0,0,0%)")

        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)

        self._info_panel = info_panel
        self._workforce_common = workforce_common
        self._scenario = main_map.scenario
        self._scene = main_map.scene

        self._item = self._scene.addWidget(self)
        self._item.setZValue(10)

        pixmaps_duty_action = self._scenario.get_workforce_to_texture_mapper().get_pixmap_of_type(
            self._workforce_common.get_type().value,
            WorkforceAction.DUTY_ACTION)
        self.add_animation_pixmaps(pixmaps_duty_action)

        self._workforce_to_action_icon_mapper = WorkforceToActionCursorMapper(main_map.scenario.server_scenario)

    def _display(self) -> None:
        if self._workforce_common.get_action() == WorkforceAction.DUTY_ACTION or self._workforce_common.get_action() == WorkforceAction.MOVE:
            row, column = self._workforce_common.get_new_position()
        else:
            row, column = self._workforce_common.get_current_position()

        logger.debug("_display row:%s, col:%s", row, column)

        scene_utils.put_widget_in_tile_center(self, row, column)

        if self._workforce_common.get_action() == WorkforceAction.DUTY_ACTION:
            self.start_animation()
        else:
            self.stop_animation()

    def plan_action(self, new_row: int, new_column: int, workforce_action: WorkforceAction) -> None:
        logger.debug("plan_action id:%s, type:%s, new_row:%s, new_column:%s, workforce_action:%s",
                     self._workforce_common.get_id(),
                     self._workforce_common.get_type(), new_row, new_column, workforce_action)

        self._workforce_common.plan_action(new_row, new_column, workforce_action)

        self._display()

    def cancel_action(self) -> None:
        logger.debug("cancel_action id:%s, type:%s", self._workforce_common.get_id(), self._workforce_common.get_type())

        self._workforce_common.cancel_action()

        self._display()

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction) -> bool:
        return self._workforce_common.is_action_allowed(new_row, new_column, workforce_action)

    def get_workforce(self) -> Workforce:
        return self._workforce_common

    def get_workforce_to_action_cursor(self, new_row: int, new_column: int) -> QtGui.QCursor:
        if self.is_action_allowed(new_row, new_column, WorkforceAction.DUTY_ACTION):
            cursor = self._workforce_to_action_icon_mapper.get_cursor_of_type(
                self._workforce_common.get_type(),
                WorkforceAction.DUTY_ACTION)
            logger.debug("get_workforce_to_action_pixmap new_row:%s, new_column:%s, workforce type:%s, action:%s",
                         new_row,
                         new_column, self._workforce_common.get_type(), WorkforceAction.DUTY_ACTION)
        elif self.is_action_allowed(new_row, new_column, WorkforceAction.MOVE):
            cursor = self._workforce_to_action_icon_mapper.get_cursor_of_type(
                self._workforce_common.get_type(),
                WorkforceAction.MOVE)
            logger.debug("get_workforce_to_action_pixmap new_row:%s, new_column:%s, workforce type:%s, action:%s",
                         new_row,
                         new_column, self._workforce_common.get_type(), WorkforceAction.MOVE)
        else:
            cursor = self._workforce_to_action_icon_mapper.get_cursor_not_allowed_of_type(
                self._workforce_common.get_type())
            logger.debug("get_workforce_to_action_pixmap new_row:%s, new_column:%s, workforce type:%s, action:%s",
                         new_row,
                         new_column, self._workforce_common.get_type(), "not allowed")

        return cursor

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        logger.debug("mousePressEvent id:%s, type:%s", self._workforce_common.get_id(),
                     self._workforce_common.get_type())

        if event.button() == QtCore.Qt.LeftButton:
            self.event_widget_selected.emit(self)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        super().enterEvent(event)
        logger.debug("enterEvent id:%s, type:%s", self._workforce_common.get_id(), self._workforce_common.get_type())

        self._info_panel.update_workforce_info(self._workforce_common.get_name())

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        super().leaveEvent(event)
        logger.debug("leaveEvent id:%s, type:%s", self._workforce_common.get_id(), self._workforce_common.get_type())

        self._info_panel.update_workforce_info(None)

