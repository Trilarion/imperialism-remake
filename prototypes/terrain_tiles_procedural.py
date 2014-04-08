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

import sys
from PySide import QtGui, QtCore

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    S = 80

    scene = QtGui.QGraphicsScene()
    for x in range(0, 9):
        for y in range(0, 6):
            scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)

    view = QtGui.QGraphicsView(scene)
    view.resize(800, 600)
    view.show()

    print(view.sceneRect())

    sys.exit(app.exec_())