"""
    Calculates the contour of nation maps.
"""

from PyQt5 import QtWidgets

import base.constants as constants
from server.scenario import *

if __name__ == '__main__':

    # load scenario

    scenario = Scenario()
    scenario.load(constants.extend(constants.CORE_SCENARIO_FOLDER, 'Europe1814.scenario'))

    # nation map
    columns = scenario[constants.ScenarioProperties.MAP_COLUMNS]
    rows = scenario[constants.ScenarioProperties.MAP_ROWS]
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
                for direction in constants.TileDirections:
                    position = scenario.get_neighbor_position(column, row, direction)
                    if position is None or map[position[0] + columns * position[1]] != nation: # outside is automatically seen as border
                        # now that is interesting we are at a border, follow
                        print(position)


    app = QtWidgets.QApplication([])

    scene = QtWidgets.QGraphicsScene()

    view = QtWidgets.QGraphicsView(scene)
    view.resize(300, 240)

    view.show()

    app.exec_()
