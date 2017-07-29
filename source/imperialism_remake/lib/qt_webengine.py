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
Wraps around QtWebEngineWidgets.QWebEngineView to provide a simple browser with home, forward and
backward functionality.
"""

from PyQt5 import QtWidgets
# TODO export new document title when load finished

try:
    from PyQt5 import QtWebEngineWidgets
except:
    pass  # TODO use this as switch


class BrowserWidget(QtWidgets.QWidget):
    """
    Browser based on QtWebEngineWidgets.QWebEngineView. Provides Home, Forward, Backward (history) functionality.
    """

    def __init__(self, icon_provider):
        """

        """
        super().__init__()

        # start with empty home url
        self.home_url = None
        self.clear_history = False

        # create and add tool bar on top (non floatable or movable)
        tool_bar = QtWidgets.QToolBar(self)

        # create actions, connect to methods, add to tool bar
        action_home = QtWidgets.QAction(self)
        action_home.setIcon(icon_provider('icon.home.png'))
        action_home.setToolTip('Home')
        action_home.triggered.connect(self.home)
        tool_bar.addAction(action_home)

        action_backward = QtWidgets.QAction(self)
        action_backward.setEnabled(False)  # initially not enabled
        action_backward.setIcon(icon_provider('icon.backward.png'))
        tool_bar.addAction(action_backward)
        self.action_backward = action_backward

        action_forward = QtWidgets.QAction(self)
        action_forward.setEnabled(False)  # initially not enabled
        action_forward.setIcon(icon_provider('icon.forward.png'))
        tool_bar.addAction(action_forward)
        self.action_forward = action_forward

        # create and add web view, also store history
        web_view = QtWebEngineWidgets.QWebEngineView()
        self.web_view = web_view
        self.web_view.loadFinished.connect(self.load_finished)

        # wire forward, backward
        action_backward.triggered.connect(self.backward)
        action_forward.triggered.connect(self.forward)

        # set Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(tool_bar)
        layout.addWidget(web_view)

    def home(self):
        """
        If a home URL is given, load it.
        """
        if self.home_url:
            self.clear_history = True
            self.web_view.load(self.home_url)

    def load(self, url):
        """
        Load an URL.
        """
        self.web_view.load(url)

    def forward(self):
        """
        Go forward in history.
        """
        self.web_view.history().forward()

    def backward(self):
        """
        Go backward in history.
        """
        self.web_view.history().back()

    def load_finished(self):
        """
        Called when loading a page is finished. Updates history and forward/backward buttons.
        """

        if self.clear_history:
            self.web_view.history().clear()  # deletes the history
            self.clear_history = False

        # enables/disables the forward/backward buttons
        self.action_backward.setEnabled(self.web_view.history().canGoBack())
        self.action_forward.setEnabled(self.web_view.history().canGoForward())
