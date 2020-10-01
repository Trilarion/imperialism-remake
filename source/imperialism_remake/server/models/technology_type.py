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
    ROAD_THROUGH_DESERT = 5
    ROAD_THROUGH_TUNDRA = 6
    PROSPECTOR_WORK_MOUNTAIN = 7
    PROSPECTOR_WORK_SWAMP = 8
    PROSPECTOR_WORK_HILLS = 9
    PROSPECTOR_WORK_DESERT = 10
    PROSPECTOR_WORK_TUNDRA = 11
    FORESTER_FOREST_LEVEL1 = 12
    FORESTER_FOREST_LEVEL2 = 13
    FORESTER_FOREST_LEVEL3 = 14
    FARMER_ORCHARD_LEVEL1 = 15
    FARMER_ORCHARD_LEVEL2 = 16
    FARMER_ORCHARD_LEVEL3 = 17
    FARMER_GRAIN_LEVEL1 = 18
    FARMER_GRAIN_LEVEL2 = 19
    FARMER_GRAIN_LEVEL3 = 20
    FARMER_COTTON_LEVEL1 = 21
    FARMER_COTTON_LEVEL2 = 22
    FARMER_COTTON_LEVEL3 = 23
    MINER_MINE_LEVEL1 = 24
    MINER_MINE_LEVEL2 = 25
    MINER_MINE_LEVEL3 = 26
    DRILLER_DERRICK_LEVEL1 = 27
    DRILLER_DERRICK_LEVEL2 = 28
    DRILLER_DERRICK_LEVEL3 = 29
    RANCHER_LIVESTOCK_LEVEL1 = 30
    RANCHER_LIVESTOCK_LEVEL2 = 31
    RANCHER_LIVESTOCK_LEVEL3 = 32
    RANCHER_WOOL_LEVEL1 = 33
    RANCHER_WOOL_LEVEL2 = 34
    RANCHER_WOOL_LEVEL3 = 35
