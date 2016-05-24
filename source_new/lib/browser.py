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

from PyQt5 import QtWidgets, QtWebEngineWidgets

"""
    Browser based on QtWebKit.QtWebView. Provides Home, Forward, Backward (in history) functionality.
"""

class BrowserWidget(QtWidgets.QWidget):

    def __init__(self, home_url, icon_provider):
        super().__init__()

        # store home url
        self.home_url = home_url

        # create and add tool bar on top (non floatable or movable)
        tool_bar = QtWidgets.QToolBar(self)

        # create actions, connect to methods, add to tool bar
        action_home = QtWidgets.QAction(self)
        action_home.setIcon(icon_provider('icon.home.png'))
        action_home.setToolTip('Home')
        action_home.triggered.connect(self.load_home_url)
        tool_bar.addAction(action_home)

        action_backward = QtWidgets.QAction(self)
        action_backward.setEnabled(False)
        action_backward.setIcon(icon_provider('icon.backward.png'))
        tool_bar.addAction(action_backward)
        self.action_backward = action_backward

        action_forward = QtWidgets.QAction(self)
        action_forward.setEnabled(False)
        action_forward.setIcon(icon_provider('icon.forward.png'))
        tool_bar.addAction(action_forward)
        self.action_forward = action_forward

        # create and add web view, connect linkClicked signal with our newPage method
        web_view = QtWebEngineWidgets.QWebEngineView()
        # must set DelegationPolicy to include all links
        # web_view.page().setLinkDelegationPolicy(QtWebEngineWidgets.QWebPage.DelegateAllLinks)
        # web_view.linkClicked.connect(self.load)
        self.web_view = web_view

        # wire forward, backward
        action_backward.triggered.connect(web_view.back)
        action_forward.triggered.connect(web_view.forward)

        # set Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(tool_bar)
        layout.addWidget(web_view)

    def load_home_url(self):
        self.load(self.home_url)

    def load(self, url):
        self.web_view.load(url)

        # update enabled disabled status of actions
        history = self.web_view.history()
        self.action_backward.setEnabled(history.canGoBack())
        self.action_forward.setEnabled(history.canGoForward())