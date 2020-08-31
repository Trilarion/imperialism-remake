# Imperialism remake
# Copyright (C) 2015-16 Trilarion
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
The main game screen.
"""
import logging
import uuid

from imperialism_remake.client.common.generic_screen import GenericScreen
from imperialism_remake.client.common.mainmap import MainMap
from imperialism_remake.client.game.game_scenario import GameScenario
from imperialism_remake.client.graphics.workforce_graphics import WorkforceGraphics
from imperialism_remake.server.model.workforce_action import WorkforceAction
from imperialism_remake.server.model.workforce_impl.workforce_engineer import WorkforceEngineer
from imperialism_remake.server.model.workforce_type import WorkforceType

logger = logging.getLogger(__name__)


class GameMainScreen(GenericScreen):
    """
        The whole screen (layout of single elements and interactions.
    """

    def __init__(self, client, scenario_file, selected_nation):
        logger.debug('create scenario_file:%s, selected_nation:%s', scenario_file, selected_nation)

        self.scenario = GameScenario()

        main_map = MainMap(self.scenario)

        super().__init__(client, self.scenario, main_map)

        self.scenario.load(scenario_file)

        # TODO this is just to test, remove me!!!
        workforce_engineer01 = WorkforceEngineer(self.scenario.server_scenario, uuid.uuid4(), 5, 5)
        workforce_engineer01_graphics = WorkforceGraphics(main_map, workforce_engineer01)
        workforce_engineer01_graphics.plan_action(5, 5, WorkforceAction.STAND)
