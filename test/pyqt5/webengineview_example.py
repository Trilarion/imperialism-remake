"""
    Simple example of how to show a web view with PyQt5. Uses QtWebEngineWidgets.QtWebEngineView
"""

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtWebEngineWidgets as QtWebEngineWidgets

# create app
app = QtWidgets.QApplication([])

# QWebEngineView
web_view_widget = QtWebEngineWidgets.QWebEngineView()
web_view_widget.titleChanged.connect(web_view_widget.setWindowTitle) # displays the actual page title as windows title
web_view_widget.load(QtCore.QUrl("http://qt-project.org/"))
web_view_widget.show()

# run
app.exec_()