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
Starts the client and delivers most of the code responsible for the main client screen and the diverse dialogs.
"""

# TODO automatic placement of help dialog depending on if another dialog is open

import logging

from PyQt5 import QtCore

from imperialism_remake.base import network as base_network
from imperialism_remake.lib import qt

# TODO like in audio, set the network client singleton somewhere else
local_network_client = base_network.NetworkClient()

logger = logging.getLogger(__name__)


class MapItem(QtCore.QObject):
    """
    Holds together a clickable QPixmapItem, a description text and a reference to a label that
    shows the text

    TODO use signals to show the text instead
    """
    description_change = QtCore.pyqtSignal(str)

    def __init__(self, parent, pixmap, label, description):
        super().__init__(parent)
        # store label and description
        self.label = label
        self.description = description

        # create clickable pixmap item and create fade animation
        self.item = qt.ClickablePixmapItem(pixmap)
        self.fade = qt.FadeAnimation(self.item)
        self.fade.set_duration(300)

        # wire to fade in/out
        self.item.signaller.entered.connect(self.fade.fadein)
        self.item.signaller.left.connect(self.fade.fadeout)

        # wire to show/hide description
        self.item.signaller.entered.connect(self.show_description)
        self.item.signaller.left.connect(self.hide_description)

    def show_description(self):
        """
        Shows the description in the label.
        """
        self.label.setText('<font color=#ffffff size=6>{}</font>'.format(self.description))

    def hide_description(self):
        """
        Hides the description from the label.
        """
        self.label.setText('')
