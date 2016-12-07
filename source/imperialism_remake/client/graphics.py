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

from PyQt5 import QtGui, QtCore, QtWidgets

from imperialism_remake.base import tools
from imperialism_remake.lib import qt


class GameDialog(QtWidgets.QWidget):
    """
    Create a dialog (widget) with many pre-configured properties (modality, title, parent, content, help callback, ...
    Main property is the custom window frame that allows dragging around (on the title bar).

    Reference it in stylesheets with 'game-dialog'.
    """

    def __init__(self, parent, content, title=None, modal=True, delete_on_close=False, help_callback=None, close_callback=None):
        # no frame but a standalone window
        super().__init__(parent, flags=QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)

        # we need this
        self.setAttribute(QtCore.Qt.WA_StyledBackground)
        self.setObjectName('game-dialog')

        # should be deleted on close
        if delete_on_close:
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # default state is Qt.NonModal
        if modal:
            self.setWindowModality(QtCore.Qt.WindowModal)

        # title bar
        title_bar = qt.DraggableToolBar()
        title_bar.setIconSize(QtCore.QSize(20, 20))
        title_bar.setObjectName('game-dialog-titlebar')
        title_bar.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        title_bar.dragged.connect(lambda delta: self.move(self.pos() + delta))

        # title in titlebar and close icon
        title = QtWidgets.QLabel(title)
        title.setObjectName('game-dialog-title')
        title_bar.addWidget(title)

        # spacer between titlebar and help/close icons
        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        title_bar.addWidget(spacer)

        # if help call back is given, add help icon
        if help_callback:
            help_action = QtWidgets.QAction(tools.load_ui_icon('icon.help.png'), 'Help', title_bar)
            help_action.triggered.connect(help_callback)
            title_bar.addAction(help_action)

        self.close_callback = close_callback
        # the close button always calls self.close (but in closeEvent we call the close callback if existing)
        close_action = QtWidgets.QAction(tools.load_ui_icon('icon.close.png'), 'Close', title_bar)
        close_action.triggered.connect(self.close)
        title_bar.addAction(close_action)

        # escape key for close
        action = QtWidgets.QAction(self)
        action.setShortcut(QtGui.QKeySequence('Escape'))
        action.triggered.connect(self.close)
        self.addAction(action)

        # layout is 2 pixel contents margin (border), title bar and content widget
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.addWidget(title_bar)
        self.layout.addWidget(content)

    def closeEvent(self, event: QtGui.QCloseEvent):
        """
        Can be used to prevent Alt+F4 or other automatic closes.

        :param event: The close event
        """
        if self.close_callback and not self.close_callback(self):
            event.ignore()


class MiniMapNationItem(qt.ClickablePathItem):
    """
    The outline of a nation in any mini map that should be clickable. Has an effect.
    """

    def __init__(self, path, z_left=1, z_entered=2):
        """
        Adds a QGraphicsDropShadowEffect when hovering over the item. Otherwise it is just a clickable QGraphicsPathItem.
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
