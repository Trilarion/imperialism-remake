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



def format_money(money):
    str_init = str(money)
    retval = ""
    for i in range(0, len(str_init)):
        if (len(str_init) - i) % 3 == 0 and i != 0:
            retval += ","
        retval += str_init[i]
    return retval

