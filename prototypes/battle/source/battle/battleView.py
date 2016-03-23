from PyQt5.QtWidgets import QMessageBox, QMainWindow

from prototypes.battle.source.battle.land.landBattleView import LandBattleView


class MainBattleWindows(QMainWindow):
    def __init__(self, config, parent=None):
        super(MainBattleWindows, self).__init__(parent)
        self.ui = LandBattleView(self, config, None)
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
        # noinspection PyTypeChecker,PyCallByClass
        result = QMessageBox.question(self,
                                      self.config.get_text('exit.window.title'),
                                      self.config.get_text('exit.window.content'),
                                      QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.No:
            event.ignore()
