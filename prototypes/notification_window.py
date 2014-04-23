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

    def __init__(self, parent):
        super().__init__(parent, QtCore.Qt.FramelessWindowHint)
        # super().__init__(parent)

        self.setAutoFillBackground(False)
        print(self.backgroundRole())
        # self.setWindowOpacity(0.1)
        # self.setBackgroundRole(QtGui.QPalette.Window)
        # self.palette().setColor(self.backgroundRole(), QtCore.Qt.green)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), QtGui.QColor(255, 0, 0, 128))
        #self.setPalette(p)

        self.label = QtGui.QLabel(self)
        self.label.setText('+++ Notification text +++')

        layout = QtGui.QHBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


class Window(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)

        button = QtGui.QPushButton()
        button.setText('Show')
        button.clicked.connect(self.show_notification)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(button)
        layout.addStretch()

        self.setLayout(layout)

    def show_notification(self):
        # notification = Notification(self)notification = Notification(self)
        self.notification = Notification(None)
        effect = QtGui.QGraphicsOpacityEffect()
        effect.setOpacity(0.5)
        # self.notification.setGraphicsEffect(effect)
        self.notification.label.setGraphicsEffect(effect)
        animation = QtCore.QPropertyAnimation(effect, 'opacity')
        animation.setDuration(2000)
        animation.setStartValue(0)
        animation.setEndValue(1)
        self.notification.show()
        # animation.start()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    app.quitOnLastWindowClosed()

    window = Window()
    window.show()

    app.exec_()
