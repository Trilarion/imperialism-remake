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

import random

from PyQt5.QtCore import QSize, Qt, QObject
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QSpacerItem, QSizePolicy, QGraphicsScene, \
    QGraphicsRectItem, QGraphicsView

from base import Constants as Const


class LandBattleView(QObject):
    def __init__(self, battle_window, parent=None):
        super().__init__(parent)
        self.BattleWindow = battle_window
        self.centralWidget = QWidget(self.BattleWindow)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.coatOfArmGraphicsScene = QGraphicsScene()
        self.currentUnitGraphicsScene = QGraphicsScene()
        self.targetedUnitGraphicsScene = QGraphicsScene()
        self.graphicsView_coatOfArm = QGraphicsView(self.coatOfArmGraphicsScene)
        self.graphicsView_currentUnit = QGraphicsView(self.currentUnitGraphicsScene)
        self.graphicsView_targetedUnit = QGraphicsView(self.targetedUnitGraphicsScene)
        self.autoCombatButton = CustomButton(self.centralWidget)
        self.helpButton = CustomButton(self.centralWidget)
        self.retreatButton = CustomButton(self.centralWidget)
        self.endUnitTurnButton = CustomButton(self.centralWidget)
        self.nextTargetButton = CustomButton(self.centralWidget)
        self.dateLabel = QLabel(self.centralWidget)
        self.buttonHintLabel = QLabel(self.centralWidget)

    def setup_hint_label(self):
        size_policy = Const.default_size_policy(self.buttonHintLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.buttonHintLabel.setSizePolicy(size_policy)
        self.buttonHintLabel.setFont(Const.default_font())
        self.buttonHintLabel.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.gridLayout.addWidget(self.buttonHintLabel, 0, 0, 1, 1)

    def setup_date_label(self, date, money):
        size_policy = Const.default_size_policy(self.dateLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.dateLabel.setSizePolicy(size_policy)
        self.dateLabel.setFont(Const.default_font())
        self.dateLabel.setText(str(date) + "\t\t$" + Const.format_money(money))
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
        self.nextTargetButton.setbutton_hint_label_text("Next Target", self.buttonHintLabel)
        size_policy = Const.default_size_policy(self.nextTargetButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.nextTargetButton.setSizePolicy(size_policy)
        self.nextTargetButton.setMinimumSize(QSize(45, 45))
        self.nextTargetButton.setMaximumSize(QSize(45, 45))
        self.nextTargetButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(Const.Graphics_Target), QIcon.Normal, QIcon.Off)
        self.nextTargetButton.setIcon(icon)
        self.nextTargetButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.nextTargetButton, 5, 1, 1, 1, Qt.AlignCenter)

    def setup_end_unit_button(self):
        self.endUnitTurnButton.setbutton_hint_label_text("End Unit's Turn", self.buttonHintLabel)
        size_policy = Const.default_size_policy(self.endUnitTurnButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.endUnitTurnButton.setSizePolicy(size_policy)
        self.endUnitTurnButton.setMinimumSize(QSize(45, 45))
        self.endUnitTurnButton.setMaximumSize(QSize(45, 45))
        self.endUnitTurnButton.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(Const.Graphics_End), QIcon.Normal, QIcon.Off)
        self.endUnitTurnButton.setIcon(icon1)
        self.endUnitTurnButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.endUnitTurnButton, 6, 1, 1, 1, Qt.AlignCenter)

    def setup_retreat_button(self):
        self.retreatButton.setbutton_hint_label_text("retreat All Units", self.buttonHintLabel)
        size_policy = Const.default_size_policy(self.retreatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.retreatButton.setSizePolicy(size_policy)
        self.retreatButton.setMinimumSize(QSize(45, 45))
        self.retreatButton.setMaximumSize(QSize(45, 45))
        self.retreatButton.setToolTip("")
        self.retreatButton.setWhatsThis("")
        self.retreatButton.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(Const.Graphics_Retreat), QIcon.Normal, QIcon.Off)
        self.retreatButton.setIcon(icon2)
        self.retreatButton.setIconSize(QSize(42, 40))
        self.gridLayout.addWidget(self.retreatButton, 7, 1, 1, 1, Qt.AlignCenter)

    def setup_help_button(self):
        self.helpButton.setbutton_hint_label_text("Help on Tactical Battles", self.buttonHintLabel)
        size_policy = Const.default_size_policy(self.helpButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.helpButton.setSizePolicy(size_policy)
        self.helpButton.setMinimumSize(QSize(80, 80))
        self.helpButton.setMaximumSize(QSize(80, 80))
        self.helpButton.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(Const.Graphics_Help), QIcon.Normal, QIcon.Off)
        self.helpButton.setIcon(icon3)
        self.helpButton.setIconSize(QSize(75, 75))
        self.gridLayout.addWidget(self.helpButton, 0, 1, 2, 1)

    def setup_auto_combat_button(self):
        self.autoCombatButton.setbutton_hint_label_text("Auto-Play", self.buttonHintLabel)
        size_policy = Const.default_size_policy(self.autoCombatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.autoCombatButton.setSizePolicy(size_policy)
        self.autoCombatButton.setMinimumSize(QSize(90, 90))
        self.autoCombatButton.setMaximumSize(QSize(90, 90))
        self.autoCombatButton.setText("")
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(Const.Graphics_General), QIcon.Normal, QIcon.Off)
        self.autoCombatButton.setIcon(icon4)
        self.autoCombatButton.setIconSize(QSize(80, 80))
        self.gridLayout.addWidget(self.autoCombatButton, 12, 1, 1, 1)

    def add_unit(self, scene, size, unit_pixmap_path, flag_pixmap_path, miror):
        unit_pixmap = QPixmap(unit_pixmap_path).scaled(size * 90 / 100, size * 90 / 100)
        if miror:
            unit_pixmap = Const.miror_pixmap(unit_pixmap)
        scene.addPixmap(unit_pixmap)
        item = scene.addPixmap(Const.miror_pixmap(QPixmap(flag_pixmap_path)).scaled(size * 23 / 100, 13 / 100 * size))
        item.setPos(0, 80 / 100 * size)
        item1 = QGraphicsRectItem(0, 0, size * 60 / 100, 5)
        item1.setBrush(QBrush(Qt.green))
        item1.setPos(size * 25 / 100, 81 / 100 * size)
        scene.addItem(item1)

    def setup_targeted_unit_view(self, targeted_unit):
        self.add_unit(self.targetedUnitGraphicsScene, 60, targeted_unit, Const.Flag_of_France, True)
        size_policy = Const.default_size_policy(self.graphicsView_targetedUnit, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_targetedUnit.setSizePolicy(size_policy)
        self.graphicsView_targetedUnit.setMinimumSize(QSize(60, 60))
        self.graphicsView_targetedUnit.setMaximumSize(QSize(60, 60))
        self.gridLayout.addWidget(self.graphicsView_targetedUnit, 9, 1, 1, 1, Qt.AlignCenter)

    def setup_current_unit_view(self, current_unit):
        self.add_unit(self.currentUnitGraphicsScene, 60, current_unit, Const.Flag_of_Spain, False)
        size_policy = Const.default_size_policy(self.graphicsView_currentUnit, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_currentUnit.setSizePolicy(size_policy)
        self.graphicsView_currentUnit.setMinimumSize(QSize(60, 60))
        self.graphicsView_currentUnit.setMaximumSize(QSize(60, 60))
        self.gridLayout.addWidget(self.graphicsView_currentUnit, 10, 1, 1, 1, Qt.AlignCenter)

    def setup_coat_of_arm_view(self, coat_of_arm_attacker):
        img = QPixmap(coat_of_arm_attacker).scaled(90, 120)
        self.coatOfArmGraphicsScene.addPixmap(img)
        self.graphicsView_coatOfArm.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        size_policy = Const.default_size_policy(self.graphicsView_coatOfArm, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_coatOfArm.setSizePolicy(size_policy)
        self.graphicsView_coatOfArm.setMinimumSize(QSize(90, 120))
        self.graphicsView_coatOfArm.setMaximumSize(QSize(90, 120))
        self.graphicsView_coatOfArm.setStyleSheet("border-style: none;background: transparent")
        self.graphicsView_coatOfArm.setCacheMode(QGraphicsView.CacheBackground)
        self.gridLayout.addWidget(self.graphicsView_coatOfArm, 3, 1, 1, 1)

    def setup_map(self):
        print("TODO... setupMap")
        # bmap = map.battle_map.BattleMap()
        # self.graphicsView = map.battle_map.BattleMapView(bmap)
        # self.gridLayout.addWidget(self.graphicsView, 1, 0, 12, 1)
        # self.graphicsView.redraw_map()

    def setup_ui(self):
        self.BattleWindow.setWindowTitle("BattleWindow")
        background = QPixmap(Const.Graphics_Background)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.BattleWindow.setMinimumSize(QSize(Const.Screen_Min_Size[0], Const.Screen_Min_Size[1]))
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
        self.setup_targeted_unit_view(random.choice(Const.Graphics_Unit_list))
        # Current Unit View
        self.setup_current_unit_view(random.choice(Const.Graphics_Unit_list))
        # Coat of Arm view
        self.setup_coat_of_arm_view(random.choice(Const.Graphics_Coat_of_arms_list))
        # Main view
        self.setup_map()
        self.BattleWindow.setPalette(palette)
        self.BattleWindow.setCentralWidget(self.centralWidget)


class CustomButton(QPushButton):
    text = ""

    def __init__(self, *__args):
        super().__init__(*__args)
        self.label = None

    def setbutton_hint_label_text(self, text, label):
        self.text = text
        self.label = label

    def enterEvent(self, event):
        if self.label is not None:
            self.label.setText(str(self.text) + "  ")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.label.setText("")
        super().leaveEvent(event)
