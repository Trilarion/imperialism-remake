#!/usr/bin/python3
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
from PyQt5.QtGui import QPolygonF, QPixmap, QColor
import math   


def hex_corner(center, size, i, offset):
    #check center QPointF
    if not isinstance(center, QPointF):
        raise ValueError('center must be a QPointF instance')
    #check i = 0 1 2 3 4 5 
    if (not isinstance(i,int)) or i < 0 or i > 5:
        raise ValueError('i must be a int instance and i must be in range [0,5]')
    #check offset angle 0 or 30    
    if (not isinstance(offset, int)) or (offset!=0 and offset!=30):
        raise ValueError('offset must be a int instance and offset must be equal to 0 or 30')   
    #check size
    try:
        if size < 0:
            raise ValueError('size must be supperior to 0')     
    except TypeError:
        raise ValueError('size type must be an unorderable type')     
    angle_deg = 60 * i   + offset
    angle_rad =  math.pi / 180 * angle_deg
    return QPointF(center.x() + size * math.cos(angle_rad),
                 center.y() + size * math.sin(angle_rad))

class QHexagon(QPolygonF):
    '''Class QHexagon
    '''
    
    def __init__(self, center, size, rotation):
        #check center QPointF
        if not isinstance(center, QPointF):
            raise ValueError('center must be a QPointF instance')
        #check offset angle 0 or 30        
        if (not isinstance(rotation, int)) or (rotation!=0 and rotation!=30):
            raise ValueError('rotation must be a int instance and rotation must be equal to 0 or 30')
        #check size    
        try:
            if size < 0:
                raise ValueError('size must be supperior to 0')     
        except TypeError:
            raise ValueError('size type must be an unorderable type')        
        self.center = center
        self.size = size
        self.rotation = rotation
        self.corners = []
        for i in range(0,5):
            self.corners.append(hex_corner(center,size,i,rotation))
        #init QPolygonF
        super(self.__class__, self).__init__(self.corners)
        
        
    # Operations
    def width(self):
        '''function width
        
        returns int
        '''
        return self.size * math.sqrt(3)/2; 
    
    
    def height(self):
        '''function height
        
        returns int
        '''
        return self.size * 3/4;     
    
    def draw(self, scene, color, texture):
        '''function draw
        
        scene: QGraphicsScene
        color: QColor
        texture: QPixmap
        
        returns 
        '''
        if not isinstance(scene,QGraphicsScene) or scene == None:
            raise ValueError('texture must be a non null QGraphicsScene instance') 
        if not isinstance(texture,QPixmap) and texture != None:
            raise ValueError('texture must be a QPixmap instance or None') 
        if color == None and texture == None:
            raise ValueError('texture or color must be specified') 
        item = scene.addPolygon(self)
        if color!=None:
            item.setBrush(QBrush(color))

            
    def __eq__(self, other):
        if isinstance(other, QHexagon):
            return ( self.size == other.size
                and self.center.x() == other.center.x()
                and self.center.y() == other.center.y()
                and self.rotation == other.rotation)
        else:
            return False
            