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

from PyQt5 import QtWidgets, QtCore, QtGui

from imperialism_remake.base import constants, tools
from imperialism_remake.lib import qt

logger = logging.getLogger(__name__)


def get_text(edit: QtWidgets.QLineEdit):
    """
    Returns the text of a line edit. However, if it is empty, it returns the place holder text (whatever there is).

    :param edit: The line edit
    :return: The text
    """
    logger.debug('get_text')

    if edit.text():
        return edit.text()
    else:
        return edit.placeholderText()


class NewScenarioWidget(QtWidgets.QWidget):
    """
    New scenario dialog.
    """

    #: signal, emitted if this dialog finishes successfully and transmits parameters in the dictionary
    finished = QtCore.pyqtSignal(object)

    # see also: https://stackoverflow.com/questions/43964766/pyqt-emit-signal-with-dict
    # and https://www.riverbankcomputing.com/pipermail/pyqt/2017-May/039175.html
    # may be changed back to dict with a later PyQt5 version

    def __init__(self, *args, **kwargs):
        """
        Sets up all the input elements of the create new scenario dialog.
        """
        super().__init__(*args, **kwargs)

        self.parameters = {}
        widget_layout = QtWidgets.QVBoxLayout(self)

        # title box
        box = QtWidgets.QGroupBox('Title')
        layout = QtWidgets.QVBoxLayout(box)
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(300)
        edit.setPlaceholderText('Unnamed')
        self.parameters[constants.ScenarioProperty.TITLE] = edit
        layout.addWidget(edit)
        widget_layout.addWidget(box)

        # map size
        box = QtWidgets.QGroupBox('Map size')
        layout = QtWidgets.QHBoxLayout(box)

        layout.addWidget(QtWidgets.QLabel('Width'))
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(50)
        edit.setValidator(QtGui.QIntValidator(1, 1000))
        edit.setPlaceholderText('100')
        self.parameters[constants.ScenarioProperty.MAP_COLUMNS] = edit
        layout.addWidget(edit)

        layout.addWidget(QtWidgets.QLabel('Height'))
        edit = QtWidgets.QLineEdit()
        edit.setFixedWidth(50)
        edit.setValidator(QtGui.QIntValidator(1, 1000))
        edit.setPlaceholderText('60')
        self.parameters[constants.ScenarioProperty.MAP_ROWS] = edit
        layout.addWidget(edit)
        layout.addStretch()

        widget_layout.addWidget(box)

        # vertical stretch
        widget_layout.addStretch()

        # add confirmation button
        layout = QtWidgets.QHBoxLayout()
        toolbar = QtWidgets.QToolBar()
        a = qt.create_action(tools.load_ui_icon('icon.confirm.png'), 'Create new scenario', toolbar, self.on_ok)
        toolbar.addAction(a)
        layout.addStretch()
        layout.addWidget(toolbar)
        widget_layout.addLayout(layout)

    def on_ok(self):
        """
        "Create scenario" has been clicked.
        """
        logger.debug('on_ok')

        p = {}

        # title
        key = constants.ScenarioProperty.TITLE
        p[key] = get_text(self.parameters[key])

        # number of columns
        key = constants.ScenarioProperty.MAP_COLUMNS
        p[key] = int(get_text(self.parameters[key]))

        # number of rows
        key = constants.ScenarioProperty.MAP_ROWS
        p[key] = int(get_text(self.parameters[key]))

        # TODO conversion can fail, (ValueError) give error message
        # we close the parent window and emit the appropriate signal
        self.parent().close()
        self.finished.emit(p)
