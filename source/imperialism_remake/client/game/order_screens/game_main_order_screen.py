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

from PyQt5 import QtWidgets

from imperialism_remake.client.game.game_scenario import GameScenario

logger = logging.getLogger(__name__)


class GameMainOrderScreen(QtWidgets.QWidget):
    def __init__(self, scenario: GameScenario, client):
        super().__init__()

        self._scenario = scenario
        self._client = client

        logger.debug('__init__')
