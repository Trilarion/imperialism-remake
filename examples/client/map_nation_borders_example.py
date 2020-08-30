"""
Calculates the contour of nation maps.
"""

import os, sys

from PyQt5 import QtWidgets

if __name__ == '__main__':

    # add source directory to path if needed
    source_directory = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.path.pardir, os.path.pardir, 'source'))
    if source_directory not in sys.path:
        sys.path.insert(0, source_directory)

    from imperialism_remake.base import constants
    from imperialism_remake.server.server_scenario import ServerScenario

    # load scenario
    scenario = ServerScenario.from_file(constants.extend(constants.CORE_SCENARIO_FOLDER, 'Europe1814.scenario'))

    # nation map
    columns = scenario[constants.ScenarioProperty.MAP_COLUMNS]
    rows = scenario[constants.ScenarioProperty.MAP_ROWS]
    map = [0] * (columns * rows)
    for nation in scenario.nations():
        provinces = scenario.provinces_of_nation(nation)
        for province in provinces:
            tiles = scenario.province_property(province, 'tiles')
            for column, row in tiles:
                map[row * columns + column] = nation

    # get outlines
    for nation in scenario.nations():
        visited = [False] * (columns * rows)
        for i in range(0, columns * rows):
            column = i % columns
            row = i // columns
            visited[i] = True
            if map[i] == nation:
                for direction in constants.TileDirections:
                    position = scenario.neighbor_position(column, row, direction)
                    if position is None or map[position[0] + columns * position[1]] != nation: # outside is automatically seen as border
                        # now that is interesting we are at a border, follow
                        print(position)


    app = QtWidgets.QApplication([])

    scene = QtWidgets.QGraphicsScene()

    view = QtWidgets.QGraphicsView(scene)
    view.resize(300, 240)

    view.show()

    app.exec_()
