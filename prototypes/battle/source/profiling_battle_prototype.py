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

import sys
import os
import cProfile
import pstats
from base.config import Config
from PyQt5.QtWidgets import QApplication

CONFIG_FILE = 'config.ini'
TMP_FILE = 'tmp'

def config():
    c = Config(CONFIG_FILE)
    print(c.error_msg)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cProfile.run('config()',TMP_FILE)
    p = pstats.Stats(TMP_FILE)
    p.sort_stats('cumtime')
    p.print_stats()
    p.sort_stats('ncalls')
    p.print_stats()
    os.remove(TMP_FILE)