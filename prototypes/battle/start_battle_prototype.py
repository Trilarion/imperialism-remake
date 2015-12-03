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

import sys, math, random, map.battle_map
from base import constants as c
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QGridLayout, QLabel, QSizePolicy, QSpacerItem, QSizePolicy,  QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QIcon,  QTransform
from PyQt5.QtCore import QSize, Qt, QMetaObject

def formatMoney(money):
    str_init = str(money)
    retval = ""
    for i in range(0,len(str_init)):
        if (len(str_init) - i) % 3 == 0 and i != 0:
            retval += ","
        retval += str_init[i]
    return retval;

class Ui_BattleWindow(object):


        
    def setupZoneText(self, date, money):
        self.status = QLabel(self.centralWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.status.setFont(font)
        self.status.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.status, 0, 0, 1, 1)   
        self.status1 = QLabel(self.centralWidget)
        self.status1.setSizePolicy(sizePolicy)
        self.status1.setFont(font)
        self.status1.setText(str(date) + "\t\t$" + formatMoney(money))
        self.status1.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.gridLayout.addWidget(self.status1, 0, 0, 1, 1)   
  


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
        self.pushButton_NextTarget = CustomButton(self.centralWidget)
        self.pushButton_NextTarget.setStatusText("Next Target",self.status)
        sizePolicy= QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_NextTarget.sizePolicy().hasHeightForWidth())
        self.pushButton_NextTarget.setSizePolicy(sizePolicy)
        self.pushButton_NextTarget.setMinimumSize(QSize(45, 45))
        self.pushButton_NextTarget.setMaximumSize(QSize(45, 45))
        self.pushButton_NextTarget.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(c.Graphics_Target), QIcon.Normal, QIcon.Off)
        self.pushButton_NextTarget.setIcon(icon)
        self.pushButton_NextTarget.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.pushButton_NextTarget, 5, 1, 1, 1,Qt.AlignCenter)
      
      
    def setupEndUnitButton(self):
        self.pushButton_endUnitTurn = CustomButton(self.centralWidget)
        self.pushButton_endUnitTurn.setStatusText("End Unit's Turn",self.status)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_endUnitTurn.sizePolicy().hasHeightForWidth())
        self.pushButton_endUnitTurn.setSizePolicy(sizePolicy)
        self.pushButton_endUnitTurn.setMinimumSize(QSize(45, 45))
        self.pushButton_endUnitTurn.setMaximumSize(QSize(45, 45))
        self.pushButton_endUnitTurn.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(c.Graphics_End), QIcon.Normal, QIcon.Off)
        self.pushButton_endUnitTurn.setIcon(icon1)
        self.pushButton_endUnitTurn.setIconSize(QSize(40, 40))
        self.gridLayout.addWidget(self.pushButton_endUnitTurn, 6, 1, 1, 1,Qt.AlignCenter)
      
      
    def setupRetreatButton(self):  
        self.pushButton_retreat = CustomButton(self.centralWidget)
        self.pushButton_retreat.setStatusText("retreat All Units",self.status)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_retreat.sizePolicy().hasHeightForWidth())
        self.pushButton_retreat.setSizePolicy(sizePolicy)
        self.pushButton_retreat.setMinimumSize(QSize(45, 45))
        self.pushButton_retreat.setMaximumSize(QSize(45, 45))
        self.pushButton_retreat.setToolTip("")
        self.pushButton_retreat.setStatusTip("")
        self.pushButton_retreat.setWhatsThis("")
        self.pushButton_retreat.setText("")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(c.Graphics_Retreat), QIcon.Normal, QIcon.Off)
        self.pushButton_retreat.setIcon(icon2)
        self.pushButton_retreat.setIconSize(QSize(42, 40))
        self.gridLayout.addWidget(self.pushButton_retreat, 7, 1, 1, 1,Qt.AlignCenter)
      

    def setupHelpButton(self):  
        self.pushButton_help = CustomButton(self.centralWidget)
        self.pushButton_help.setStatusText("Help on Tactical Battles",self.status)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_help.sizePolicy().hasHeightForWidth())
        self.pushButton_help.setSizePolicy(sizePolicy)
        self.pushButton_help.setMinimumSize(QSize(90, 90))
        self.pushButton_help.setMaximumSize(QSize(90, 90))
        self.pushButton_help.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(c.Graphics_Help), QIcon.Normal, QIcon.Off)
        self.pushButton_help.setIcon(icon3)
        self.pushButton_help.setIconSize(QSize(80, 80))
        self.gridLayout.addWidget(self.pushButton_help, 0, 1, 2, 1)   
        
    
    def setupAutoButton(self):
        self.pushButton_auto = CustomButton(self.centralWidget)
        self.pushButton_auto.setStatusText("Auto-Play",self.status)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_auto.sizePolicy().hasHeightForWidth())
        self.pushButton_auto.setSizePolicy(sizePolicy)
        self.pushButton_auto.setMinimumSize(QSize(90, 90))
        self.pushButton_auto.setMaximumSize(QSize(90, 90))
        self.pushButton_auto.setText("")
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(c.Graphics_General), QIcon.Normal, QIcon.Off)
        self.pushButton_auto.setIcon(icon4)
        self.pushButton_auto.setIconSize(QSize(80, 80))
        self.gridLayout.addWidget(self.pushButton_auto, 12, 1, 1, 1) 
       
        
        
    def setupTargetedUnitView(self,targetedUnit):
        self.graphicsScene_targetedUnit= QGraphicsScene()
        self.graphicsScene_targetedUnit.addPixmap(self.mirorPixmap(QPixmap(targetedUnit)).scaled(75, 75))
        self.graphicsView_targetedUnit = QGraphicsView(self.graphicsScene_targetedUnit)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_targetedUnit.sizePolicy().hasHeightForWidth())
        self.graphicsView_targetedUnit.setSizePolicy(sizePolicy)
        self.graphicsView_targetedUnit.setMinimumSize(QSize(90, 90))
        self.graphicsView_targetedUnit.setMaximumSize(QSize(90, 90))
        self.gridLayout.addWidget(self.graphicsView_targetedUnit, 9, 1, 1, 1,Qt.AlignCenter) 
        
    def setupCurrentUnitView(self,currentUnit):   
        self.graphicsScene_currentUnit= QGraphicsScene()
        self.graphicsScene_currentUnit.addPixmap(QPixmap(currentUnit).scaled(75, 75))
        self.graphicsView_currentUnit = QGraphicsView(self.graphicsScene_currentUnit)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_currentUnit.sizePolicy().hasHeightForWidth())
        self.graphicsView_currentUnit.setSizePolicy(sizePolicy)
        self.graphicsView_currentUnit.setMinimumSize(QSize(90, 90))
        self.graphicsView_currentUnit.setMaximumSize(QSize(90, 90))
        self.gridLayout.addWidget(self.graphicsView_currentUnit, 10, 1, 1, 1,Qt.AlignCenter)
       
       
    def mirorPixmap(self,pixmap):
        transform = QTransform()  
        transform.scale(-1, 1)
        return QPixmap(pixmap.transformed(transform))

    def setupFlagView(self,flag_attacker):
        self.graphicsScene_flag= QGraphicsScene()
        img = QPixmap(flag_attacker).scaled(90,120)
        self.graphicsScene_flag.addPixmap(img)         
        self.graphicsView_flag = QGraphicsView(self.graphicsScene_flag)
        self.graphicsView_flag.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_flag.sizePolicy().hasHeightForWidth())       
        self.graphicsView_flag.setSizePolicy(sizePolicy)
        self.graphicsView_flag.setMinimumSize(QSize(90, 120))
        self.graphicsView_flag.setMaximumSize(QSize(90, 120))
        self.graphicsView_flag.setStyleSheet("border-style: none;background: transparent")
        self.graphicsView_flag.setCacheMode(QGraphicsView.CacheBackground)
        self.gridLayout.addWidget(self.graphicsView_flag, 3, 1, 1, 1)       

        
    def setupMainView(self):
        bmap = map.battle_map.BattleMap()
        self.graphicsView = map.battle_map.BattleMapView(bmap)
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 12, 1)
        self.graphicsView.redraw_map()
    
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
        self.setupZoneText("Spring, 1811", 10000)
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
        self.setupAutoButton()
        #Targeted Unit view
        self.setupTargetedUnitView(random.choice(c.Graphics_Unit_list))
        #Current Unit View
        self.setupCurrentUnitView(random.choice(c.Graphics_Unit_list))
        #Flag view
        self.setupFlagView(random.choice(c.Graphics_Coat_of_arms_list))
        #Main view
        self.setupMainView()
        BattleWindow.setPalette(palette)
        BattleWindow.setCentralWidget(self.centralWidget)
        QMetaObject.connectSlotsByName(BattleWindow)
    

class CustomButton(QPushButton):
    text = ""
   

    def setStatusText(self, text, label):
        self.text = text
        self.label = label


    def enterEvent(self, event):
        self.label.setText(str(self.text) + "  ")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.label.setText("")
        super().leaveEvent(event)

class ControlMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_BattleWindow()
        self.ui.setupUi(self)


 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.showMaximized()
    sys.exit(app.exec_())
