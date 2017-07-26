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

import os, sys

from PyQt5 import QtCore, QtWidgets

from imperialism_remake.base import tools
from imperialism_remake.lib import qt_webengine

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    app = QtWidgets.QApplication([])

    widget = qt_webengine.BrowserWidget(tools.load_ui_icon)
    widget.home_url = QtCore.QUrl(("http://qt-project.org/"))
    widget.show()

    app.exec_()
