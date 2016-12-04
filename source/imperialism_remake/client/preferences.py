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
Preferences Widget
"""

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtNetwork as QtNetwork

from base import constants, tools
from client import audio
from lib import qt
from client.client import local_network_client


class PreferencesWidget(QtWidgets.QWidget):
    """
    Content widget for the options/preferences dialog window, based on QTabWidget.
    """

    def __init__(self, *args, **kwargs):
        """
        Create and add all tab
        """
        super().__init__(*args, **kwargs)

        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(32, 32))
        action_group = QtWidgets.QActionGroup(toolbar)

        # general preferences
        action_general = qt.create_action(tools.load_ui_icon('icon.preferences.general.png'), 'Show general preferences', action_group, toggle_connection=self._toggled_action_preferences_general, checkable=True)
        toolbar.addAction(action_general)

        # network preferences
        a = qt.create_action(tools.load_ui_icon('icon.preferences.network.png'), 'Show network preferences', action_group, toggle_connection=self._toggled_action_preferences_network, checkable=True)
        toolbar.addAction(a)

        # graphics preferences
        a = qt.create_action(tools.load_ui_icon('icon.preferences.graphics.png'), 'Show graphics preferences', action_group, toggle_connection=self._toggled_action_preferences_graphics, checkable=True)
        toolbar.addAction(a)

        # music preferences
        a = qt.create_action(tools.load_ui_icon('icon.preferences.music.png'), 'Show music preferences', action_group, toggle_connection=self._toggled_action_preferences_music, checkable=True)
        toolbar.addAction(a)

        # spacer
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        # reset preferences
        a = QtWidgets.QAction(tools.load_ui_icon('icon.preferences.reset.png'), 'Reset preferences', self)
        a.triggered.connect(self.reset_preferences)
        toolbar.addAction(a)

        self.stacked_layout = QtWidgets.QStackedLayout()

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(toolbar)
        layout.addLayout(self.stacked_layout)

        # empty lists
        self._check_boxes = []
        self._line_edits = []
        self._sliders = []

        # add tabs
        self._layout_widget_preferences_general()
        self._layout_widget_preferences_graphics()
        self._layout_widget_preferences_music()
        self._layout_widget_preferences_network()

        # initially show general preferences
        action_general.setChecked(True)

    def reset_preferences(self):
        """
        Shows small confirmation dialog, then resets preferences to factory standard.
        """
        answer = QtWidgets.QMessageBox.question(self, 'Preferences', 'Restore standard preferences?',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            pass

    def _toggled_action_preferences_general(self, checked):
        """
        Toolbar button for general preferences toggled.

        :param checked: If True, the button is now checked.
        """
        if checked:
            self.stacked_layout.setCurrentWidget(self.tab_general)

    def _layout_widget_preferences_general(self):
        """
        Create general options widget.
        """
        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)

        # language
        label = QtWidgets.QLabel('Choose')
        combobox = QtWidgets.QComboBox()
        tab_layout.addWidget(qt.wrap_in_groupbox(qt.wrap_in_boxlayout((label, combobox)), 'User Interface Language'))

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_general = tab
        self.stacked_layout.addWidget(tab)

    def _toggled_action_preferences_graphics(self, checked):
        """
            Toolbar button for graphical preferences toggled.
        """
        if checked:
            self.stacked_layout.setCurrentWidget(self.tab_graphics)

    def _layout_widget_preferences_graphics(self):
        """
        Create graphical options widget.
        """

        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)

        # full screen mode
        checkbox = QtWidgets.QCheckBox('Full screen mode')
        self._register_check_box(checkbox, constants.Option.MAINWINDOW_FULLSCREEN)
        tab_layout.addWidget(checkbox)

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_graphics = tab
        self.stacked_layout.addWidget(tab)

    def _toggled_action_preferences_network(self, checked):
        """
        Toolbar button for network preferences toggled.

        :param checked:
        """
        if checked:
            self.stacked_layout.setCurrentWidget(self.tab_network)

    def _layout_widget_preferences_network(self):
        """
        Create network options widget.
        """
        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)

        # client
        layout = QtWidgets.QVBoxLayout()
        if local_network_client.is_connected():
            peer_address, peer_port = local_network_client.peer_address()
            status = 'Connected to {}:{}'.format(peer_address.toString(), peer_port)
        else:
            status = 'Disconnected'
        layout.addWidget(QtWidgets.QLabel(status))
        tab_layout.addWidget(qt.wrap_in_groupbox(layout, 'Client'))
        # alias name edit box
        label = QtWidgets.QLabel('Alias')
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        self._register_line_edit(edit, constants.Option.LOCALCLIENT_NAME)
        layout.addLayout(qt.wrap_in_boxlayout((label, edit)))

        # local server group box
        layout = QtWidgets.QVBoxLayout()
        local_ip = [x.toString() for x in QtNetwork.QNetworkInterface.allAddresses() if not x.isLoopback() and x.protocol() == QtNetwork.QAbstractSocket.IPv4Protocol][0]
        layout.addWidget(QtWidgets.QLabel('Local IP address: {}'.format(local_ip)))
        # accepts incoming connections checkbox
        checkbox = QtWidgets.QCheckBox('Accepts incoming connections')
        self._register_check_box(checkbox, constants.Option.LOCALSERVER_OPEN)
        layout.addWidget(checkbox)
        # alias name edit box
        label = QtWidgets.QLabel('Alias')
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        self._register_line_edit(edit, constants.Option.LOCALSERVER_NAME)
        layout.addLayout(qt.wrap_in_boxlayout((label, edit)))
        # actions toolbar
        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(24, 24))
        # show local server monitor
        toolbar.addAction(
            qt.create_action(tools.load_ui_icon('icon.preferences.network.png'), 'Show local server monitor', toolbar))
        layout.addLayout(qt.wrap_in_boxlayout(toolbar))
        tab_layout.addWidget(qt.wrap_in_groupbox(layout, 'Local Server'))

        # remote server group box
        layout = QtWidgets.QVBoxLayout()
        # remote server address
        label = QtWidgets.QLabel('Remote IP address')
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        layout.addLayout(qt.wrap_in_boxlayout((label, edit)))
        # actions toolbar
        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(24, 24))
        # connect to remote server
        a = qt.create_action(tools.load_ui_icon('icon.preferences.network.png'), 'Connect/Disconnect to remote server', toolbar, checkable=True)
        toolbar.addAction(a)
        layout.addLayout(qt.wrap_in_boxlayout(toolbar))
        tab_layout.addWidget(qt.wrap_in_groupbox(layout, 'Remote Server'))

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_network = tab
        self.stacked_layout.addWidget(tab)

    def _toggled_action_preferences_music(self, checked):
        """
        Toolbar button for music preferences toggled.

        :param checked:
        """
        if checked:
            self.stacked_layout.setCurrentWidget(self.tab_music)

    def _layout_widget_preferences_music(self):
        """
        Create music options widget.
        """
        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)

        # soundtrack section
        layout = QtWidgets.QVBoxLayout()

        # mute checkbox
        checkbox = QtWidgets.QCheckBox('Mute soundtrack')
        self._register_check_box(checkbox, constants.Option.SOUNDTRACK_MUTE)
        layout.addWidget(checkbox)

        # volume slide
        layout.addWidget(QtWidgets.QLabel('Volume'))
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setTickInterval(25)
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        slider.setMaximumWidth(100)
        self._register_slider(slider, constants.Option.SOUNDTRACK_VOLUME)
        layout.addWidget(slider)

        # wrap in group box and add to tab
        tab_layout.addWidget(qt.wrap_in_groupbox(layout, 'Soundtrack'))

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_music = tab
        self.stacked_layout.addWidget(tab)

    def _register_check_box(self, checkbox, option):
        """
        Takes an option identifier (str) where the option value must be True/False and sets a checkbox according
        to the current value. Stores the checkbox, option pair in a list.

        :param checkbox:
        :param option:
        """
        checkbox.setChecked(tools.get_option(option))
        self._check_boxes.append((checkbox, option))

    def _register_slider(self, slider, option):
        """

        :param slider:
        :param option:
        """
        slider.setValue(tools.get_option(option))
        self._sliders.append((slider, option))

    def _register_line_edit(self, edit, option):
        """

        :param edit:
        :param option:
        """
        edit.setText(tools.get_option(option))
        self._line_edits.append((edit, option))

    def close_request(self, parent_widget):
        """
        User wants to close the dialog, check if an option has been changed. If an option has been changed, ask for
        okay from user and update the options.

        Also react on some updated options (others might only take affect after a restart of the application).
        We immediately : start/stop music (mute option)

        :param parent_widget:
        :return:
        """
        # check if something was changed
        options_modified = any([box.isChecked() is not tools.get_option(option) for (box, option) in self._check_boxes])
        # TODO line edits and sliders

        if options_modified:
            answer = QtWidgets.QMessageBox.question(parent_widget, 'Preferences', 'Save modified preferences', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if answer == QtWidgets.QMessageBox.Yes:
                # all _check_boxes
                for (box, option) in self._check_boxes:
                    tools.set_option(option, box.isChecked())
                # start/stop audio player (depending on mute)
                if tools.get_option(constants.Option.SOUNDTRACK_MUTE):
                    audio.soundtrack_player.stop()
                    pass
                else:
                    audio.soundtrack_player.play()
                    pass
        return True
