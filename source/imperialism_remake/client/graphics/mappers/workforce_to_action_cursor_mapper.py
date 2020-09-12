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

from PyQt5 import QtGui

from imperialism_remake.base import constants
from imperialism_remake.server.models.workforce_action import WorkforceAction

logger = logging.getLogger(__name__)


class WorkforceToActionCursorMapper:
    def __init__(self, server_scenario):
        super().__init__()

        self._cursors = {}
        self._cursor_not_allowed = {}

        workforce_action_cursor_settings = server_scenario.get_workforce_action_cursor_settings()
        for workforce_type in workforce_action_cursor_settings:
            if workforce_type not in self._cursors:
                self._cursors[workforce_type] = {}

            self._cursors[workforce_type][WorkforceAction.MOVE] = QtGui.QCursor(QtGui.QPixmap(
                constants.extend(constants.GRAPHICS_MAP_ICON_FOLDER,
                                 workforce_action_cursor_settings[workforce_type]['workforce_action_cursor_move'])))
            self._cursors[workforce_type][WorkforceAction.DUTY_ACTION] = QtGui.QCursor(QtGui.QPixmap(
                constants.extend(constants.GRAPHICS_MAP_ICON_FOLDER,
                                 workforce_action_cursor_settings[workforce_type][
                                     'workforce_action_cursor_duty_action'])))
            self._cursor_not_allowed[workforce_type] = QtGui.QCursor(QtGui.QPixmap(
                constants.extend(constants.GRAPHICS_MAP_ICON_FOLDER,
                                 workforce_action_cursor_settings[workforce_type][
                                     'workforce_action_cursor_not_allowed'])))

    def get_cursor_of_type(self, workforce_type: int, action: WorkforceAction):
        return self._cursors[workforce_type][action]

    def get_cursor_not_allowed_of_type(self, workforce_type: int):
        return self._cursor_not_allowed[workforce_type]
