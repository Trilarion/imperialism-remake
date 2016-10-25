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
Monitors the server state and updates it regularly
"""

from datetime import datetime

from PyQt5 import QtCore, QtWidgets

from base import constants
import base.network
from client.client import local_network_client

class ServerMonitorWidget(QtWidgets.QWidget):
    """
    Displays server stats
    """

    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QVBoxLayout(self)

        self.status = QtWidgets.QLabel('No information yet.')
        self.layout.addWidget(self.status)
        self.layout.addStretch()

        local_network_client.connect_to_channel(constants.C.SYSTEM, self.update_monitor)

        # one initial update
        self.request_update()

        # set timer for following updates
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.request_update)
        self.timer.setInterval(10000)
        self.timer.start()

    def request_update(self):
        """

        """
        local_network_client.send(constants.C.SYSTEM, constants.M.SYSTEM_MONITOR_UPDATE)

    def update_monitor(self, client:base.network.NetworkClient, channel:constants.C, action:constants.M, content):
        """
        Regular updates of the server stats
        """
        # get time and format it
        now = datetime.now().strftime('%H:%M:%S')

        text = 'Last update: {} - {} connected clients'.format(now, content['number_connected_clients'])
        self.status.setText(text)

    def cleanup(self, parent_widget):
        """
        User wants to close the dialog

        :param parent_widget:
        """
        local_network_client.disconnect_from_channel(constants.C.SYSTEM, self.request_update)
        return True
