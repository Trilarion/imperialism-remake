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
from PySide import QtCore, QtGui

test_map = [['se', 'se', 'sw', 'sw', 'b', 'b', 'm', 'm', 'sh'],
            ['se', 'p', 'p', 'sw', 'b', 'm', 'm', 'm', 'sh'],
            ['sc', 'sc', 'p', 't', 'b', 'm', 'f', 'f', 'sh'],
            ['sc', 'g', 'p', 't', 't', 'f', 'f', 'f', 'o'],
            ['ho', 'g', 'g', 'd', 'c', 't', 'hi', 'f', 'o'],
            ['ho', 'ho', 'd', 'd', 'c', 'c', 'hi', 'hi', 'o']]


def load_80x80(name):
    path = os.path.join('.', 'terrain_tiles_procedural_data', '80x80', name)
    if not os.path.isfile(path):
        raise Exception('Could not find: {}.'.format(path))
    pixmap = QtGui.QPixmap(path)
    return pixmap

def scene_80x80():
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

    return scene

def scene_colors_simple():
    scene = QtGui.QGraphicsScene()

    # maps tiles to a color
    map_tiles = {
        'b': QtCore.Qt.green,
        'c': QtCore.Qt.green,
        'd': QtCore.Qt.yellow,
        'f': QtCore.Qt.green,
        'g': QtCore.Qt.green,
        'hi': QtCore.Qt.green,
        'ho': QtCore.Qt.green,
        'm': QtCore.Qt.green,
        'o': QtCore.Qt.green,
        'p': QtCore.Qt.green,
        'sc': QtCore.Qt.green,
        'se': QtCore.Qt.blue,
        'sh': QtCore.Qt.green,
        'sw': QtCore.Qt.darkGreen,
        't': QtCore.Qt.white
    }

    S = 80

    for x in range(0, 9):
        for y in range(0, 6):
            pass
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setZValue(2)

    for x in range(0, 9):
        for y in range(0, 6):
            key = test_map[y][x]
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setBrush(map_tiles[key])
            pen = QtGui.QPen(QtCore.Qt.transparent)
            item.setPen(pen)
            item.setZValue(1)

    return scene

def load_texture(name):
    path = os.path.join('.', 'terrain_tiles_procedural_data', 'textures', name)
    if not os.path.isfile(path):
        raise Exception('Could not find: {}.'.format(path))
    pixmap = QtGui.QPixmap(path)
    return pixmap

def scene_texture_simple():
    scene = QtGui.QGraphicsScene()

    textures = {
        'se': 'tex_Water.jpg',
        'sw': 'Swamp.png',
        't': 'Tundra.png',
        'p': 'Plains.png',
        'd': 'Desert.png'
    }

    # translate textures to brush
    for key, name in textures.items():
        img = load_texture(name)
        textures[key] = QtGui.QBrush(img)

    # maps tiles to a texture
    map_tiles = {
        'b': 'p',
        'c': 'p',
        'd': 'd',
        'f': 'p',
        'g': 'p',
        'hi': 'p',
        'ho': 'p',
        'm': 'p',
        'o': 'p',
        'p': 'p',
        'sc': 'p',
        'se': 'se',
        'sh': 'p',
        'sw': 'sw',
        't': 't'
    }

    S = 80

    for x in range(0, 9):
        for y in range(0, 6):
            pass
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setZValue(2)

    for x in range(0, 9):
        for y in range(0, 6):
            key = test_map[y][x]
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setBrush(textures[map_tiles[key]])
            pen = QtGui.QPen(QtCore.Qt.transparent)
            item.setPen(pen)
            item.setZValue(1)

    return scene

if __name__ == '__main__':
    app = QtGui.QApplication([])

    # scene = scene_80x80()
    # scene = scene_colors_simple()
    scene = scene_texture_simple()

    size = scene.sceneRect()
    item = scene.addRect(size)
    item.setZValue(10)

    view = QtGui.QGraphicsView(scene)
    view.resize(780, 500)
    view.show()

    sys.exit(app.exec_())