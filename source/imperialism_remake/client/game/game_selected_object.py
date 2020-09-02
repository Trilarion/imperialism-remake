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

logger = logging.getLogger(__name__)


class GameSelectedObject:
    def __init__(self):
        self._selected_object = None

    def select_object(self, selected_object):
        self._selected_object = selected_object

        logger.debug("set_selected_object id:%s, type:%s", selected_object.get_id(), selected_object.get_type())

    def deselect_object(self):
        self._selected_object = None

        logger.debug("clear_selected_object")
