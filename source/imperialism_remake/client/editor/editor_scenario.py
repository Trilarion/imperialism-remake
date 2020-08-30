# Imperialism remake
# Copyright (C) 2014-16 Trilarion
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

from imperialism_remake.client.common.generic_scenario import GenericScenario

logger = logging.getLogger(__name__)


class EditorScenario(GenericScenario):
    """
    Wrap around the Scenario file to get notified of recreations
    """

    def __init__(self):
        super().__init__()
