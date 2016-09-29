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

import base.constants as constants
import base.tools as tools
import client.audio as audio
import lib.qt_graphics as qt_graphics


class PreferencesWidget(QtWidgets.QWidget):
    """
        Content widget for the options/preferences dialog window, based on QTabWidget.

        TODO add option to go back to default settings
    """

    def __init__(self):
        """
            Create and add all tabs
        """
        super().__init__()

        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(32, 32))
        action_group = QtWidgets.QActionGroup(toolbar)

        action_preferences_general = qt_graphics.create_action(tools.load_ui_icon('icon.preferences.general.png'),
            'Show general preferences', action_group, toggle_connection=self._toggled_action_preferences_general,
            checkable=True)
        toolbar.addAction(action_preferences_general)

        toolbar.addAction(
            qt_graphics.create_action(tools.load_ui_icon('icon.preferences.network.png'), 'Show network preferences',
                action_group, toggle_connection=self._toggled_action_preferences_network, checkable=True))
        toolbar.addAction(
            qt_graphics.create_action(tools.load_ui_icon('icon.preferences.graphics.png'), 'Show graphics preferences',
                action_group, toggle_connection=self._toggled_action_preferences_graphics, checkable=True))
        toolbar.addAction(
            qt_graphics.create_action(tools.load_ui_icon('icon.preferences.music.png'), 'Show music preferences',
                action_group, toggle_connection=self._toggled_action_preferences_music, checkable=True))

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

        # show general preferences
        action_preferences_general.setChecked(True)

    def _toggled_action_preferences_general(self, checked):
        """
            Toolbar button for general preferences toggled.
        """
        if checked is True:
            self.stacked_layout.setCurrentWidget(self.tab_general)

    def _layout_widget_preferences_general(self):
        """
            Create general options widget.
        """
        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)

        # reset button
        button = QtWidgets.QPushButton('Restore defaults')
        tab_layout.addLayout(qt_graphics.wrap_in_boxlayout(button))

        # language
        layout = QtWidgets.QVBoxLayout()
        tab_layout.addWidget(qt_graphics.wrap_in_groupbox(layout, 'Language'))

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_general = tab
        self.stacked_layout.addWidget(tab)

    def _toggled_action_preferences_graphics(self, checked):
        """
            Toolbar button for graphical preferences toggled.
        """
        if checked is True:
            self.stacked_layout.setCurrentWidget(self.tab_graphics)

    def _layout_widget_preferences_graphics(self):
        """
            Create graphical options widget.
        """

        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)

        # full screen mode
        checkbox = QtWidgets.QCheckBox('Full screen mode')
        self._register_check_box(checkbox, constants.Opt.FULLSCREEN)
        tab_layout.addWidget(checkbox)

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_graphics = tab
        self.stacked_layout.addWidget(tab)

    def _toggled_action_preferences_network(self, checked):
        """
            Toolbar button for network preferences toggled.
        """
        if checked is True:
            self.stacked_layout.setCurrentWidget(self.tab_network)

    def _layout_widget_preferences_network(self):
        """
            Create network options widget.
        """
        tab = QtWidgets.QWidget()
        tab_layout = QtWidgets.QVBoxLayout(tab)

        # status label
        self.network_status_label = QtWidgets.QLabel('')
        tab_layout.addWidget(self.network_status_label)

        # remote server group box
        l = QtWidgets.QVBoxLayout()
        # remote server address
        l2 = QtWidgets.QHBoxLayout()
        l2.addWidget(QtWidgets.QLabel('Remote IP address'))
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        l2.addWidget(edit)
        l2.addStretch()
        l.addLayout(l2)
        # actions toolbar
        l2 = QtWidgets.QHBoxLayout()
        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(24, 24))
        # connect to remote server
        toolbar.addAction(qt_graphics.create_action(tools.load_ui_icon('icon.preferences.network.png'),
            'Connect/Disconnect to remote server', toolbar, checkable=True))
        l2.addWidget(toolbar)
        l2.addStretch()
        l.addLayout(l2)
        tab_layout.addWidget(qt_graphics.wrap_in_groupbox(l, 'Remote Server'))

        # local server group box
        l = QtWidgets.QVBoxLayout()
        # accepts incoming connections checkbox
        checkbox = QtWidgets.QCheckBox('Accepts incoming connections')
        self._register_check_box(checkbox, constants.Opt.LS_OPEN)
        l.addWidget(checkbox)
        # alias name edit box
        l2 = QtWidgets.QHBoxLayout()
        l2.addWidget(QtWidgets.QLabel('Alias'))
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        l2.addWidget(edit)
        l2.addStretch()
        self._register_line_edit(edit, constants.Opt.LS_NAME)
        l.addLayout(l2)
        # actions toolbar
        l2 = QtWidgets.QHBoxLayout()
        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(24, 24))
        # show local server monitor
        toolbar.addAction(
            qt_graphics.create_action(tools.load_ui_icon('icon.preferences.network.png'), 'Show local server monitor',
                toolbar))
        # local server is on/off
        toolbar.addAction(
            qt_graphics.create_action(tools.load_ui_icon('icon.preferences.network.png'), 'Turn local server on/off',
                toolbar, checkable=True))
        l2.addWidget(toolbar)
        l2.addStretch()
        l.addLayout(l2)
        tab_layout.addWidget(qt_graphics.wrap_in_groupbox(l, 'Local Server'))

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_network = tab
        self.stacked_layout.addWidget(tab)

    def _toggled_action_preferences_music(self, checked):
        """
            Toolbar button for music preferences toggled.
        """
        if checked is True:
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
        self._register_check_box(checkbox, constants.Opt.SOUNDTRACK_MUTE)
        layout.addWidget(checkbox)

        # volume slide
        layout.addWidget(QtWidgets.QLabel('Volume'))
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setTickInterval(25)
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        slider.setMaximumWidth(100)
        self._register_slider(slider, constants.Opt.SOUNDTRACK_VOLUME)
        layout.addWidget(slider)

        # wrap in group box and add to tab
        tab_layout.addWidget(qt_graphics.wrap_in_groupbox(layout, 'Soundtrack'))

        # vertical stretch
        tab_layout.addStretch()

        # add tab
        self.tab_music = tab
        self.stacked_layout.addWidget(tab)

    def _register_check_box(self, checkbox, option):
        """
            Takes an option identifier (str) where the option value must be True/False and sets a checkbox according
            to the current value. Stores the checkbox, option pair in a list.
        """
        checkbox.setChecked(tools.get_option(option))
        self._check_boxes.append((checkbox, option))

    def _register_slider(self, slider, option):
        """

        """
        slider.setValue(tools.get_option(option))
        self._sliders.append((slider, option))

    def _register_line_edit(self, edit, option):
        """

        """
        edit.setText(tools.get_option(option))
        self._line_edits.append((edit, option))

    def close_request(self, parent_widget):
        """
            User wants to close the dialog, check if an option has been changed. If an option has been changed, ask for
            okay from user and update the options.

            Also react on some updated options (others might only take affect after a restart of the application).
            We immediately : start/stop music (mute option)
        """
        # check if something was changed
        options_modified = any([box.isChecked() is not tools.get_option(option) for (box, option) in self._check_boxes])
        # TODO line edits and sliders

        if options_modified:
            answer = QtWidgets.QMessageBox.question(parent_widget, 'Preferences', 'Save modified preferences',
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            if answer == QtWidgets.QMessageBox.Yes:
                # all _check_boxes
                for (box, option) in self._check_boxes:
                    tools.set_option(option, box.isChecked())
                # start/stop audio player (depending on mute)
                if tools.get_option(constants.Opt.SOUNDTRACK_MUTE):
                    audio.soundtrack_player.stop()
                    pass
                else:
                    audio.soundtrack_player.play()
                    pass
        return True
