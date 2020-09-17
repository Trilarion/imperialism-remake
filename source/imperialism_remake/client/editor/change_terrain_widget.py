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

from imperialism_remake.client.editor.change_texture_widget import ChangeTextureWidget

logger = logging.getLogger(__name__)


class ChangeTerrainWidget(ChangeTextureWidget):
    def __init__(self, screen, column, row):
        super().__init__(screen.main_map, column, row, screen.scenario.server_scenario.get_terrain_settings(),
                         screen.scenario.get_terrain_type_to_pixmap_mapper(),
                         screen.scenario.server_scenario.set_terrain_at)

    def mousePressEvent(self, event):
        logger.debug("mousePressEvent x:%s, y:%s", event.x(), event.y())

        self._fill_texture(event.x(), event.y())
