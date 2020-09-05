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
from PyQt5.QtWidgets import QGraphicsOpacityEffect

logger = logging.getLogger(__name__)


class BlinkingWidget(QtWidgets.QLabel):
    BLINK_DURATION = 700

    def __init__(self):
        super(BlinkingWidget, self).__init__()

        self._effect = QGraphicsOpacityEffect()
        self._animation = QtCore.QPropertyAnimation(self._effect, b"opacity")
        self._animation.setDuration(self.BLINK_DURATION / 2)

        self._timer = QtCore.QTimer()
        self._timer.setInterval(self.BLINK_DURATION)
        self._timer.timeout.connect(self._timer_fired)

        self.setGraphicsEffect(self._effect)

        self._do_blink(1, 1)

    def _timer_fired(self):
        self._do_blink(1, 0)
        self._do_blink(0, 1)

    def start_animation(self):
        logger.debug("start_animation")
        # TODO

    def stop_animation(self):
        logger.debug("stop_animation")
        # TODO

    def start_blinking(self):
        logger.debug("start_blinking")
        self._timer.start()

    def stop_blinking(self):
        logger.debug("stop_blinking")
        self._timer.stop()

        self._do_blink(1, 1)

    def _do_blink(self, start, stop):
        self._animation.setStartValue(start)
        self._animation.setEndValue(stop)
        self._animation.start()
