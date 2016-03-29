"""
    Calculates the countour of nation maps
"""

from PyQt5 import QtGui

from base import constants as c
from server.scenario import *

# load scenario

scenario = Scenario()
scenario.load(c.extend(c.Core_Scenario_Folder, 'Europe1814.scenario'))

# nation map
columns = scenario[MAP_COLUMNS]
rows = scenario[MAP_ROWS]
map = [0] * (columns * rows)
for nation in scenario.all_nations():
    provinces = scenario.get_provinces_of_nation(nation)
    for province in provinces:
        tiles = scenario.get_province_property(province, 'tiles')
        for column, row in tiles:
            map[row * columns + column] = nation

# get outlines
for nation in scenario.all_nations():
    visited = [False] * (columns * rows)
    for i in range(0, columns * rows):
        column = i % columns
        row = i // columns
        visited[i] = True
        if map[i] == nation:
            for direction in c.TileDirections:
                position = scenario.get_neighbor_position(column, row, direction)
                if position is None or map[position[0] + columns * position[1]] != nation: # outside is automatically seen as border
                    # now that is interesting we are at a border, follow
                    print(position)


app = QtGui.QApplication([])

scene = QtGui.QGraphicsScene()

view = QtGui.QGraphicsView(scene)
view.resize(300, 240)

view.show()

app.exec_()
