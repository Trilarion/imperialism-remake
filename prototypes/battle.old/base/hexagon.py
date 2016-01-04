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

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPolygonF
import math   
    
def hex_corner(x, y, size, i, offset):
    angle_deg = 60 * i   + offset
    angle_rad =  math.pi / 180 * angle_deg
    return QPointF(x + size * math.cos(angle_rad),
                 y + size * math.sin(angle_rad))
                 
def hexagon(center_x, center_y, size, offset):
    list_of_QPointF = [
        hex_corner(center_x, center_y,size/2,0, offset),
        hex_corner(center_x, center_y,size/2,1, offset),
        hex_corner(center_x, center_y,size/2,2, offset),
        hex_corner(center_x, center_y,size/2,3, offset),
        hex_corner(center_x, center_y,size/2,4, offset),
        hex_corner(center_x, center_y,size/2,5, offset)
    ]
    return QPolygonF(list_of_QPointF)
    
class QHexagon(QPolygonF):

    def __init__(self,center_x, center_y, size, offset):
        self.corners = hexagon(center_x, center_y, size, offset)
        super(self.__class__, self).__init__(self.corners)
