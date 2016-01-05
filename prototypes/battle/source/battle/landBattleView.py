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

import math

from PyQt5.QtCore import QSize, Qt, QObject, QMetaObject, QPointF
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QPushButton, QGridLayout, QLabel, QSpacerItem, QSizePolicy, \
    QGraphicsScene, QGraphicsView, QMainWindow

from base import constants
from base.config import Config
from battle.landArmy import LandArmy
from battle.landBattle import LandBattle
from battle.landUnitInBattle import LandUnitInBattle

CONFIG_FILE = 'config.ini'

class MainBattleWindows(QMainWindow):
    def __init__(self, parent=None):
        super(MainBattleWindows, self).__init__(parent)
        self.ui = LandBattleView(self, None)
        self.config = self.ui.config
        self.ui.setup_ui()

    def resizeEvent(self, evt=None):
        self.ui.resize_event()

    def show(self):
        if self.config is None:
            self.showMaximized()
        elif self.config.show_fullscreen():
            self.showFullScreen()
        elif self.config.maximize():
            self.showMaximized()
        else:
            self.resize(self.config.get_resolution_qsize())
            self.showNormal()
        self.resizeEvent()

    def closeEvent(self, event):
        result = QMessageBox.question(self,
                                      self.config.get_string('exit.window.title'),
                                      self.config.get_string('exit.window.content'),
                                      QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.No:
            event.ignore()


class MainQGraphicsScene(QGraphicsScene):
    def __init__(self):
        self.landBattle = None
        super(MainQGraphicsScene, self).__init__()

    def mousePressEvent(self, event):
        position = QPointF(event.scenePos())
        if self.landBattle is not None:
            x, y = self.landBattle.map.position_to_grid_position(position)
            if x >= 0 and y >= 0:
                print('TODO mouse click on grid ' + str(x) + ';' + str(y))
                # if ev.button() == Qt.LeftButton:
                #    item = QtGui.QGraphicsTextItem("CLICK")
                #    item.setPos(ev.scenePos())
                #    self.addItem(item)

    def set_land_battle(self, land_battle):
        self.landBattle = land_battle


class LandBattleView(QObject):
    """Class LandBattleView
    """

    def __init__(self, battle_window, parent=None):
        super().__init__(parent)
        self.config = Config(CONFIG_FILE)
        if self.config.error_msg != '':
            QMessageBox.critical(battle_window, 'Configuration Error', self.config.error_msg)
            exit(-1)
        self.BattleWindow = battle_window
        self.centralWidget = QWidget(self.BattleWindow)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.coatOfArmsGraphicsScene = QGraphicsScene()
        self.currentUnitGraphicsScene = QGraphicsScene()
        self.targetedUnitGraphicsScene = QGraphicsScene()
        self.mainScene = MainQGraphicsScene()
        self.graphicsView_coatOfArm = QGraphicsView(self.coatOfArmsGraphicsScene)
        self.graphicsView_currentUnit = QGraphicsView(self.currentUnitGraphicsScene)
        self.graphicsView_targetedUnit = QGraphicsView(self.targetedUnitGraphicsScene)
        self.graphicsView_main = QGraphicsView(self.mainScene)
        self.autoCombatButton = CustomButton(self.centralWidget)
        self.helpButton = CustomButton(self.centralWidget)
        self.retreatButton = CustomButton(self.centralWidget)
        self.endUnitTurnButton = CustomButton(self.centralWidget)
        self.nextTargetButton = CustomButton(self.centralWidget)
        for button in self.autoCombatButton, self.helpButton, self.retreatButton, \
                      self.nextTargetButton, self.endUnitTurnButton:
            button.add_action_leave(self.clear_label_hint)
            button.add_action_enter(self.set_label_hint)
            button.add_action_click(self.click_button)
        self.dateLabel = QLabel(self.centralWidget)
        self.buttonHintLabel = QLabel(self.centralWidget)
        self.gridLayout.addWidget(self.graphicsView_main, 1, 0, 12, 1)
        # start testcase only
        nation_uk = self.config.get_nation("uk")
        nation_fr = self.config.get_nation("france")
        nation_fr.computer = True
        unit_type = self.config.get_unit_type('Militia I')
        current_unit = LandUnitInBattle(False, 'Charge', False, 50, 25, 1, unit_type, nation_fr)
        targetted_unit = LandUnitInBattle(False, 'Shoot', False, 75, 50, 1, unit_type, nation_uk)
        defender = LandArmy(False, None, nation_uk)
        attacker = LandArmy(False, None, nation_fr)
        # end testcase only
        self.landBattle = LandBattle(self.config, False, 0, current_unit, targetted_unit, defender, attacker)
        self.mainScene.set_land_battle(self.landBattle)

    def setup_hint_label(self):
        size_policy = constants.default_size_policy(self.buttonHintLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.buttonHintLabel.setSizePolicy(size_policy)
        self.buttonHintLabel.setFont(constants.default_font())
        self.buttonHintLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.buttonHintLabel, 0, 0, 1, 1)

    def setup_date_label(self, date, money):
        size_policy = constants.default_size_policy(self.dateLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.dateLabel.setSizePolicy(size_policy)
        self.dateLabel.setFont(constants.default_font())
        self.dateLabel.setText(str(date) + "\t\t$" + constants.format_money(money))
        self.dateLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.dateLabel, 0, 0, 1, 1)

    def setup_space(self):
        # Space between help Button and flag view
        spacer_item = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacer_item, 2, 1, 1, 1)
        # Space between flag view and next target Button
        spacer_item1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacer_item1, 4, 1, 1, 1)
        # Space between retreat Button and targetted unit view
        spacer_item2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacer_item2, 8, 1, 1, 1)
        # Space between current unit view and auto Button
        spacer_item3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacer_item3, 11, 1, 1, 1)

    def setup_next_target_button(self):

        size_policy = constants.default_size_policy(self.nextTargetButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.nextTargetButton.setSizePolicy(size_policy)
        self.nextTargetButton.setMinimumSize(QSize(45, 45))
        self.nextTargetButton.setMaximumSize(QSize(45, 45))
        self.nextTargetButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(self.config.theme_selected.get_target_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.nextTargetButton.setIcon(icon)
        self.nextTargetButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.nextTargetButton, 5, 1, 1, 1, Qt.AlignCenter)

    def setup_end_unit_button(self):
        size_policy = constants.default_size_policy(self.endUnitTurnButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.endUnitTurnButton.setSizePolicy(size_policy)
        self.endUnitTurnButton.setMinimumSize(QSize(45, 45))
        self.endUnitTurnButton.setMaximumSize(QSize(45, 45))
        self.endUnitTurnButton.setText("")
        icon1 = QIcon()
        icon1.addPixmap(self.config.theme_selected.get_end_button_pixmap(), QIcon.Normal, QIcon.Off)
        self.endUnitTurnButton.setIcon(icon1)
        self.endUnitTurnButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.endUnitTurnButton, 6, 1, 1, 1, Qt.AlignCenter)

    def setup_retreat_button(self):
        size_policy = constants.default_size_policy(self.retreatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.retreatButton.setSizePolicy(size_policy)
        self.retreatButton.setMinimumSize(QSize(45, 45))
        self.retreatButton.setMaximumSize(QSize(45, 45))
        self.retreatButton.setToolTip("")
        self.retreatButton.setWhatsThis("")
        self.retreatButton.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(self.config.theme_selected.get_retreat_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.retreatButton.setIcon(icon2)
        self.retreatButton.setIconSize(QSize(42, 40))
        self.gridLayout.addWidget(self.retreatButton, 7, 1, 1, 1, Qt.AlignCenter)

    def setup_help_button(self):
        size_policy = constants.default_size_policy(self.helpButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.helpButton.setSizePolicy(size_policy)
        self.helpButton.setMinimumSize(QSize(80, 80))
        self.helpButton.setMaximumSize(QSize(80, 80))
        self.helpButton.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(self.config.theme_selected.get_help_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.helpButton.setIcon(icon3)
        self.helpButton.setIconSize(QSize(75, 75))
        self.gridLayout.addWidget(self.helpButton, 0, 1, 2, 1)

    def setup_auto_combat_button(self):
        size_policy = constants.default_size_policy(self.autoCombatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.autoCombatButton.setSizePolicy(size_policy)
        self.autoCombatButton.setMinimumSize(QSize(90, 90))
        self.autoCombatButton.setMaximumSize(QSize(90, 90))
        self.autoCombatButton.setText("")
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(self.config.theme_selected.get_autocombat_button_pixmap()), QIcon.Normal, QIcon.Off)
        self.autoCombatButton.setIcon(icon4)
        self.autoCombatButton.setIconSize(QSize(80, 80))
        self.gridLayout.addWidget(self.autoCombatButton, 12, 1, 1, 1)

    def setup_targeted_unit_view(self):
        size = QSize(60, 60)
        nation = self.landBattle.defender.nation
        defending = False
        if self.landBattle.attacker.nation.computer:
            nation = self.landBattle.attacker.nation
            defending = True
        self.landBattle.draw_targetted_unit(defending, self.targetedUnitGraphicsScene, size)
        size_policy = constants.default_size_policy(self.graphicsView_targetedUnit, QSizePolicy.Fixed,
                                                    QSizePolicy.Fixed)
        self.graphicsView_targetedUnit.setSizePolicy(size_policy)
        self.graphicsView_targetedUnit.setMinimumSize(size)
        self.graphicsView_targetedUnit.setMaximumSize(size)
        self.gridLayout.addWidget(self.graphicsView_targetedUnit, 9, 1, 1, 1, Qt.AlignCenter)

    def setup_current_unit_view(self):
        size = QSize(60, 60)
        nation = self.landBattle.defender.nation
        nation = self.landBattle.defender.nation
        defending = False
        if not self.landBattle.attacker.nation.computer:
            nation = self.landBattle.attacker.nation
            defending = True
        self.landBattle.draw_current_unit(nation, defending, self.currentUnitGraphicsScene, size)
        size_policy = constants.default_size_policy(self.graphicsView_currentUnit, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_currentUnit.setSizePolicy(size_policy)
        self.graphicsView_currentUnit.setMinimumSize(size)
        self.graphicsView_currentUnit.setMaximumSize(size)
        self.gridLayout.addWidget(self.graphicsView_currentUnit, 10, 1, 1, 1, Qt.AlignCenter)

    def setup_coat_of_arms_view(self):
        size = QSize(90, 120)
        self.landBattle.draw_coat_of_arms(self.coatOfArmsGraphicsScene, size)
        self.graphicsView_coatOfArm.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        size_policy = constants.default_size_policy(self.graphicsView_coatOfArm, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_coatOfArm.setSizePolicy(size_policy)
        self.graphicsView_coatOfArm.setMinimumSize(size)
        self.graphicsView_coatOfArm.setMaximumSize(size)
        self.graphicsView_coatOfArm.setStyleSheet("border-style: none;background: transparent")
        self.graphicsView_coatOfArm.setCacheMode(QGraphicsView.CacheBackground)
        self.gridLayout.addWidget(self.graphicsView_coatOfArm, 3, 1, 1, 1)

    def setup_map(self):
        self.mainScene = MainQGraphicsScene()
        self.graphicsView_main.setScene(self.mainScene)
        self.mainScene.set_land_battle(self.landBattle)
        width = 2 * self.graphicsView_main.height() / math.sqrt(3)
        height = self.graphicsView_main.height()
        if width > self.graphicsView_main.width():
            width = self.graphicsView_main.width()
            height = self.graphicsView_main.width() * math.sqrt(3) / 2
        item = self.mainScene.addRect(0, 0, width - 15, height - 15)
        item.hide()
        self.landBattle.draw_battle_map(self.mainScene)

    def setup_ui(self):
        self.BattleWindow.setWindowTitle(self.config.get_string('battle.window.title'))
        background = self.config.theme_selected.get_background_pixmap()
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.BattleWindow.setMinimumSize(Config.get_min_resolution_qsize())
        self.BattleWindow.setAutoFillBackground(True)
        self.gridLayout.setVerticalSpacing(0)
        # Label
        self.setup_hint_label()
        self.setup_date_label("Spring, 1811", 10000)
        # Space item
        self.setup_space()
        # Help Push Button
        self.setup_help_button()
        # Next Target Button
        self.setup_next_target_button()
        # End Unit Button
        self.setup_end_unit_button()
        # Retreat Button
        self.setup_retreat_button()
        # Automatic battle button
        self.setup_auto_combat_button()
        # Targeted Unit view
        self.setup_targeted_unit_view()
        # Current Unit View
        self.setup_current_unit_view()
        # Coat of Arm view
        self.setup_coat_of_arms_view()
        # Main view
        self.setup_map()
        self.BattleWindow.setPalette(palette)
        self.BattleWindow.setCentralWidget(self.centralWidget)
        QMetaObject.connectSlotsByName(self.BattleWindow)


    def resize_event(self):
        self.setup_map()

    def clear_label_hint(self, custom_button):
        self.buttonHintLabel.setText('')

    def set_label_hint(self, custom_button):
        text = ''
        if custom_button == self.autoCombatButton:
            text = self.config.get_string('auto.play.label')
        elif custom_button == self.helpButton:
            text = self.config.get_string('help.tacticalbattle.label')
        elif custom_button == self.retreatButton:
            text = self.config.get_string('retreat.all.label')
        elif custom_button == self.endUnitTurnButton:
            text = self.config.get_string('end.unit.label')
        elif custom_button == self.nextTargetButton:
            text = self.config.get_string('next.target.label')
        if text != '':
            self.buttonHintLabel.setText(text)

    def click_button(self, custom_button):
        if custom_button == self.autoCombatButton:
            print('click autoCombatButton')
        elif custom_button == self.helpButton:
            print('click helpButton')
        elif custom_button == self.retreatButton:
            print('click retreatButton')
        elif custom_button == self.endUnitTurnButton:
            print('click endUnitTurnButton')
        elif custom_button == self.nextTargetButton:
            print('click nextTargetButton')


class CustomButton(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.enter_functions = []
        self.leave_functions = []
        self.click_functions = []
        super().clicked.connect(self.click)

    def enterEvent(self, event):
        for f in self.enter_functions:
            f(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        for f in self.leave_functions:
            f(self)
        super().leaveEvent(event)

    def click(self):
        for f in self.click_functions:
            f(self)

    def add_action_enter(self, enter_function):
        self.enter_functions.append(enter_function)

    def add_action_leave(self, leave_function):
        self.leave_functions.append(leave_function)

    def add_action_click(self, click_function):
        self.click_functions.append(click_function)

    def clear_action_enter(self):
        self.enter_functions = []

    def clear_action_leave(self):
        self.leave_functions = []

    def clear_action_click(self, click_function):
        self.click_functions = []
