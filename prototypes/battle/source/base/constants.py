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


import os

from PyQt5.QtGui import QTransform, QPixmap, QFont
from PyQt5.QtWidgets import QSizePolicy


def default_size_policy(widget, horizontal, vertical):
    size_policy = QSizePolicy(horizontal, vertical)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    return size_policy


def default_font():
    font = QFont()
    font.setPointSize(10)
    font.setWeight(75)
    font.setBold(True)
    return font


def miror_pixmap(pixmap):
    transform = QTransform()
    transform.scale(-1, 1)
    return QPixmap(pixmap.transformed(transform))


def format_money(money):
    str_init = str(money)
    retval = ""
    for i in range(0, len(str_init)):
        if (len(str_init) - i) % 3 == 0 and i != 0:
            retval += ","
        retval += str_init[i]
    return retval


def extend(path, *parts):
    """
        Uses os.path.join to join parts of a path. Also checks for existence and raises an error
        if the path is not existing.
        :param path:
    """
    extended = os.path.join(path, *parts)
    if not os.path.exists(extended):
        raise RuntimeError('constructed path {} does not exist'.format(extended))
    if Debug_Mode:
        Used_Resources.add(extended)
    return extended


# debug mode and helpers
Debug_Mode = False
Used_Resources = set()

# base folders (do not directly contain data)
Data_Folder = extend('..', 'data')
Artwork_Folder = extend(Data_Folder, 'artwork')

# graphics related folders
Graphics_Folder = extend(Artwork_Folder, 'graphics')
Graphics_Map_Folder = extend(Graphics_Folder, 'map')
Graphics_Flag_Folder = extend(Graphics_Folder, 'flag')
Graphics_Coat_Of_Map_Folder = extend(Graphics_Folder, 'coat_of_arms')
Graphics_Unit_Folder = extend(Graphics_Folder, 'unit')


# Flag file
Flag_of_Algeria = extend(Graphics_Flag_Folder, 'Flag_of_Algeria.svg')
Flag_of_Bavaria = extend(Graphics_Flag_Folder, 'Flag_of_Bavaria.svg')
Flag_of_Denmark = extend(Graphics_Flag_Folder, 'Flag_of_Denmark.svg')
Flag_of_Egypt = extend(Graphics_Flag_Folder, 'Flag_of_Egypt.svg')
Flag_of_France = extend(Graphics_Flag_Folder, 'Flag_of_France.svg')
Flag_of_Hanover = extend(Graphics_Flag_Folder, 'Flag_of_Hanover.svg')
Flag_of_Russia = extend(Graphics_Flag_Folder, 'Flag_of_Russia.svg')
Flag_of_Spain = extend(Graphics_Flag_Folder, 'Flag_of_Spain.svg')
Flag_of_Sweden = extend(Graphics_Flag_Folder, 'Flag_of_Sweden.svg')
Flag_of_Switzerland = extend(Graphics_Flag_Folder, 'Flag_of_Switzerland.svg')
Flag_of_the_Kingdom_of_Sardinia = extend(Graphics_Flag_Folder, 'Flag_of_the_Kingdom_of_Sardinia.svg')
Flag_of_the_Kingdom_of_the_Two_Sicilies = extend(Graphics_Flag_Folder, 'Flag_of_the_Kingdom_of_the_Two_Sicilies.svg')
Flag_of_the_Netherlands = extend(Graphics_Flag_Folder, 'Flag_of_the_Netherlands.svg')
Flag_of_the_Papal_States = extend(Graphics_Flag_Folder, 'Flag_of_the_Papal_States.svg')
Flag_of_the_United_Kingdom = extend(Graphics_Flag_Folder, 'Flag_of_the_United_Kingdom.svg')
Flag_of_Portugal = extend(Graphics_Flag_Folder, 'Flag_of_Portugal.svg')
Flag_of_Ottoman = extend(Graphics_Flag_Folder, 'Flag_of_Ottoman.svg')
Graphics_Flag_list = [
    Flag_of_Algeria,
    Flag_of_Bavaria,
    Flag_of_Denmark,
    Flag_of_Egypt,
    Flag_of_France,
    Flag_of_Hanover,
    Flag_of_Russia,
    Flag_of_Spain,
    Flag_of_Sweden,
    Flag_of_Switzerland,
    Flag_of_the_Kingdom_of_Sardinia,
    Flag_of_the_Kingdom_of_the_Two_Sicilies,
    Flag_of_the_Netherlands,
    Flag_of_the_Papal_States,
    Flag_of_the_United_Kingdom,
    Flag_of_Portugal,
    Flag_of_Ottoman
]
# Coat of Map
Coat_of_arms_of_France = extend(Graphics_Coat_Of_Map_Folder, 'Coat_of_arms_of_France.svg')
Coat_of_arms_of_Italy = extend(Graphics_Coat_Of_Map_Folder, 'Coat_of_arms_of_Italy.svg')
Coat_of_arms_of_Russian_Empire = extend(Graphics_Coat_Of_Map_Folder, 'Coat_of_arms_of_Russian_Empire.svg')
Coat_of_arms_ottoman = extend(Graphics_Coat_Of_Map_Folder, 'Coat_of_arms_ottoman.svg')
Graphics_Coat_of_arms_list = [
    Coat_of_arms_of_France,
    Coat_of_arms_of_Italy,
    Coat_of_arms_of_Russian_Empire,
    Coat_of_arms_ottoman,
]

# Unit File
infantry_shoot = extend(Graphics_Unit_Folder, 'infantry.shoot.png')
infantry_stand = extend(Graphics_Unit_Folder, 'infantry.stand.png')
infantry_charge = extend(Graphics_Unit_Folder, 'infantry.charge.png')

Graphics_Unit_list = [
    infantry_shoot, infantry_stand, infantry_charge
]

# minimal screen resolution
Screen_Min_Size = (800, 600)
