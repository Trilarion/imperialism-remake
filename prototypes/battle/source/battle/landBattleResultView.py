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

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QGraphicsView, QGraphicsScene, QLabel

from base.constants import version
from config.config import Config

CONFIG_FILE = 'config.ini'


class LandBattleResultView(QWidget):
    """Class LandBattle
    """

    def __init__(self, conf, defeat):
        self.config = conf
        super().__init__()
        self.setWindowTitle(conf.get_text('victory'))
        self.setFixedSize(QSize(640, 480))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.FramelessWindowHint)
        button = QPushButton(conf.get_text('close'), self)
        button.setCheckable(True)
        button.setFixedSize(QSize(640, 30))
        button.move(0, 450)
        # noinspection PyUnresolvedReferences
        button.clicked.connect(self.close)
        result_output = QTextEdit(self)
        result_output.setReadOnly(True)
        result_output.setFixedSize(QSize(640, 200))
        result_output.move(0, 250)
        result_output.setLineWrapMode(QTextEdit.NoWrap)
        result_output.insertHtml(self.generate_result_text())
        gview = QGraphicsView(self)
        scene = QGraphicsScene()
        if defeat:
            img = conf.theme_selected.get_defeat_pixmap()
            text = conf.get_text('defeat')
        else:
            img = conf.theme_selected.get_victory_pixmap()
            text = conf.get_text('victory')
        scene.addPixmap(img.scaled(QSize(640, 220)))
        gview.move(0, 30)
        gview.setScene(scene)
        label_title = QLabel(self)
        label_title.setText(text)
        label_title.setFixedSize(QSize(640, 30))
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(self.get_font_title())

    @staticmethod
    def get_font_title():
        font = QFont()
        font.setPointSize(15)
        font.setWeight(75)
        font.setBold(True)
        return font

    @staticmethod
    def generate_result_text():
        return '<center><h1>TODO</h1><br/><h2>TODO</h2>TODO</center>'

    def closeEvent(self, event):
        event.ignore()

    def close(self):
        self.close()


if __name__ == '__main__':
    v = version()
    app = QApplication(sys.argv)
    config = Config(CONFIG_FILE, v)
    rst = LandBattleResultView(config, False)
    rst.show()
    sys.exit(app.exec_())
