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
from PySide import QtCore, QtGui

class Ui_BattleWindow(object):


    def setupSpace(self):
        #Space between help Button and flag view
        spacerItem = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        #Space between flag view and next target Button
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacerItem1, 4, 1, 1, 1)
        #Space between retreat Button and targetted unit view
        spacerItem2 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 8, 1, 1, 1)
        #Space between current unit view and auto Button
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.gridLayout.addItem(spacerItem3, 11, 1, 1, 1)

        
    def setupNextTargetButton(self):
        self.pushButton_NextTarget = QtGui.QPushButton(self.centralWidget)
        sizePolicy= QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_NextTarget.sizePolicy().hasHeightForWidth())
        self.pushButton_NextTarget.setSizePolicy(sizePolicy)
        self.pushButton_NextTarget.setMinimumSize(QtCore.QSize(45, 45))
        self.pushButton_NextTarget.setMaximumSize(QtCore.QSize(45, 45))
        self.pushButton_NextTarget.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("res/target.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_NextTarget.setIcon(icon)
        self.pushButton_NextTarget.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_NextTarget.setObjectName("pushButton_NextTarget")
        self.gridLayout.addWidget(self.pushButton_NextTarget, 5, 1, 1, 1,QtCore.Qt.AlignCenter)
      
      
    def setupEndUnitButton(self):
        self.pushButton_endUnitTurn = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_endUnitTurn.sizePolicy().hasHeightForWidth())
        self.pushButton_endUnitTurn.setSizePolicy(sizePolicy)
        self.pushButton_endUnitTurn.setMinimumSize(QtCore.QSize(45, 45))
        self.pushButton_endUnitTurn.setMaximumSize(QtCore.QSize(45, 45))
        self.pushButton_endUnitTurn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("res/end.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_endUnitTurn.setIcon(icon1)
        self.pushButton_endUnitTurn.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_endUnitTurn.setObjectName("pushButton_endUnitTurn")
        self.gridLayout.addWidget(self.pushButton_endUnitTurn, 6, 1, 1, 1,QtCore.Qt.AlignCenter)
      
      
    def setupRetreatButton(self):  
        self.pushButton_retreat = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_retreat.sizePolicy().hasHeightForWidth())
        self.pushButton_retreat.setSizePolicy(sizePolicy)
        self.pushButton_retreat.setMinimumSize(QtCore.QSize(45, 45))
        self.pushButton_retreat.setMaximumSize(QtCore.QSize(45, 45))
        self.pushButton_retreat.setToolTip("")
        self.pushButton_retreat.setStatusTip("")
        self.pushButton_retreat.setWhatsThis("")
        self.pushButton_retreat.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("res/retreat.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_retreat.setIcon(icon2)
        self.pushButton_retreat.setIconSize(QtCore.QSize(42, 40))
        self.pushButton_retreat.setObjectName("pushButton_retreat")
        self.gridLayout.addWidget(self.pushButton_retreat, 7, 1, 1, 1,QtCore.Qt.AlignCenter)
      

    def setupHelpButton(self):  
        self.pushButton_help = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_help.sizePolicy().hasHeightForWidth())
        self.pushButton_help.setSizePolicy(sizePolicy)
        self.pushButton_help.setMinimumSize(QtCore.QSize(90, 90))
        self.pushButton_help.setMaximumSize(QtCore.QSize(90, 90))
        self.pushButton_help.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("res/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_help.setIcon(icon3)
        self.pushButton_help.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_help.setObjectName("pushButton_help")
        self.gridLayout.addWidget(self.pushButton_help, 0, 1, 2, 1)   
        
    
    def setupAutoButton(self):
        self.pushButton_auto = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_auto.sizePolicy().hasHeightForWidth())
        self.pushButton_auto.setSizePolicy(sizePolicy)
        self.pushButton_auto.setMinimumSize(QtCore.QSize(90, 90))
        self.pushButton_auto.setMaximumSize(QtCore.QSize(90, 90))
        self.pushButton_auto.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("res/general.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_auto.setIcon(icon4)
        self.pushButton_auto.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_auto.setObjectName("pushButton_auto")
        self.gridLayout.addWidget(self.pushButton_auto, 12, 1, 1, 1) 
        
        
    def setupZoneText(self):
        self.status = QtGui.QLabel(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.status.setFont(font)
        self.status.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.status.setObjectName("status")
        self.gridLayout.addWidget(self.status, 0, 0, 1, 1)     
        
        
    def setupTargetedUnitView(self):
        self.graphicsView_targetedUnit = QtGui.QGraphicsView(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_targetedUnit.sizePolicy().hasHeightForWidth())
        self.graphicsView_targetedUnit.setSizePolicy(sizePolicy)
        self.graphicsView_targetedUnit.setMinimumSize(QtCore.QSize(50, 50))
        self.graphicsView_targetedUnit.setMaximumSize(QtCore.QSize(50, 50))
        self.graphicsView_targetedUnit.setObjectName("graphicsView_targetedUnit")
        self.gridLayout.addWidget(self.graphicsView_targetedUnit, 9, 1, 1, 1,QtCore.Qt.AlignCenter) 
        
    def setupCurrentUnitView(self):   
        self.graphicsView_currentUnit = QtGui.QGraphicsView(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_currentUnit.sizePolicy().hasHeightForWidth())
        self.graphicsView_currentUnit.setSizePolicy(sizePolicy)
        self.graphicsView_currentUnit.setMinimumSize(QtCore.QSize(50, 50))
        self.graphicsView_currentUnit.setMaximumSize(QtCore.QSize(50, 50))
        self.graphicsView_currentUnit.setObjectName("graphicsView_currentUnit")
        self.gridLayout.addWidget(self.graphicsView_currentUnit, 10, 1, 1, 1,QtCore.Qt.AlignCenter)
       

    def setupFlagView(self):
        self.graphicsView_flag = QtGui.QGraphicsView(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView_flag.sizePolicy().hasHeightForWidth())
        self.graphicsView_flag.setSizePolicy(sizePolicy)
        self.graphicsView_flag.setMinimumSize(QtCore.QSize(90, 120))
        self.graphicsView_flag.setMaximumSize(QtCore.QSize(90, 120))
        self.graphicsView_flag.setObjectName("graphicsView_flag")
        self.gridLayout.addWidget(self.graphicsView_flag, 3, 1, 1, 1)
        
        
    def setupMainView(self):
        self.graphicsView = QtGui.QGraphicsView(self.centralWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 12, 1)
    
    def setupUi(self, BattleWindow):
        BattleWindow.setObjectName("BattleWindow")
        BattleWindow.resize(800, 600)
        BattleWindow.setMinimumSize(QtCore.QSize(800, 600))
        BattleWindow.setAutoFillBackground(True)
        self.centralWidget = QtGui.QWidget(BattleWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
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
        #Label
        self.setupZoneText()
		#Targeted Unit view
        self.setupTargetedUnitView()
		#Current Unit View
        self.setupCurrentUnitView()
        self.setupCurrentUnitView()
		#Flag view
        self.setupFlagView()
        #Main view
        self.setupMainView()
        
        BattleWindow.setCentralWidget(self.centralWidget)
        self.retranslateUi(BattleWindow)
        QtCore.QMetaObject.connectSlotsByName(BattleWindow)

    def retranslateUi(self, BattleWindow):
        BattleWindow.setWindowTitle(QtGui.QApplication.translate("BattleWindow", "BattleWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.status.setText(QtGui.QApplication.translate("BattleWindow", "status ....", None, QtGui.QApplication.UnicodeUTF8))
		
		
class ControlMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(ControlMainWindow, self).__init__(parent)
        self.ui = Ui_BattleWindow()
        self.ui.setupUi(self)
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mySW = ControlMainWindow()
    mySW.showMaximized()
    sys.exit(app.exec_())
