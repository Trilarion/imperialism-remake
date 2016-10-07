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
    Starts the browser. Start with project root as working directory.
"""

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import lib.qt as qt
import base.tools as tools

if __name__ == '__main__':

    app = QtWidgets.QApplication([])

    widget = qt.BrowserWidget(tools.load_ui_icon)
    widget.home_url = QtCore.QUrl(("http://qt-project.org/"))
    widget.show()

    app.exec_()
