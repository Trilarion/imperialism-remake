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

from imperialism_remake.client.common.info_panel import InfoPanel
from imperialism_remake.client.workforce.workforce_widget import WorkforceWidget
from imperialism_remake.server.models.workforce_action import WorkforceAction

logger = logging.getLogger(__name__)


class GameSelectedObject:
    def __init__(self, info_panel: InfoPanel):
        self._selected_widget_object = None
        self._info_panel = info_panel

    # TODO use for selected_widget_object common base class og objects, not only workforce
    def select_widget_object(self, selected_widget_object):
        self.deselect_widget_object_rather_than(-1, -1)

        self._selected_widget_object = selected_widget_object

        if isinstance(self._selected_widget_object, WorkforceWidget):
            logger.debug("set_selected_object id:%s, type:%s", selected_widget_object.get_workforce().get_id(),
                         selected_widget_object.get_workforce().get_type())

            self._info_panel.update_selected_object_info(
                self._selected_widget_object.get_workforce().get_name() + " {} -> {}".format(
                    self._selected_widget_object.get_workforce().get_current_position(),
                    self._selected_widget_object.get_workforce().get_new_position()))

        self._selected_widget_object.start_blinking()

        # TODO draw buttons with actions  for this object on toolbar

    def deselect_widget_object_rather_than(self, row, column):
        logger.debug("deselect_object")

        if self._selected_widget_object is not None:
            my_new_row, my_new_column = self._selected_widget_object.get_workforce().get_new_position()
            my_row, my_column = self._selected_widget_object.get_workforce().get_current_position()
            if my_new_row == my_row and my_new_column == my_column:
                if my_row == row and my_column == column:
                    logger.debug("deselect_object do not deselect me")
                    return
            elif my_row == row and my_column == column:
                logger.debug("deselect_object do not deselect planned me")
                return

            self._selected_widget_object.stop_blinking()
            self._selected_widget_object = None

            self._info_panel.update_selected_object_info(None)

    def do_action(self, row, column):
        logger.debug("do_action in row:%s, column:%s", row, column)
        # if action is allowed do duty or move if allowed

        if self._selected_widget_object is None:
            logger.error("do_action something bad happened. Cannot do action for unknown object")
            return

        if isinstance(self._selected_widget_object, WorkforceWidget):
            logger.debug("do_action for workforce")
            self._selected_widget_object.plan_action(row, column, WorkforceAction.DUTY_ACTION)
        # TODO elif obj is ??? e.g. Naval or army?

        self.deselect_widget_object_rather_than(-1, -1)
