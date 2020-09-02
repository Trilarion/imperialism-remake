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
from imperialism_remake.server.models.workforce import Workforce


class NationAsset:
    def __init__(self, nation_id):
        self._nation_id = nation_id

        self._workforces = {}
        self._raw_resources = {}
        self._processed_resources = {}

    def get_id(self):
        return self._nation_id

    def add_workforce(self, workforce: Workforce):
        if self._workforces.get(workforce.get_id()):
            raise Exception("Nation has already this worker")

        self._workforces[workforce.get_id()] = workforce

    def get_workforces(self):
        return self._workforces
