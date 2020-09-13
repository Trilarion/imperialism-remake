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

from imperialism_remake.server.models.turn import Turn
from imperialism_remake.server.workforce.workforce_factory import WorkforceFactory

logger = logging.getLogger(__name__)


class TurnManager(QtCore.QObject):
    event_turn_completed = QtCore.pyqtSignal(Turn)

    def __init__(self, scenario):
        super().__init__()

        self._scenario = scenario
        self._turn = Turn()

    def get_turn(self) -> Turn:
        return self._turn

    def make_turn(self) -> None:
        logger.debug("make_turn start")

        logger.debug("send next planned state for workforces: %s", self._turn.get_workforces())
        # TODO send planned actions and other stuff to server and emit event once response is received
        time.sleep(2)

        # TODO this is just for test. It is server action simulation and MUST be removed a little bit later
        old_workforces = self._turn.get_workforces()
        del self._turn
        self._turn = Turn()
        for k, w in old_workforces.items():
            r, c = w.get_new_position()
            workforce = WorkforceFactory.create_new_workforce(self._scenario.server_scenario, self._turn, w.get_id(),
                                                              r, c, w.get_type())
            self._turn.add_workforce(workforce)
        # end of TODO

        self.event_turn_completed.emit(self._turn)
        logger.debug("make_turn completed")
