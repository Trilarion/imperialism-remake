from PyQt5.QtCore import QObject, QPointF
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QGraphicsScene, QPushButton


class MainBattleWindows(QMainWindow):
    def __init__(self, config, parent=None):
        super(MainBattleWindows, self).__init__(parent)
        self.config = config

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
        # noinspection PyTypeChecker,PyCallByClass
        result = QMessageBox.question(self,
                                      self.config.get_text('exit.window.title'),
                                      self.config.get_text('exit.window.content'),
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


class BattleView(QObject):
    def __init__(self, battle_window, config, parent=None):
        super().__init__(parent)
        self.mainScene = MainQGraphicsScene()


class CustomButton(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.enter_functions = []
        self.leave_functions = []
        self.click_functions = []
        # noinspection PyUnresolvedReferences
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

    def clear_action_click(self):
        self.click_functions = []
