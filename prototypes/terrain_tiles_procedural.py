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

import sys, os, random
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

def load_objects(name):
    path = os.path.join('.', 'terrain_tiles_procedural_data', 'objects', name)
    if not os.path.isfile(path):
        raise Exception('Could not find: {}.'.format(path))
    pixmap = QtGui.QPixmap(path)
    return pixmap

def scene_texture_with_objects():
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

    objects = {
        'h1': 'hill_1.png',
        'h2': 'hill_2.png',
        'm1': 'mountain_1.png',
        'm2': 'mountain_2.png',
        'f1': 'tree_1.png',
        'f2': 'tree_2.png',
        'sc1': 'scrubtree_1.png',
        'sc2': 'scrubtree_2.png'
    }

    # translate objects to pixmaps
    for key, name in objects.items():
        img = load_objects(name)
        objects[key] = img

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

    # paint grid
    for x in range(0, 9):
        for y in range(0, 6):
            pass
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setZValue(1000)

    # paint terrain textures
    for x in range(0, 9):
        for y in range(0, 6):
            key = test_map[y][x]
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setBrush(textures[map_tiles[key]])
            pen = QtGui.QPen(QtCore.Qt.transparent)
            item.setPen(pen)
            item.setZValue(1)

    # paint some random objects
    for x in range(0, 9):
        for y in range(0, 6):
            pos = (x * S + y % 2 * S / 2, y * S)
            key = test_map[y][x]
            if key == 'f':
                # forest
                for h in range(0, 17):
                    item = scene.addPixmap(objects['f1'])
                    item.setOffset(pos[0] + S * random.random()-0.1*S, pos[1] + S * random.random()-0.1*S)
                    item.setZValue(2)
                for h in range(0, 17):
                    item = scene.addPixmap(objects['f2'])
                    item.setOffset(pos[0] + S * random.random()-0.1*S, pos[1] + S * random.random()-0.1*S)
                    item.setZValue(2)
            if key == 'sc':
                # scrub forest
                for h in range(0, 17):
                    item = scene.addPixmap(objects['sc1'])
                    item.setOffset(pos[0] + S * random.random()-0.1*S, pos[1] + S * random.random()-0.1*S)
                    item.setZValue(2)
                for h in range(0, 17):
                    item = scene.addPixmap(objects['sc2'])
                    item.setOffset(pos[0] + S * random.random()-0.1*S, pos[1] + S * random.random()-0.1*S)
                    item.setZValue(2)
            if key == 'm':
                # mountains
                for h in range(0, 4):
                    item = scene.addPixmap(objects['m1'])
                    item.setOffset(pos[0] + S * random.random()-0.2*S, pos[1] + S * random.random()-0.2*S)
                    item.setZValue(2)
                for h in range(0, 3):
                    item = scene.addPixmap(objects['m2'])
                    item.setOffset(pos[0] + S * random.random()-0.2*S, pos[1] + S * random.random()-0.2*S)
                    item.setZValue(2)
            if key == 'hi':
                # hills
                for h in range(0, 4):
                    item = scene.addPixmap(objects['h1'])
                    item.setOffset(pos[0] + S * random.random()-0.2*S, pos[1] + S * random.random()-0.2*S)
                    item.setZValue(2)
                for h in range(0, 3):
                    item = scene.addPixmap(objects['h2'])
                    item.setOffset(pos[0] + S * random.random()-0.2*S, pos[1] + S * random.random()-0.2*S)
                    item.setZValue(2)
    return scene

