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
Simple example of how to show a web view with PyQt5. Uses QtWebEngineWidgets.QtWebEngineView
"""

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets

if __name__ == '__main__':

    # create app
    app = QtWidgets.QApplication([])

    # QWebEngineView
    web_view_widget = QtWebEngineWidgets.QWebEngineView()
    # displays the actual page title as windows title
    web_view_widget.titleChanged.connect(web_view_widget.setWindowTitle)
    web_view_widget.load(QtCore.QUrl("http://qt-project.org/"))
    web_view_widget.show()

    # run
    app.exec_()