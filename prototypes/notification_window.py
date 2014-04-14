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

from PySide import QtCore, QtGui

class Notification(QtGui.QWidget):

    finished = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


class NotificationExample(QtGui.QMainWindow):

    def __init__(self):
        super().__init__()

        button = QtGui.QPushButton()
        button.setText('Show')

if __name__ == '__main__':

    app = QtGui.QApplication([])

    mainwindow = NotificationExample()
    mainwindow.show()


    app.exec_()