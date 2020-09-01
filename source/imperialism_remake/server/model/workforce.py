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
import uuid

from imperialism_remake.server.model.workforce_action import WorkforceAction
from imperialism_remake.server.model.workforce_type import WorkforceType


class Workforce:
    def __init__(self, workforce_id, row, column, workforce_type: WorkforceType):
        self._workforce_id = workforce_id
        self._workforce_type = workforce_type
        self._workforce_action = WorkforceAction.STAND

        self._row = row
        self._column = column
        self._new_row = None
        self._new_column = None

        # Overriden in inherited workforce class implementations
        self._build_expenses = None

    def get_id(self):
        return self._workforce_id

    def get_type(self):
        return self._workforce_type

    def get_action(self):
        return self._workforce_action

    def get_new_position(self):
        return self._new_row, self._new_column

    def get_current_position(self):
        return self._row, self._column

    def plan_action(self, new_row: int, new_column: int, workforce_action: WorkforceAction):
        self._workforce_action = workforce_action
        self._new_row = new_row
        self._new_column = new_column

    def cancel_action(self):
        self._workforce_action = WorkforceAction.STAND
        self._new_row = self._row
        self._new_column = self._column



