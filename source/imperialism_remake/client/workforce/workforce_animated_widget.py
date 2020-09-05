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
from imperialism_remake.client.utils import scene_utils
from imperialism_remake.lib.blinking_animated_widget import BlinkingAnimatedWidget
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.client.workforce.workforce_common import WorkforceCommon

logger = logging.getLogger(__name__)


class WorkforceAnimatedWidget(BlinkingAnimatedWidget):
    event_widget_selected = QtCore. pyqtSignal(object)

    def __init__(self, main_map, info_panel: InfoPanel, workforce_common: WorkforceCommon):
        super().__init__()

        self.setStyleSheet("background-color: rgba(0,0,0,0%)")

        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)

        self._info_panel = info_panel
        self._workforce_common = workforce_common
        self._scenario = main_map.scenario
        self._scene = main_map.scene

        self._item = self._scene.addWidget(self)
        self._item.setZValue(10)

        pixmap_stand = self._scenario.get_workforce_to_texture_mapper().get_pixmap_of_type(
            self._workforce_common.get_type().value,
            WorkforceAction.STAND)
        self.setPixmap(pixmap_stand)

        pixmaps_duty_action = self._scenario.get_workforce_to_texture_mapper().get_pixmap_of_type(
            self._workforce_common.get_type().value,
            WorkforceAction.DUTY_ACTION)
        self.add_animation_pixmaps(pixmaps_duty_action)

    def _display(self):
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

    def plan_action(self, new_row: int, new_column: int, workforce_action: WorkforceAction):
        logger.debug("plan_action id:%s, type:%s, new_row:%s, new_column:%s, workforce_action:%s",
                     self._workforce_common.get_id(),
                     self._workforce_common.get_type(), new_row, new_column, workforce_action)

        self._workforce_common.plan_action(new_row, new_column, workforce_action)

        self._display()

    def cancel_action(self):
        logger.debug("cancel_action id:%s, type:%s", self._workforce_common.get_id(), self._workforce_common.get_type())

        self._workforce_common.cancel_action()

        self._display()

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction):
        return self._workforce_common.is_action_allowed(new_row, new_column, workforce_action)

    def get_workforce(self):
        return self._workforce_common

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        logger.debug("mousePressEvent id:%s, type:%s", self._workforce_common.get_id(), self._workforce_common.get_type())

        if event.button() == QtCore.Qt.LeftButton:
            self.event_widget_selected.emit(self)

        super().mousePressEvent(event)

    def enterEvent(self, event: QtCore.QEvent) -> None:
        logger.debug("enterEvent id:%s, type:%s", self._workforce_common.get_id(), self._workforce_common.get_type())

        self._info_panel.update_workforce_info(self._workforce_common.get_name())

        super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:
        logger.debug("leaveEvent id:%s, type:%s", self._workforce_common.get_id(), self._workforce_common.get_type())

        self._info_panel.update_workforce_info(None)

        super().leaveEvent(event)
