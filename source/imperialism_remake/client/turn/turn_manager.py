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
import time

from PyQt5 import QtCore

from imperialism_remake.server.models.turn_planned import TurnPlanned
from imperialism_remake.server.models.turn_result import TurnResult
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.models.workforce_type import WorkforceType
from imperialism_remake.server.workforce.workforce_factory import WorkforceFactory

logger = logging.getLogger(__name__)


class TurnManager(QtCore.QObject):
    event_turn_completed = QtCore.pyqtSignal(TurnResult)

    def __init__(self, scenario):
        super().__init__()

        self._scenario = scenario
        self._turn_planned = TurnPlanned()

    def get_turn_planned(self) -> TurnPlanned:
        return self._turn_planned

    def make_turn(self) -> None:
        logger.debug("make_turn start")

        logger.debug("send next planned state for workforces: %s", self._turn_planned.get_workforces())
        # TODO send planned actions and other stuff to server and emit event once response is received
        time.sleep(1)

        # TODO this is just for test. It is server action simulation and MUST be removed a little bit later
        old_workforces = self._turn_planned.get_workforces()
        del self._turn_planned
        self._turn_planned = TurnPlanned()

        turn_result = TurnResult()
        for k, w in old_workforces.items():
            r, c = w.get_new_position()
            workforce = WorkforceFactory.create_new_workforce(self._scenario.server_scenario, self._turn_planned,
                                                              w.get_id(),
                                                              r, c, w.get_type())
            self._turn_planned.add_workforce(workforce)

            turn_result._workforces[workforce.get_id()] = workforce

            old_r, old_c = w.get_current_position()
            if w.get_action() == WorkforceAction.DUTY_ACTION and w.get_type() == WorkforceType.ENGINEER and (
                    old_r != r or old_c != c):
                self._scenario.server_scenario.add_road((r, c), (old_r, old_c))

                turn_result._roads.append(((r, c), (old_r, old_c)))
        # end of TODO

        self.event_turn_completed.emit(turn_result)
        logger.debug("make_turn completed")
