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
import os

from PyQt5 import QtCore

from imperialism_remake.base import constants
from imperialism_remake.lib import utils
from imperialism_remake.server.server_scenario import ServerScenario

logger = logging.getLogger(__name__)


class GenericScenario(QtCore.QObject):
    #: signal, scenario has changed completely
    changed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.server_scenario = None

    def load(self, file_name):
        """
        :param file_name:
        """
        logger.debug('load file_name:%s', file_name)

        if os.path.isfile(file_name):
            self.server_scenario = ServerScenario.from_file(file_name)
            self.changed.emit()

    def create(self, properties):
        """
        Create new scenario (from the create new scenario dialog).

        :param properties:
        """
        logger.debug('create properties:%s', properties)

        self.server_scenario = ServerScenario()
        self.server_scenario[constants.ScenarioProperty.TITLE] = properties[constants.ScenarioProperty.TITLE]
        self.server_scenario.create_empty_map(properties[constants.ScenarioProperty.MAP_COLUMNS],
                                              properties[constants.ScenarioProperty.MAP_ROWS])

        # standard rules
        self.server_scenario[constants.ScenarioProperty.RULES] = 'standard.rules'
        # self.scenario.load_rules()
        # TODO rules as extra?
        rule_file = constants.extend(constants.SCENARIO_RULESET_FOLDER,
                                     self.server_scenario[constants.ScenarioProperty.RULES])
        self.server_scenario._rules = utils.read_from_file(rule_file)

        # emit that everything has changed
        self.changed.emit()
