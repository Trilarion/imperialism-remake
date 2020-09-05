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
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.client.workforce.workforce_common import WorkforceCommon
from imperialism_remake.server.models.workforce_type import WorkforceType


class WorkforceEngineer(WorkforceCommon):
    def __init__(self, server_scenario, workforce_id, row, column):
        super().__init__(server_scenario, workforce_id, row, column, WorkforceType.ENGINEER)

    def is_action_allowed(self, new_column, new_row, workforce_action: WorkforceAction):
        is_action_allowed = super().is_action_allowed(new_column, new_row, workforce_action)
        if not is_action_allowed:
            return False

        # TODO other specific rules for Engineer (e.g no building through Mountains/swamp if technology is not available yet)

        return True