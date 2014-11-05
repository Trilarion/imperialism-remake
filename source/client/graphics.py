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

from PySide import QtGui, QtCore

from base import tools as t


"""
    Graphics elements that are dependent on the tools and lib.graphics library, but not on any game specific (constants,
    scenario or otherwise) logic. Therefore kind of a intermediate abstraction between the fully independent lib.graphics
    module and the client game specific logic under folder client.
"""

import lib.graphics as g


class GameDialog(QtGui.QWidget):
    """
        Create a dialog (widget) with many preconfigured properties (modality, title, parent, content, help callback, ...

        Main property is the custom window frame that allows dragging around (on the titlebar).

        Reference in stylesheets with 'gamedialog'.
    """

    def __init__(self, parent, content, title=None, modal=True, delete_on_close=False, help_callback=None,
                 close_callback=None):
        # no frame but a standalong window
        super().__init__(parent, f=QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

        # we need this
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setObjectName('gamedialog')

        # should be deleted on close
        if delete_on_close:
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # default state is Qt.NonModal
        if modal:
            self.setWindowModality(QtCore.Qt.WindowModal)

        # title bar
        title_bar = g.DraggableToolBar()
        title_bar.setIconSize(QtCore.QSize(20, 20))
        title_bar.setObjectName('titlebar')
        title_bar.setSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Fixed)
        title_bar.dragged.connect(lambda delta: self.move(self.pos() + delta))

        # title in titlebar and close icon
        title = QtGui.QLabel(title)
        title.setObjectName('gamedialog-title')
        title_bar.addWidget(title)

        # spacer between titlebar and help/close icons
        spacer = QtGui.QWidget()
        spacer.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        title_bar.addWidget(spacer)

        # if help call back is given, add help icon
        if help_callback:
            help_action = QtGui.QAction(t.load_ui_icon('icon.help.png'), 'Help', title_bar)
            help_action.triggered.connect(help_callback)
            title_bar.addAction(help_action)

        self.close_callback = close_callback
        # the close button always calls self.close (but in closeEvent we call the close callback if existing)
        close_action = QtGui.QAction(t.load_ui_icon('icon.close.png'), 'Close', title_bar)
        close_action.triggered.connect(self.close)
        title_bar.addAction(close_action)

        # escape key for close
        action = QtGui.QAction(self)
        action.setShortcut(QtGui.QKeySequence('Escape'))
        action.triggered.connect(self.close)
        self.addAction(action)

        # layout is 2 pixel contents margin (border), title bar and content widget
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.addWidget(title_bar)
        self.layout.addWidget(content)

    def closeEvent(self, event):
        """
            To prevent Alt+F4 or other automatic closes.
        """
        if self.close_callback and not self.close_callback(self):
            event.ignore()