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
from imperialism_remake.server.model.workforce_action import WorkforceAction

logger = logging.getLogger(__name__)


class WorkforceToTextureMapper:
    def __init__(self, server_scenario):
        super().__init__()

        workforce_settings = server_scenario.get_workforce_settings()

        self.pixmaps_stand = {}
        self.pixmaps_busy = {}
        for workforce_type in workforce_settings:
            pixmap_stand = QtGui.QPixmap(
                constants.extend(constants.GRAPHICS_WORKFORCE_FOLDER, workforce_settings[workforce_type]['texture_filename_stand']))
            self.pixmaps_stand[workforce_type] = pixmap_stand.scaled(constants.TILE_SIZE, constants.TILE_SIZE)

            pixmap_busy = QtGui.QPixmap(
                constants.extend(constants.GRAPHICS_WORKFORCE_FOLDER, workforce_settings[workforce_type]['texture_filename_in_action']))
            self.pixmaps_busy[workforce_type] = pixmap_busy.scaled(constants.TILE_SIZE, constants.TILE_SIZE)

    def get_pixmap_of_type(self, workforce_type: int, action):
        if workforce_type >= len(self.pixmaps_stand):
            raise RuntimeError('Tile type undefined: %s', workforce_type)

        if action == WorkforceAction.DUTY_ACTION:
            return self.pixmaps_busy[workforce_type]
        else:
            return self.pixmaps_stand[workforce_type]
