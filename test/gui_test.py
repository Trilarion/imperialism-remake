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

from PySide import QtGui
import gui

class Window(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        # options layout
        layout_options = QtGui.QGridLayout()

        # show button
        button_show = QtGui.QPushButton()
        button_show.setText('Show')
        button_show.clicked.connect(self.show_notification)

        # show button layout
        layout_show = QtGui.QHBoxLayout()
        layout_show.addStretch()
        layout_show.addWidget(button_show)

        # main layout
        layout_main = QtGui.QVBoxLayout()
        layout_main.addLayout(layout_options)
        layout_main.addStretch()
        layout_main.addLayout(layout_show)

        # set layout and notification
        self.setLayout(layout_main)

    def show_notification(self):
        gui.show_notification(self, 'Notification')

if __name__ == '__main__':
    app = QtGui.QApplication([])

    window = Window()
    window.show()

    app.exec_()