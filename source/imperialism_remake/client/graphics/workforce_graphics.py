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

from PyQt5 import QtWidgets, QtGui, QtCore

from imperialism_remake.client.utils import scene_utils
from imperialism_remake.server.model.workforce_action import WorkforceAction
from imperialism_remake.server.model.workforce_impl.workforce_common import WorkforceCommon

logger = logging.getLogger(__name__)


class WorkforceGraphics(QtWidgets.QLabel):
    def __init__(self, main_map, workforce: WorkforceCommon):
        super().__init__()

        self.setStyleSheet("background-color: rgba(0,0,0,0%)")

        self.setWindowFlags(QtCore.Qt.Popup | QtCore.Qt.FramelessWindowHint)

        self._workforce = workforce
        self._scenario = main_map.scenario
        self._scene = main_map.scene

    def _display(self):
        if self._workforce.get_action() == WorkforceAction.DUTY_ACTION or self._workforce.get_action() == WorkforceAction.MOVE:
            row, column = self._workforce.get_new_position()
        else:
            row, column = self._workforce.get_current_position()

        # add workforce pixmap to myself (I am label) and display in scene
        self.setPixmap(self._scenario.get_workforce_to_texture_mapper().get_pixmap_of_type(
            self._workforce.get_type().value,
            self._workforce.get_action()))

        scene_utils.put_label_in_tile_center(self._scene, self, row, column, 10)

    def plan_action(self, new_row: int, new_column: int, workforce_action: WorkforceAction):
        logger.debug("plan_action id:%s, type:%s, new_row:%s, new_column:%s, workforce_action:%s",
                     self._workforce.get_id(),
                     self._workforce.get_type(), new_row, new_column, workforce_action)

        self._workforce.plan_action(new_row, new_column, workforce_action)

        self._display()

    def cancel_action(self):
        logger.debug("cancel_action id:%s, type:%s", self._workforce.get_id(), self._workforce.get_type())

        self._workforce.cancel_action()

        self._display()

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction):
        return self._workforce.is_action_allowed(new_row, new_column, workforce_action)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)

        logger.debug("mousePressEvent id:%s, type:%s, ev:%s", self._workforce.get_id(), self._workforce.get_type(),
                     event)

    # TODO How to detect outside mouse click event ?
