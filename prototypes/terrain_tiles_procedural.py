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

import sys, os
from PySide import QtGui, QtCore

def load_80x80(name):
    path = os.path.join('.', 'terrain_tiles_procedural_data', '80x80', name)
    if not os.path.isfile(path):
        raise Exception('Could not find: {}.'.format(path))
    pixmap = QtGui.QPixmap(path)
    return pixmap

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    test_map = [['se', 'se', 'sw', 'sw', 'b', 'b', 'm', 'm', 'sh'],
                ['se', 'p', 'p', 'sw', 'b', 'm', 'm', 'm', 'sh'],
                ['sc', 'sc', 'p', 't', 'b', 'm', 'f', 'f', 'sh'],
                ['sc', 'g', 'p', 't', 't', 'f', 'f', 'f', 'o'],
                ['ho', 'g', 'g', 'd', 'c', 'c', 'hi', 'f', 'o'],
                ['ho', 'ho', 'd', 'd', 'c', 't', 'hi', 'hi', 'o']]

    map_tiles = {
        'b': 'buffalo.png',
        'c': 'cotton.png',
        'd': 'desert.png',
        'f': 'forest.png',
        'g': 'grain.png',
        'hi': 'hills.png',
        'ho': 'horse.png',
        'm': 'mountains.png',
        'o': 'orchard.png',
        'p': 'plains.png',
        'sc': 'scrubforest.png',
        'se': 'sea.png',
        'sh': 'sheep.png',
        'sw': 'swamp.png',
        't': 'tundra.png'
    }

    # translate to pixmaps
    for key, name in map_tiles.items():
        img = load_80x80(name)
        map_tiles[key] = img

    S = 80

    scene = QtGui.QGraphicsScene()
    for x in range(0, 9):
        for y in range(0, 6):
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setZValue(2)

    for x in range(0, 9):
        for y in range(0, 6):
            key = test_map[y][x]
            item = scene.addPixmap(map_tiles[key])
            item.setOffset(x * S + y % 2 * S / 2, y * S)
            item.setZValue(1)

    view = QtGui.QGraphicsView(scene)
    view.resize(800, 600)
    view.show()

    print(view.sceneRect())

    sys.exit(app.exec_())