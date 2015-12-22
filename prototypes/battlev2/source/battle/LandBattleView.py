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

from base import Constants as c
import random
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout, QLabel, QSizePolicy, QSpacerItem, QSizePolicy,  QGraphicsScene, QGraphicsRectItem, QGraphicsView
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QIcon,  QTransform
from PyQt5.QtCore import QSize, Qt, QMetaObject


class LandBattleView(object):
        
        
    def setupHintLabel(self):
        self.buttonHintLabel = QLabel(self.centralWidget)
        sizePolicy = c.defaultSizePolicy(self.buttonHintLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.buttonHintLabel.setSizePolicy(sizePolicy)
        self.buttonHintLabel.setFont(c.defaultFont())
        self.buttonHintLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.buttonHintLabel, 0, 0, 1, 1)      
        
        
    def setupDateLabel(self, date, money):
        self.dateLabel = QLabel(self.centralWidget)
        sizePolicy = c.defaultSizePolicy(self.dateLabel, QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.dateLabel.setSizePolicy(sizePolicy)
        self.dateLabel.setFont(c.defaultFont())
        self.dateLabel.setText(str(date) + "\t\t$" + c.formatMoney(money))
        self.dateLabel.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.dateLabel, 0, 0, 1, 1)   
  


    def setupSpace(self):
        #Space between help Button and flag view
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        #Space between flag view and next target Button
        spacerItem1 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        #Space between retreat Button and targetted unit view
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 8, 1, 1, 1)
        #Space between current unit view and auto Button
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacerItem3, 11, 1, 1, 1)

        
    def setupNextTargetButton(self):
        self.nextTargetButton = CustomButton(self.centralWidget)
        self.nextTargetButton.setbuttonHintLabelText("Next Target",self.buttonHintLabel)
        sizePolicy = c.defaultSizePolicy(self.nextTargetButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.nextTargetButton.setSizePolicy(sizePolicy)
        self.nextTargetButton.setMinimumSize(QSize(45, 45))
        self.nextTargetButton.setMaximumSize(QSize(45, 45))
        self.nextTargetButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(c.Graphics_Target), QIcon.Normal, QIcon.Off)
        self.nextTargetButton.setIcon(icon)
        self.nextTargetButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.nextTargetButton, 5, 1, 1, 1,Qt.AlignCenter)
      
      
    def setupEndUnitButton(self):
        self.endUnitTurnButton = CustomButton(self.centralWidget)
        self.endUnitTurnButton.setbuttonHintLabelText("End Unit's Turn",self.buttonHintLabel)
        sizePolicy = c.defaultSizePolicy(self.endUnitTurnButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.endUnitTurnButton.setSizePolicy(sizePolicy)
        self.endUnitTurnButton.setMinimumSize(QSize(45, 45))
        self.endUnitTurnButton.setMaximumSize(QSize(45, 45))
        self.endUnitTurnButton.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(c.Graphics_End), QIcon.Normal, QIcon.Off)
        self.endUnitTurnButton.setIcon(icon1)
        self.endUnitTurnButton.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.endUnitTurnButton, 6, 1, 1, 1,Qt.AlignCenter)
      
      
    def setupRetreatButton(self):  
        self.retreatButton = CustomButton(self.centralWidget)
        self.retreatButton.setbuttonHintLabelText("retreat All Units",self.buttonHintLabel)
        sizePolicy = c.defaultSizePolicy(self.retreatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.retreatButton.setSizePolicy(sizePolicy)
        self.retreatButton.setMinimumSize(QSize(45, 45))
        self.retreatButton.setMaximumSize(QSize(45, 45))
        self.retreatButton.setToolTip("")
        self.retreatButton.setWhatsThis("")
        self.retreatButton.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(c.Graphics_Retreat), QIcon.Normal, QIcon.Off)
        self.retreatButton.setIcon(icon2)
        self.retreatButton.setIconSize(QSize(42, 40))
        self.gridLayout.addWidget(self.retreatButton, 7, 1, 1, 1,Qt.AlignCenter)
      

    def setupHelpButton(self):  
        self.helpButton = CustomButton(self.centralWidget)
        self.helpButton.setbuttonHintLabelText("Help on Tactical Battles",self.buttonHintLabel)
        sizePolicy = c.defaultSizePolicy(self.helpButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.helpButton.setSizePolicy(sizePolicy)
        self.helpButton.setMinimumSize(QSize(80, 80))
        self.helpButton.setMaximumSize(QSize(80, 80))
        self.helpButton.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(c.Graphics_Help), QIcon.Normal, QIcon.Off)
        self.helpButton.setIcon(icon3)
        self.helpButton.setIconSize(QSize(75, 75))
        self.gridLayout.addWidget(self.helpButton, 0, 1, 2, 1)   
        
    
    def setupAutoCombatButton(self):
        self.autoCombatButton = CustomButton(self.centralWidget)
        self.autoCombatButton.setbuttonHintLabelText("Auto-Play",self.buttonHintLabel)
        sizePolicy = c.defaultSizePolicy(self.autoCombatButton, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.autoCombatButton.setSizePolicy(sizePolicy)
        self.autoCombatButton.setMinimumSize(QSize(90, 90))
        self.autoCombatButton.setMaximumSize(QSize(90, 90))
        self.autoCombatButton.setText("")
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(c.Graphics_General), QIcon.Normal, QIcon.Off)
        self.autoCombatButton.setIcon(icon4)
        self.autoCombatButton.setIconSize(QSize(80, 80))
        self.gridLayout.addWidget(self.autoCombatButton, 12, 1, 1, 1) 
       
    def addUnit(self, scene, size, unitPixmapPath, flagPixmapPath, miror):
        unitPixmap = QPixmap(unitPixmapPath).scaled(size * 90/100, size * 90/100)
        if miror:
            unitPixmap = c.mirorPixmap(unitPixmap)
        scene.addPixmap(unitPixmap)
        item = scene.addPixmap(c.mirorPixmap(QPixmap(flagPixmapPath)).scaled(size * 23/100, 13/100 * size))
        item.setPos(0,80/100 * size)
        item1 = QGraphicsRectItem(0,0,size * 60 / 100,5)
        item1.setBrush(QBrush(Qt.green))
        item1.setPos(size * 25/100,81/100 * size)
        scene.addItem(item1)
        
    def setupTargetedUnitView(self,targetedUnit):
        self.targetedUnitGraphicsScene= QGraphicsScene()
        self.addUnit(self.targetedUnitGraphicsScene, 60, targetedUnit, c.Flag_of_France, True)
        self.graphicsView_targetedUnit = QGraphicsView(self.targetedUnitGraphicsScene)
        sizePolicy = c.defaultSizePolicy(self.graphicsView_targetedUnit, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_targetedUnit.setSizePolicy(sizePolicy)
        self.graphicsView_targetedUnit.setMinimumSize(QSize(60, 60))
        self.graphicsView_targetedUnit.setMaximumSize(QSize(60, 60))
        self.gridLayout.addWidget(self.graphicsView_targetedUnit, 9, 1, 1, 1,Qt.AlignCenter) 
        
    def setupCurrentUnitView(self,currentUnit):   
        self.currentUnitGraphicsScene= QGraphicsScene()
        self.addUnit(self.currentUnitGraphicsScene, 60, currentUnit, c.Flag_of_Spain, False)
        self.graphicsView_currentUnit = QGraphicsView(self.currentUnitGraphicsScene)
        sizePolicy = c.defaultSizePolicy(self.graphicsView_currentUnit, QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.graphicsView_currentUnit.setSizePolicy(sizePolicy)
        self.graphicsView_currentUnit.setMinimumSize(QSize(60, 60))
        self.graphicsView_currentUnit.setMaximumSize(QSize(60, 60))
        self.gridLayout.addWidget(self.graphicsView_currentUnit, 10, 1, 1, 1,Qt.AlignCenter)
       

    def setupCoatOfArmView(self,coatOfArm_attacker):
        self.coatOfArmGraphicsScene= QGraphicsScene()
        img = QPixmap(coatOfArm_attacker).scaled(90,120)
        self.coatOfArmGraphicsScene.addPixmap(img)         
        self.graphicsView_coatOfArm = QGraphicsView(self.coatOfArmGraphicsScene)
        self.graphicsView_coatOfArm.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sizePolicy = c.defaultSizePolicy(self.graphicsView_coatOfArm, QSizePolicy.Fixed, QSizePolicy.Fixed)   
        self.graphicsView_coatOfArm.setSizePolicy(sizePolicy)
        self.graphicsView_coatOfArm.setMinimumSize(QSize(90, 120))
        self.graphicsView_coatOfArm.setMaximumSize(QSize(90, 120))
        self.graphicsView_coatOfArm.setStyleSheet("border-style: none;background: transparent")
        self.graphicsView_coatOfArm.setCacheMode(QGraphicsView.CacheBackground)
        self.gridLayout.addWidget(self.graphicsView_coatOfArm, 3, 1, 1, 1)       

        
    def setupMap(self):
        print("TODO... setupMap")
        #bmap = map.battle_map.BattleMap()
        #self.graphicsView = map.battle_map.BattleMapView(bmap)
        #self.gridLayout.addWidget(self.graphicsView, 1, 0, 12, 1)
        #self.graphicsView.redraw_map()
    
    def setupUi(self, BattleWindow):
        BattleWindow.setWindowTitle("BattleWindow")
        background =  QPixmap(c.Graphics_Background)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(background))
        BattleWindow.setMinimumSize(QSize(c.Screen_Min_Size[0],c.Screen_Min_Size[1]))
        BattleWindow.setAutoFillBackground(True)
        self.centralWidget = QWidget(BattleWindow)
        self.gridLayout = QGridLayout(self.centralWidget)
        self.gridLayout.setVerticalSpacing(0)
        #Label
        self.setupHintLabel()
        self.setupDateLabel("Spring, 1811", 10000)
        #Space item
        self.setupSpace()
        #Help Push Button
        self.setupHelpButton()
        #Next Target Button
        self.setupNextTargetButton()
        #End Unit Button
        self.setupEndUnitButton()
        #Retreat Button
        self.setupRetreatButton()
        #Automatic battle button
        self.setupAutoCombatButton()
        #Targeted Unit view
        self.setupTargetedUnitView(random.choice(c.Graphics_Unit_list))
        #Current Unit View
        self.setupCurrentUnitView(random.choice(c.Graphics_Unit_list))
        #Coat of Arm view
        self.setupCoatOfArmView(random.choice(c.Graphics_Coat_of_arms_list))
        #Main view
        self.setupMap()
        BattleWindow.setPalette(palette)
        BattleWindow.setCentralWidget(self.centralWidget)
        QMetaObject.connectSlotsByName(BattleWindow)
    

class CustomButton(QPushButton):
    text = ""
   

    def setbuttonHintLabelText(self, text, label):
        self.text = text
        self.label = label


    def enterEvent(self, event):
        self.label.setText(str(self.text) + "  ")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.label.setText("")
        super().leaveEvent(event)