def scene_river_simple():

    # the begin is like texture_simple()
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

    # grid
    for x in range(0, 9):
        for y in range(0, 6):
            pass
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setZValue(1000)

    # textures
    for x in range(0, 9):
        for y in range(0, 6):
            key = test_map[y][x]
            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
            item.setBrush(textures[map_tiles[key]])
            pen = QtGui.QPen(QtCore.Qt.transparent)
            item.setPen(pen)
            item.setZValue(1)

    # river
    river_texture = load_texture('brushwalker437.jpg')
    river_brush = QtGui.QBrush(river_texture)
    river_tiles = [(6,2), (5,2), (5,1), (5,0), (4,0), (3,1), (2,1), (1,1), (0.5, 1)]
    scale = lambda x: (x[0] * S + x[1] % 2 * S/2 + S/2, x[1] * S + S/2)
    start = scale(river_tiles[0])
    river = []
    po = start
    for x in range(1, len(river_tiles)):
        pn = scale(river_tiles[x])
        for y in range(2, 11, 3):
            river.append((po[0]+y/10*(pn[0]-po[0]), po[1]+y/10*(pn[1]-po[1])))
        po = pn

    path = QtGui.QPainterPath()
    path.moveTo(start[0], start[1])
    po = start
    for p in river:
        pn = p
        pc = ((po[0] + pn[0]) / 2 + random.uniform(-10, 10),(po[1] + pn[1]) / 2 + random.uniform(-10, 10))
        path.quadTo(pc[0], pc[1], pn[0], pn[1])
        # path.lineTo(p[0], p[1])
        po = pn

    pen = QtGui.QPen(river_brush, 8, c=QtCore.Qt.RoundCap, j=QtCore.Qt.RoundJoin)
    item = scene.addPath(path, pen)
    item.setZValue(2)

    # border
    border_tiles = [(4.5, 3), (3.5,3), (2.5,3), (2.5, 4), (3.5, 4), (4.5, 4), (4.5, 3)]
    border_tiles = [(x[0] * S, x[1] * S) for x in border_tiles]
    start = border_tiles[0]
    path = QtGui.QPainterPath()
    path.moveTo(start[0], start[1])
    for p in border_tiles[1:]:
        path.lineTo(p[0], p[1])
    brush = QtGui.QBrush(QtGui.QColor(255, 128, 0, 192), bs=QtCore.Qt.Dense3Pattern)
    pen = QtGui.QPen(brush, 16, j=QtCore.Qt.MiterJoin)
    item = scene.addPath(path, pen)
    item.setZValue(2)

    return scene

def scene_texture_custom_shape():
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

    # draw the grid
#    for x in range(0, 9):
#        for y in range(0, 6):
#            item = scene.addRect(x * S + y % 2 * S / 2, y * S, S, S)
#            item.setZValue(1000)

    # pen = QtGui.QPen(QtCore.Qt.transparent, 0)
    pen = QtGui.QPen()

    # get paths
    paths = {}
    for x in range(0, 9):
        for y in range(0, 6):
            key = map_tiles[test_map[y][x]]
            if key not in paths:
                paths[key] = QtGui.QPainterPath()
            paths[key].addRect(x * S + y % 2 * S / 2, y * S, S, S)

    # delete the 'p' path (we don't do it)
    del(paths['p'])

    # simplify paths, and change randomly
    for key, path in paths.items():
        path = path.simplified()
        polygons = path.toSubpathPolygons()
        path = QtGui.QPainterPath()
        for i in range(0, len(polygons)):
            polygon = polygons[i]
            path.moveTo(polygon[0])
            for j in range(1, len(polygon)):
                path.quadTo(polygon[j], polygon[j] + QtCore.QPointF(random.uniform(-15, 15), random.uniform(-15, 15)))


        paths[key] = path

    # add to scene and fill with texture
    for key, path in paths.items():
        item = scene.addPath(path, pen, textures[map_tiles[key]])
        item.setZValue(100)

    # just fill everything with 'p' texture below
    item = scene.addRect(0, 0, 9.5*S, 6*S, pen, textures['p'])
    item.setZValue(1)


    return scene

if __name__ == '__main__':
    app = QtGui.QApplication([])

    # scene = scene_80x80()
    # scene = scene_colors_simple()
    # scene = scene_texture_simple()
    # scene = scene_texture_with_objects()
    # scene = scene_river_simple()
    scene = scene_texture_custom_shape()

    size = scene.sceneRect()
    item = scene.addRect(size)
    item.setZValue(10)

    view = QtGui.QGraphicsView(scene)
    view.resize(780, 500)
    view.show()

    sys.exit(app.exec_())