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
from enum import Enum


class TechnologyType(Enum):
    ROAD_THROUGH_HILLS = 0
    ROAD_THROUGH_MOUNTAINS = 1
    ROAD_THROUGH_SWAMP = 2
    ROAD_THROUGH_PLAINS = 3
    GEOLOGY_WORK_MOUNTAIN = 4
    GEOLOGY_WORK_SWAMP = 5
    GEOLOGY_WORK_HILLS = 6
    FORESTER_WORK_FOREST = 7
    FORESTER_WORK_SCHRUBFOREST = 8
    FARMER_WORK_ORCHARD = 9
    FARMER_WORK_GRAIN = 10
    FARMER_WORK_COTTON = 11
