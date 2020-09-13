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


class BlinkingAnimatedWidget(QtWidgets.QLabel):
    BLINK_DURATION = 700
    ANIMATION_PIXMAP_DURATION = 700

    def __init__(self, pixmap_stand):
        super(BlinkingAnimatedWidget, self).__init__()

        self._effect = QGraphicsOpacityEffect()
        self._animation = QtCore.QPropertyAnimation(self._effect, b"opacity")
        self._animation.setDuration(self.BLINK_DURATION / 2)

        self._timer_blink = QtCore.QTimer()
        self._timer_blink.setInterval(self.BLINK_DURATION)
        self._timer_blink.timeout.connect(self._timer_blink_fired)

        self._timer_animation_pixmap = QtCore.QTimer()
        self._timer_animation_pixmap.setInterval(self.ANIMATION_PIXMAP_DURATION)
        self._timer_animation_pixmap.timeout.connect(self._animation_pixmap_step)

        self.setGraphicsEffect(self._effect)

        self._do_blink(1, 1)

        self._animation_pixmaps = []
        self._current_animation_pixmap_index = 0
        self._original_pixmap = pixmap_stand
        self.setPixmap(self._original_pixmap)

    def _timer_blink_fired(self) -> None:
        self._do_blink(1, 0)
        self._do_blink(0, 1)

    def start_animation(self) -> None:
        logger.debug("start_animation")
        if self._current_animation_pixmap_index < len(self._animation_pixmaps):
            self._timer_animation_pixmap.start()
            self.setPixmap(self._animation_pixmaps[self._current_animation_pixmap_index])
            self._current_animation_pixmap_index = 1
        else:
            logger.warning("No animation pixmap is set")

    def stop_animation(self) -> None:
        logger.debug("stop_animation")
        self._timer_animation_pixmap.stop()

        self.setPixmap(self._original_pixmap)

    def _add_animation_pixmaps(self, pixmaps) -> None:
        [self._animation_pixmaps.append(pixmap) for pixmap in pixmaps]

    def _animation_pixmap_step(self) -> None:
        self.setPixmap(self._animation_pixmaps[self._current_animation_pixmap_index])
        self._current_animation_pixmap_index += 1
        if self._current_animation_pixmap_index == len(self._animation_pixmaps):
            self._current_animation_pixmap_index = 0

    def start_blinking(self) -> None:
        logger.debug("start_blinking")
        self._timer_blink.start()

    def stop_blinking(self) -> None:
        logger.debug("stop_blinking")
        self._timer_blink.stop()

        self._do_blink(1, 1)

    def _do_blink(self, start: int, stop: int) -> None:
        self._animation.setStartValue(start)
        self._animation.setEndValue(stop)
        self._animation.start()
