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
Graphics elements that are dependent on the tools and lib.graphics library, but not on any game specific (constants,
scenario or otherwise) logic. Therefore kind of a intermediate abstraction between the fully independent lib.graphics
module and the client game specific logic under folder client.
"""
import logging

from PyQt5 import QtWidgets

from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


class MiniMapNationItem(qt.ClickablePathItem):
    """
    The outline of a nation in any mini map that should be clickable. Has an effect.
    """

    def __init__(self, path, z_left=1, z_entered=2):
        """
        Adds a QGraphicsDropShadowEffect when hovering over the item. Otherwise it is just a clickable
        QGraphicsPathItem.
        """
        super().__init__(path)

        self.z_entered = z_entered
        self.z_left = z_left

        self.signaller.entered.connect(self.entered_item)
        self.signaller.left.connect(self.left_item)

        self.hover_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.hover_effect.setOffset(4, 4)
        self.setGraphicsEffect(self.hover_effect)

        # the graphics effect is enabled initially, disable by calling left_item
        self.left_item()

    def entered_item(self):
        """
        Set z value and enables the hover effect.
        """
        self.setZValue(self.z_entered)
        self.hover_effect.setEnabled(True)

    def left_item(self):
        """
        Set the z value and disables the hover effect.
        """
        self.hover_effect.setEnabled(False)
        self.setZValue(self.z_left)
