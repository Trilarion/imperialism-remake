# Imperialism remake
# Copyright (C) 2016 Trilarion
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
Game lobby. Place for starting/loading games.
"""
import logging

from PyQt5 import QtCore, QtWidgets

from imperialism_remake.base import constants
from imperialism_remake.base.network import local_network_client

logger = logging.getLogger(__name__)


class SinglePlayerScenarioTitleSelection(QtWidgets.QGroupBox):
    """
    Displays a widget with all available scenario titles for starting new single player scenarios.
    """

    #: signal, emitted if a title is selected.
    title_selected = QtCore.pyqtSignal(str)

    # TODO if the height is higher than the window we may have to enable scroll bars, not now with one scenario though

    def __init__(self):
        """

        """
        super().__init__()
        self.setTitle('Select Scenario')
        self.layout = QtWidgets.QVBoxLayout(self)

        # add a channel for us
        local_network_client.connect_to_channel(constants.C.LOBBY, self.received_titles)

        # send message and ask for scenario titles
        local_network_client.send(constants.C.LOBBY, constants.M.LOBBY_SCENARIO_CORE_LIST)

    def received_titles(self, client, channel, action, content):
        """
            Received all available scenario titles as a list together with the file names
            which act as unique identifiers. The list is sorted by title.
        """

        # immediately close the channel, we do not want to get this content twice
        client.remove_channel(channel)

        # unpack content
        scenario_titles, self.scenario_files = zip(*content)

        # create list widget
        self.list = QtWidgets.QListWidget()
        self.list.itemSelectionChanged.connect(self.selection_changed)
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list.addItems(scenario_titles)
        # set height size fixed to content
        self.list.setFixedHeight(self.list.sizeHintForRow(0) * self.list.count() + 2 * self.list.frameWidth())

        self.layout.addWidget(self.list)

    def selection_changed(self):
        """
            A scenario title has been selected in the list.
        """
        # get selected file
        row = self.list.currentRow()  # only useful if QListWidget does not sort by itself
        scenario_file = self.scenario_files[row]
        # emit title selected signal
        self.title_selected.emit(scenario_file)

    def stop(self):
        """
            Interruption. Clean up network channels and the like.
        """
        # network channel might still be open
        local_network_client.remove_channel(self.CH_TITLES, ignore_not_existing=True)
