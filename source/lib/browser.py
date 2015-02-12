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

from PySide import QtGui, QtWebKit

"""
    Browser based on QtWebKit.QtWebView. Provides Home, Forward, Backward (in history) functionality.
"""

# TODO base instead on QtWebPage?

class BrowserWidget(QtGui.QWidget):
    def __init__(self, home_url, icon_provider):
        super().__init__()

        # store home url
        self.home_url = home_url

        # create and add tool bar on top (non floatable or movable)
        tool_bar = QtGui.QToolBar(self)

        # create actions, connect to methods, add to tool bar
        action_home = QtGui.QAction(self)
        action_home.setIcon(icon_provider('icon.home.png'))
        action_home.setToolTip('Home')
        action_home.triggered.connect(self.actionHomeTriggered)
        tool_bar.addAction(action_home)

        action_backward = QtGui.QAction(self)
        action_backward.setEnabled(False)
        action_backward.setIcon(icon_provider('icon.backward.png'))
        action_backward.triggered.connect(self.actionBackwardTriggered)
        tool_bar.addAction(action_backward)
        self.action_backward = action_backward

        action_forward = QtGui.QAction(self)
        action_forward.setEnabled(False)
        action_forward.setIcon(icon_provider('icon.forward.png'))
        action_forward.triggered.connect(self.actionForwardTriggered)
        tool_bar.addAction(action_forward)
        self.action_forward = action_forward

        # create and add web view, connect linkClicked signal with our newPage method
        web_view = QtWebKit.QWebView()
        # must set DelegationPolicy to include all links
        web_view.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        web_view.linkClicked.connect(self.newPage)
        self.web_view = web_view

        # set Layout
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(tool_bar)
        layout.addWidget(web_view)

        # Initialize history (initially there is no current page)
        self.history = []
        self.current_page_index = -1

        # Finally set the home page
        self.actionHomeTriggered()

    def actionHomeTriggered(self):
        """
            Sets the home page as new page
        """
        self.newPage(self.home_url)

    def actionForwardTriggered(self):
        """
            If there is somewhere to go forward in history, do it
        """
        # only if we aren't at the end of the index
        if self.current_page_index + 1 < len(self.history):
            # increase index
            self.current_page_index += 1
            # enable backward button
            self.action_backward.setEnabled(True)
            # disable forward button if we are at the end of the history
            if self.current_page_index + 1 == len(self.history):
                self.action_forward.setEnabled(False)
            # display page (should come last, because tool tips are set according to enabled/disabled state)
            self.displayPage(self.history[self.current_page_index])

    def actionBackwardTriggered(self):
        """
            If there is somewhere to go backward in history, do it
        """
        # only if we have something in the history
        if self.current_page_index > 0:
            # decrease index
            self.current_page_index -= 1
            # disable backward button if historyIndex == 0
            if self.current_page_index == 0:
                self.action_backward.setEnabled(False)
            # enable forward button
            self.action_forward.setEnabled(True)
            # display page (should come last, because tool tips are set according to enabled/disabled state)
            self.displayPage(self.history[self.current_page_index])

    def newPage(self, url):
        """
            A new Page is to be loaded, prune forward history and load it.
        """
        # TODO is the same as currently displayed don't do anything
        # increase index
        self.current_page_index += 1
        # prune forward history
        self.history = self.history[0: self.current_page_index]
        # add url
        self.history.append(url)
        # enable backward button if current_page_index > 0
        if self.current_page_index > 0:
            self.action_backward.setEnabled(True)
        # disable forward button
        self.action_forward.setEnabled(False)
        # display page
        self.displayPage(url)

    def displayPage(self, url):
        """
            Load the page and include the page title in the window title
        """
        # load new page
        self.web_view.load(url)

        # update title of window, only show extended version if the page has a title
        # TODO title?
        # page_title = self.web_view.title()
        # if not page_title:
        # self.widget.setWindowTitle(self.title)
        # else:
        #    self.widget.setWindowTitle('{} - {}'.format(self.title, self.web_view.title()))

        # update tooltips of forward/backward button
        if self.action_backward.isEnabled():
            text = self.history[self.current_page_index - 1].toString()
            self.action_backward.setToolTip(text)
        else:
            self.action_backward.setToolTip(None)
        if self.action_forward.isEnabled():
            text = self.history[self.current_page_index + 1].toString()
            self.action_forward.setToolTip(text)
        else:
            self.action_forward.setToolTip(None)