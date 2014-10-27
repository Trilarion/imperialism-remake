# Imperialism remake
# Copyright (C) 2014 Trilarion
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

from PySide import QtCore, QtGui
from server.network import server_manager

class ServerMonitorWidget(QtGui.QWidget):

    def __init__(self):
        super().__init__()

        layout = QtGui.QGridLayout(self)

        self.status_label = QtGui.QLabel()
        layout.addWidget(self.status_label, 0, 0)

        # set timer for update
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_monitor)
        self.timer.setInterval(60000) # every second
        self.timer.start()
        self.update_monitor()

    def update_monitor(self):
        text = '{} clients'.format(len(server_manager.server_clients))
        self.status_label.setText(text)