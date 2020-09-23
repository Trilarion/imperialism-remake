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

"""
GUI and internal working of the scenario editor. This is also partly of the client but since the client should not
know anything about the scenario, we put it in the server module.
"""
import logging

from PyQt5 import QtCore

from imperialism_remake.client.graphics.mappers.structure_type_to_pixmap_mapper import StructureTypeToPixmapMapper
from imperialism_remake.client.graphics.mappers.terrain_resource_to_pixmap_mapper import TerrainResourceToPixmapMapper
from imperialism_remake.client.graphics.mappers.terrain_type_to_pixmap_mapper import TerrainTypeToPixmapMapper
from imperialism_remake.client.graphics.mappers.workforce_to_pixmap_mapper import WorkforceToTextureMapper

logger = logging.getLogger(__name__)


class GenericScenario(QtCore.QObject):
    #: signal, scenario has changed completely
    scenario_changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.server_scenario = None

        self._terrain_type_to_pixmap_mapper = None
        self._workforce_to_texture_mapper = None

        logger.debug("__init__")

    def _init(self):
        logger.debug("_init")

        self._terrain_type_to_pixmap_mapper = TerrainTypeToPixmapMapper(self.server_scenario)
        self._workforce_to_texture_mapper = WorkforceToTextureMapper(self.server_scenario)
        self._terrain_resource_to_pixmap_mapper = TerrainResourceToPixmapMapper(self.server_scenario)
        self._structure_type_to_pixmap_mapper = StructureTypeToPixmapMapper(self.server_scenario)

        # emit that everything has changed
        self.scenario_changed.emit()

    def get_terrain_type_to_pixmap_mapper(self):
        return self._terrain_type_to_pixmap_mapper

    def get_terrain_resource_to_pixmap_mapper(self):
        return self._terrain_resource_to_pixmap_mapper

    def get_workforce_to_texture_mapper(self):
        return self._workforce_to_texture_mapper

    def get_structure_type_to_pixmap_mapper(self):
        return self._structure_type_to_pixmap_mapper
