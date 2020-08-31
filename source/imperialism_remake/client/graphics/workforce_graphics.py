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
from imperialism_remake.client.graphics.mappers.workforce_to_texture_mapper import WorkforceToTextureMapper
from imperialism_remake.client.utils import scene_utils
from imperialism_remake.server.model.workforce_action import WorkforceAction
from imperialism_remake.server.model.workforce_impl.workforce_common import WorkforceCommon


#TODO make this a clickable QT object to track click and cursor move to neighbour map cell
class WorkforceGraphics:
    def __init__(self, main_map, workforce: WorkforceCommon):
        self._workforce = workforce
        self._scenario = main_map.scenario
        self._scene = main_map.scene

    def _display(self):
        if self._workforce.get_action() == WorkforceAction.DUTY_ACTION or self._workforce.get_action() == WorkforceAction.MOVE:
            row, column = self._workforce.get_new_position()
        else:
            row, column = self._workforce.get_new_position()

        # TODO make WorkforceToTextureMapper as singleton
        scene_utils.put_pixmap_in_tile_center(self._scene, WorkforceToTextureMapper(self._scenario).get_pixmap_of_type(
            self._workforce.get_type().value,
            self._workforce.get_action()), row, column, 10)

    def plan_action(self, new_row: int, new_column: int, workforce_action: WorkforceAction):
        self._workforce.plan_action(new_row, new_column, workforce_action)

        self._display()

    def cancel_action(self):
        self._workforce.cancel_action()

        self._display()

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction):
        return self._workforce.is_action_allowed(new_row, new_column, workforce_action)
