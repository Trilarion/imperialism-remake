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
    ROAD_THROUGH_HILLS = 1
    ROAD_THROUGH_MOUNTAINS = 2
    ROAD_THROUGH_SWAMP = 3
    ROAD_THROUGH_PLAINS = 4
    PROSPECTOR_WORK_MOUNTAIN = 5
    PROSPECTOR_WORK_SWAMP = 6
    PROSPECTOR_WORK_HILLS = 7
    PROSPECTOR_WORK_DESERT = 8
    PROSPECTOR_WORK_TUNDRA = 9
    FORESTER_FOREST_LEVEL1 = 10
    FORESTER_FOREST_LEVEL2 = 11
    FORESTER_FOREST_LEVEL3 = 12
    FARMER_ORCHARD_LEVEL1 = 13
    FARMER_ORCHARD_LEVEL2 = 14
    FARMER_ORCHARD_LEVEL3 = 15
    FARMER_GRAIN_LEVEL1 = 16
    FARMER_GRAIN_LEVEL2 = 17
    FARMER_GRAIN_LEVEL3 = 18
    FARMER_COTTON_LEVEL1 = 19
    FARMER_COTTON_LEVEL2 = 20
    FARMER_COTTON_LEVEL3 = 21
    MINER_MINE_LEVEL1 = 22
    MINER_MINE_LEVEL2 = 23
    MINER_MINE_LEVEL3 = 24
    DRILLER_DERRICK_LEVEL1 = 25
    DRILLER_DERRICK_LEVEL2 = 26
    DRILLER_DERRICK_LEVEL3 = 27
    RANCHER_RANCH_LEVEL1 = 28
    RANCHER_RANCH_LEVEL2 = 29
    RANCHER_RANCH_LEVEL3 = 30
