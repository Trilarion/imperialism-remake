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
from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets

from imperialism_remake.base import constants, tools
from imperialism_remake.base.network import local_network_client
from imperialism_remake.client.graphics.minimap_nation_item import MiniMapNationItem
from imperialism_remake.lib import qt, utils

logger = logging.getLogger(__name__)


class SinglePlayerScenarioPreview(QtWidgets.QWidget):
    """
    Displays the preview of a single player scenario in the game lobby.

    If a nation is selected the nation_selected signal is emitted with the nation name.
    """

    #: signal, emitted if a nation is selected and the start button is pressed
    nation_selected = QtCore.pyqtSignal(int)

    def __init__(self, scenario_file):
        """
            Given a scenario file name, get the preview from the server.
        """
        # TODO move the network communication outside this class.
        super().__init__()

        # add a channel for us
        local_network_client.connect_to_channel(constants.C.LOBBY, self.received_preview)

        # send a message and ask for preview
        local_network_client.send(constants.C.LOBBY, constants.M.LOBBY_SCENARIO_PREVIEW, scenario_file)

        self.selected_nation = None

    def received_preview(self, client, channel, action, message):
        """
        Populates the widget after the network reply comes from the server with the preview.
        """

        # immediately unsubscribe, we need it only once
        local_network_client.disconnect_from_channel(constants.C.LOBBY, self.received_preview)

        # unpack message
        nations = [(message[constants.SCENARIO_FILE_NATIONS][key][constants.NationProperty.NAME], key) for key in message[constants.SCENARIO_FILE_NATIONS]]
        nations = sorted(nations)  # by first element, which is the name
        nation_names, self.nation_ids = zip(*nations)

        # fill the widget with useful stuff
        layout = QtWidgets.QGridLayout(self)

        # selection list for nations
        self.nations_list = QtWidgets.QListWidget()
        # self.nations_list.setFixedWidth(200)
        self.nations_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.nations_list.itemSelectionChanged.connect(self.nations_list_selection_changed)
        self.nations_list.addItems(nation_names)
        self.nations_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # 10px extra
        self.nations_list.setFixedWidth(self.nations_list.sizeHintForColumn(0) +
                                        2 * self.nations_list.frameWidth() + 17 + 10)
        # TODO use app.style().pixelMetric(QtWidgets.QStyle.PM_ScrollBarExtent)
        layout.addWidget(qt.wrap_in_groupbox(self.nations_list, 'Nations'), 0, 0)

        # map view (no scroll bars)
        self.map_scene = QtWidgets.QGraphicsScene()
        self.map_view = qt.FitSceneInViewGraphicsView(self.map_scene)
        self.map_view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.map_view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #       self.map_view.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        #       self.map_view.setFixedSize(100, 100)
        layout.addWidget(qt.wrap_in_groupbox(self.map_view, 'Map'), 0, 1)

        # scenario description
        self.description = QtWidgets.QPlainTextEdit()
        self.description.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.description.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.description.setReadOnly(True)
        self.description.setPlainText(message[constants.ScenarioProperty.DESCRIPTION])
        height = self.description.fontMetrics().lineSpacing() * 4  # 4 lines high
        self.description.setFixedHeight(height)
        layout.addWidget(qt.wrap_in_groupbox(self.description, 'Description'), 1, 0, 1, 2)  # goes over two columns

        # nation description
        self.nation_info = QtWidgets.QPlainTextEdit()
        self.nation_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.nation_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.nation_info.setReadOnly(True)
        height = self.nation_info.fontMetrics().lineSpacing() * 6  # 6 lines high
        self.nation_info.setFixedHeight(height)
        layout.addWidget(qt.wrap_in_groupbox(self.nation_info, 'Nation Info'), 2, 0, 1, 2)

        # stretching of the elements
        layout.setRowStretch(0, 1)  # nation list and map get all the available height
        layout.setColumnStretch(1, 1)  # map gets all the available width

        # add the start button
        toolbar = QtWidgets.QToolBar()
        toolbar.addAction(qt.create_action(tools.load_ui_icon('icon.confirm.png'), 'Start selected scenario', toolbar,
                                           trigger_connection=self.start_scenario_clicked))
        layout.addWidget(toolbar, 3, 0, 1, 2, alignment=QtCore.Qt.AlignRight)

        # draw the map
        columns = message[constants.ScenarioProperty.MAP_COLUMNS]
        rows = message[constants.ScenarioProperty.MAP_ROWS]
        self.map_scene.setSceneRect(0, 0, columns, rows)

        # fill the ground layer with a neutral color
        item = self.map_scene.addRect(0, 0, columns, rows)
        item.setBrush(QtCore.Qt.lightGray)
        item.setPen(qt.TRANSPARENT_PEN)
        item.setZValue(0)

        # for all nations
        for nation_id, nation in message[constants.SCENARIO_FILE_NATIONS].items():

            # get nation color
            color_string = nation[constants.NationProperty.COLOR]
            color = QtGui.QColor()
            color.setNamedColor(color_string)

            # get nation name
            nation_name = nation[constants.NationProperty.NAME]

            # get nation outline
            path = QtGui.QPainterPath()
            # TODO traversing everything is quite slow go only once and add to paths
            for column in range(0, columns):
                for row in range(0, rows):
                    if nation_id == message['map'][column + row * columns]:
                        path.addRect(column, row, 1, 1)
            path = path.simplified()

            item = MiniMapNationItem(path)
            item.signaller.clicked.connect(
                partial(self.map_selected_nation, utils.index_of_element(nation_names, nation_name)))
            #           item.signaller.entered.connect(partial(self.change_map_name, nation_name))
            #           item.signaller.left.connect(partial(self.change_map_name, ''))
            brush = QtGui.QBrush(color)
            item.setBrush(brush)

            item.setToolTip(nation_name)

            pen = QtGui.QPen()
            pen.setWidth(2)
            pen.setCosmetic(True)
            item.setPen(pen)

            self.map_scene.addItem(item)
        #           item = self.map_scene.addPath(path, brush=brush) # will use the default pen for outline

        self.preview = message

    def change_map_name(self, nation_name, event):
        """
        Display of hoovered nation name.
        """
        # TODO not looking nice so far. Improve, display somewhere else (not in the scene).
        self.map_name_item.setText(nation_name)

    def map_selected_nation(self, nation_row, event):
        """
            Clicked on a nation in the map. Just selects the corresponding row in the nation table.
        """
        self.nations_list.setCurrentRow(nation_row)

    def nations_list_selection_changed(self):
        """
            A nation was selected in the nations table, fill nation description and set it selected.
        """
        row = self.nations_list.currentRow()
        nation_id = self.nation_ids[row]
        #       self.selected_nation = self.preview['nations'][nation_id][constants.NationProperty.NAME]
        self.selected_nation = nation_id
        nation_description = self.preview[constants.SCENARIO_FILE_NATIONS][nation_id][constants.NationProperty.DESCRIPTION]
        self.nation_info.setPlainText(nation_description)

    def start_scenario_clicked(self):
        """
            Start scenario button is clicked. Only react if a nation is already selected.
        """
        if self.selected_nation is not None:
            self.nation_selected.emit(self.selected_nation)

    def stop(self):
        """
            Interruption. Clean up network channels and the like.
        """
        # TODO is this right? network channel might still be open
#       local_network_client.remove_channel(self.CH_PREVIEW, ignore_not_existing=True)
