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

from imperialism_remake.server.models.turn_planned import TurnPlanned
from imperialism_remake.server.models.workforce import Workforce
from imperialism_remake.server.models.workforce_type import WorkforceType
from imperialism_remake.server.server_scenario import ServerScenario
from imperialism_remake.server.workforce.workforce_common import WorkforceCommon
from imperialism_remake.server.workforce.workforce_engineer import WorkforceEngineer
from imperialism_remake.server.workforce.workforce_farmer import WorkforceFarmer
from imperialism_remake.server.workforce.workforce_forester import WorkforceForester
from imperialism_remake.server.workforce.workforce_miner import WorkforceMiner
from imperialism_remake.server.workforce.workforce_prospector import WorkforceProspector


class WorkforceFactory:
    @staticmethod
    def create_new_workforce(server_scenario: ServerScenario, turn_planned: TurnPlanned,
                             workforce: Workforce) -> WorkforceCommon:
        if workforce.get_type() == WorkforceType.PROSPECTOR:
            return WorkforceProspector(server_scenario, turn_planned, workforce)
        elif workforce.get_type() == WorkforceType.ENGINEER:
            return WorkforceEngineer(server_scenario, turn_planned, workforce)
        elif workforce.get_type() == WorkforceType.FORESTER:
            return WorkforceForester(server_scenario, turn_planned, workforce)
        elif workforce.get_type() == WorkforceType.FARMER:
            return WorkforceFarmer(server_scenario, turn_planned, workforce)
        elif workforce.get_type() == WorkforceType.MINER:
            return WorkforceMiner(server_scenario, turn_planned, workforce)
