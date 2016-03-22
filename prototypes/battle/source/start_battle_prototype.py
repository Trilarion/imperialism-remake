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

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from battle.landBattleView import MainBattleWindows
from config.config import Config
from base.constants import version

CONFIG_FILE = 'config.ini'

if __name__ == '__main__':
    v = version()
    print('Battle prototype version: %f' % version())
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icon.png'))
    # load config files
    config = Config(CONFIG_FILE,v)
    # start the battle view
    mySW = MainBattleWindows(config)
    mySW.show()
    sys.exit(app.exec_())
