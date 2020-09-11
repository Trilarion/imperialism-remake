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


class WorkforceToTextureMapper:
    def __init__(self, server_scenario):
        super().__init__()

        workforce_settings = server_scenario.get_workforce_settings()

        self.pixmaps_stand = {}
        self.pixmaps_on_duty = {}
        for workforce_type in workforce_settings:
            pixmap_stand = QtGui.QPixmap(
                constants.extend(constants.GRAPHICS_WORKFORCE_FOLDER,
                                 workforce_settings[workforce_type]['texture_filename_stand']))
            self.pixmaps_stand[workforce_type] = pixmap_stand.scaled(constants.WORKFORCE_SIZE[0],
                                                                     constants.WORKFORCE_SIZE[1])

            duty_image = QtGui.QImage(constants.extend(constants.GRAPHICS_WORKFORCE_FOLDER,
                                                       workforce_settings[workforce_type]['texture_filename_on_duty']))

            # must be sure that sprite is divided evenly
            hor_count = int(duty_image.width() / constants.WORKFORCE_SIZE[0])
            ver_count = int(duty_image.height() / constants.WORKFORCE_SIZE[1])
            width = constants.WORKFORCE_SIZE[0]
            height = constants.WORKFORCE_SIZE[1]
            self.pixmaps_on_duty[workforce_type] = [
                QtGui.QPixmap.fromImage(duty_image.copy(row * height, col * width, width, height)).scaled(
                    constants.WORKFORCE_SIZE[0],
                    constants.WORKFORCE_SIZE[1]) for row
                in range(hor_count) for col in range(ver_count)]

    def get_pixmap_of_type(self, workforce_type: int, action):
        if workforce_type >= len(self.pixmaps_stand):
            raise RuntimeError('Tile type undefined: %s', workforce_type)

        if action == WorkforceAction.DUTY_ACTION:
            return self.pixmaps_on_duty[workforce_type]
        else:
            return self.pixmaps_stand[workforce_type]
