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

from imperialism_remake.client.common.generic_screen import GenericScreen
from imperialism_remake.client.common.mainmap import MainMap
from imperialism_remake.client.game.game_scenario import GameScenario

logger = logging.getLogger(__name__)


class GameMainScreen(GenericScreen):
    """
        The whole screen (layout of single elements and interactions.
    """

    def __init__(self, client, scenario_file, selected_nation):
        logger.debug('create scenario_file:%s, selected_nation:%s', scenario_file, selected_nation)

        self.scenario = GameScenario()

        super().__init__(client, self.scenario, MainMap(self.scenario))

        self.scenario.load(scenario_file)
