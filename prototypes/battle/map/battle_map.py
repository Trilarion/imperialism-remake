# Imperialism remake
# Copyright (C) 2015 Spitaels <spitaelsantoine@gmail.com>
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

import math

from enum import Enum
from base import constants as c
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsSimpleTextItem
from PyQt5.QtCore import Qt, pyqtSignal, QPointF
from PyQt5.QtGui import QBrush, QPainterPath, QFont, QColor, QPen, QCursor
from base.hexagon import QHexagon
"""
    Defines a battle.
"""

DEFAULT_DIAMETER = 20
DEFAULT_FORTIFICATION_DIAMETER = 7
SCROLL_BAR_HEIGHT = 20


class TerrainType(Enum):
    Grass = 0
    Sand = 1
    River = 2
    
DefaultBrushColor = Qt.darkGreen
DefaultBrush = QBrush(DefaultBrushColor)


class Terrain:
    type = TerrainType.Grass
    fortification = False
    accessible = True

    @staticmethod
    def getTerrainBrush(int_type):
        if int_type == TerrainType.Grass:
            return QBrush(Qt.darkGreen)
        elif int_type == TerrainType.Sand:
            return QBrush(QColor(254,232,214))
        elif int_type == TerrainType.River:
            return QBrush(QColor(64,64,255))
        else:
            return DefaultBrush;


class BattleMap():

    def __init__(self, diameter = DEFAULT_DIAMETER, fortification_diameter = DEFAULT_FORTIFICATION_DIAMETER):
        """
            Start with a clean state.
        """
        self.diameter = diameter
        self.number_tiles = diameter * diameter
        self.fortification_diameter = fortification_diameter

    def tileSize(self,viewHeight):
        return (viewHeight - SCROLL_BAR_HEIGHT)/ ( (self.diameter - 1 ) * 3 / 4 + 1)

    @staticmethod
    def scene_position(column, row):
        """
            Converts a map position to a scene position
        """
        return math.sqrt(3)/2 * (column + ( (row + 1) % 2) /2), row * 3 / 4



class BattleMapView(QGraphicsView):
    """
        The big map holding the game map and everything.
    """

    tile_at_focus_changed = pyqtSignal(int, int)

    def __init__(self, battle):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.NoAnchor)
        self.setResizeAnchor(QGraphicsView.NoAnchor)
        self.setMouseTracking(True)
        self.current_column = -1
        self.current_row = -1
        self.battle = battle

    def redraw_map(self):
        """
            When a battle is loaded new we need to draw the whole map new.
        """
        self.scene.clear()
        self.TitleSize = self.battle.tileSize(self.height())
        columns = self.battle.diameter
        rows = self.battle.diameter

        width = (columns + 0.5) * self.TitleSize
        height = rows * self.TitleSize 
        self.scene.setSceneRect(0, 0, width, height)

        # fill plains, hills, mountains, tundra, swamp, desert with texture

        # draw the main hexagon
        sx, sy = self.battle.scene_position(columns/2, rows/2)        
        size_main = math.sqrt(3)/2 * (rows - 1) * self.TitleSize 
        center_x, center_y = size_main/2 +  self.TitleSize/2, size_main/2 -  3 * self.TitleSize/4
        main_hexa = QHexagon(center_x, center_y,  size_main,0)
        # draw the fortification hexagon
        size_fort = math.sqrt(3)/2 * (self.battle.fortification_diameter - 0.5) * self.TitleSize 
        center_x, center_y = size_main/2 +  self.TitleSize/2, size_main/2 - self.TitleSize/4
        fort_hexa = QHexagon(center_x, center_y,  size_fort,0)
        self.scene.addPolygon(fort_hexa)
        # draw the grid
        for row in range(0, rows):
            for column in range(0, columns):
                sx, sy = self.battle.scene_position(column, row)
                center_x, center_y = (sx + 0.5) * self.TitleSize, (sy + 0.5 ) * self.TitleSize
                hexa = QHexagon(center_x, center_y,  self.TitleSize,30)
                if hexa.intersected(main_hexa):
                    item = self.scene.addPolygon(hexa)
                    if hexa.intersected(fort_hexa):
                        item.setBrush(QBrush(Qt.red))
                    item.setZValue(1000)
                    text = '({},{})'.format(column, row)
                    item = QGraphicsSimpleTextItem(text)
                    item.setBrush(QBrush(Qt.black))
                    item.setPos((sx + 0.5) * self.TitleSize - item.boundingRect().width() / 2, (sy + 0.5) * self.TitleSize)
                    item.setZValue(1001)
                    self.scene.addItem(item)

    def resizeEvent(self, evt=None):
        self.redraw_map()

    #TODO optimize ....
    def mousePressEvent(self, event):
        position = QPointF(event.pos())

        columns = self.battle.diameter
        rows = self.battle.diameter

        # draw the main hexagon
        sx, sy = self.battle.scene_position(columns/2, rows/2)        
        size_main = math.sqrt(3)/2 * (rows - 1) * self.TitleSize 
        center_x, center_y = size_main/2 +  self.TitleSize/2, size_main/2 -  3 * self.TitleSize/4
        main_hexa = QHexagon(center_x, center_y,  size_main,0)

        # go each position of the grid
        for row in range(0, rows):
            for column in range(0, columns):
                sx, sy = self.battle.scene_position(column, row)
                center_x, center_y = (sx + 0.5) * self.TitleSize, (sy + 0.5 ) * self.TitleSize
                hexa = QHexagon(center_x, center_y,  self.TitleSize,30)
                if hexa.intersected(main_hexa):
                    if hexa.containsPoint(position,Qt.OddEvenFill):
                        print("pressed here: " + str(column) + ", " + str(row))
                        self.update()
                        return
        print("outside combat zone")
        self.update()

