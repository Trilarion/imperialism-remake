# Imperialism remake
# Copyright (C) 2017 Trilarion
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
    A full screen, frameless window with the possibility to show child dialogs

    See also: https://stackoverflow.com/questions/24395747
"""

if __name__ == '__main__':

    from PyQt5 import QtWidgets, QtCore

    app = QtWidgets.QApplication([])

    window = QtWidgets.QWidget(flags=QtCore.Qt.WindowStaysOnTopHint)

    child_window = QtWidgets.QWidget(window, flags=QtCore.Qt.Window)
    child_window.setWindowModality(QtCore.Qt.WindowModal)
    child_window.resize(400, 300)

    layout = QtWidgets.QVBoxLayout(window)
    exit = QtWidgets.QPushButton('Exit')
    exit.clicked.connect(app.exit)
    layout.addWidget(exit)
    create = QtWidgets.QPushButton('Create child window')
    create.clicked.connect(child_window.show)
    layout.addWidget(create)
    layout.addStretch()

    window.showFullScreen()

    app.exec_()