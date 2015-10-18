from PyQt5 import QtGui, QtCore, QtWidgets, QtWebKitWidgets
import base.constants as c, base.tools as t
from lib.browser import BrowserWidget
import os

def local_url(relative_path):
    absolute_path = os.path.abspath(relative_path)
    url = QtCore.QUrl.fromLocalFile(absolute_path)
    return url

def icon_provider(text):
    return None

class BrowserWidget(QtWidgets.QWidget):

    def __init__(self, home_url, icon_provider):
        super().__init__()

        # store home url
        self.home_url = home_url

        # create and add tool bar on top (non floatable or movable)
        tool_bar = QtWidgets.QToolBar(self)

        # create actions, connect to methods, add to tool bar
        action_home = QtWidgets.QAction(self)
        #action_home.setIcon(icon_provider('icon.home.png'))
        action_home.setToolTip('Home')
        action_home.triggered.connect(self.load_home_url)
        tool_bar.addAction(action_home)

        action_backward = QtWidgets.QAction(self)
        action_backward.setEnabled(False)
        #action_backward.setIcon(icon_provider('icon.backward.png'))
        tool_bar.addAction(action_backward)
        self.action_backward = action_backward

        action_forward = QtWidgets.QAction(self)
        action_forward.setEnabled(False)
        #action_forward.setIcon(icon_provider('icon.forward.png'))
        tool_bar.addAction(action_forward)
        self.action_forward = action_forward

        # create and add web view, connect linkClicked signal with our newPage method
        web_view = QtWebKitWidgets.QWebView()
        # must set DelegationPolicy to include all links
        web_view.page().setLinkDelegationPolicy(QtWebKitWidgets.QWebPage.DelegateAllLinks)
        web_view.linkClicked.connect(self.load)
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


app = QtWidgets.QApplication([])

# load global stylesheet to app
with open(c.Global_Stylesheet, 'r', encoding='utf-8') as file:
    style_sheet = file.read()
app.setStyleSheet(style_sheet)

#help_browser_widget = BrowserWidget(QtCore.QUrl(c.Manual_Index), t.load_ui_icon)
#help_browser_widget.show()

home_url = local_url('./data/manual/index.html')
w = BrowserWidget(home_url, icon_provider)
w.load_home_url()
w.show()

app.exec_()
