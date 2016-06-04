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

from PyQt5 import QtWidgets
import lib.graphics as g

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)
        self.setWindowTitle('Graphics Examples')
        # options layout
        layout_options = QtWidgets.QGridLayout()

        # show button
        button_show = QtWidgets.QPushButton()
        button_show.setText('Notification')
        button_show.clicked.connect(self.show_notification)

        # show button layout
        layout_show = QtWidgets.QHBoxLayout()
        layout_show.addStretch()
        layout_show.addWidget(button_show)

        # main layout
        layout_main = QtWidgets.QVBoxLayout()
        layout_main.addLayout(layout_options)
        layout_main.addStretch()
        layout_main.addLayout(layout_show)

        # set layout and notification
        self.setLayout(layout_main)

    def show_notification(self):
        message = 'Test notification'
        self.notification = g.Notification(self, message, position_constraint=g.RelativeLayoutConstraint().center_horizontal().south(20))
        self.notification.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    window = Window()
    window.show()

    app.exec_()