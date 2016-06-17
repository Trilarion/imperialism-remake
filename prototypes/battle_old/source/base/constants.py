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

import re

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QSizePolicy

LOG_FILENAME = 'game.log'
LOG_PATTERN = '%(asctime)s %(module)s:%(filename)s:%(funcName)s:%(lineno)d   %(levelname)s:%(message)s'

MINIMUM_RESOLUTION = 800, 600
RESOLUTION_PATTERN = '^(\d+)\s*x\s*(\d+)$'


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


def parse_resolution(res_str):
    try:
        m = re.search(RESOLUTION_PATTERN, res_str)
        w, h = int(m.group(1)), int(m.group(2))
        return w, h
    except AttributeError:
        return -1, -1


def parse_resolution_to_qsize(res_str):
    w, h = parse_resolution(res_str)
    return QSize(w, h)


def get_min_resolution_qsize():
    w, h = MINIMUM_RESOLUTION
    return QSize(w, h)

