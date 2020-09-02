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

from PyQt5 import QtWidgets, QtCore

logger = logging.getLogger(__name__)


class BlinkingWidget(QtWidgets.QLabel):
    def __init__(self):
        super(BlinkingWidget, self).__init__()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._timer_fired)

    def _timer_fired(self):
        logger.debug("_timer_fired")

    def start_animation(self, pixmap):
        logger.debug("start_animation")

    def stop_animation(self):
        logger.debug("stop_animation")

    def start_blinking(self, pixmap):
        logger.debug("start_blinking")

    def stop_blinking(self):
        logger.debug("stop_blinking")
