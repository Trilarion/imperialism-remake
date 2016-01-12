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
from battle.landArmy import LandArmy
from battle.landBattleMap import LandBattleMap
from battle.landUnitInBattle import LandUnitInBattle
from config.config import Config
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QApplication
from base.constants import version
CONFIG_FILE = 'config.ini'


class LandBattleResult(QWidget):
    """Class LandBattle
    """
    def __init__(self, config):
        self.config = config
        super().__init__()
        self.setWindowTitle(config.get_text('victory'))


if __name__ == '__main__':
    v = version()
    app = QApplication(sys.argv)
    config = Config(CONFIG_FILE,v)
    rst = LandBattleResult(config)
    rst.show()
    sys.exit(app.exec_())