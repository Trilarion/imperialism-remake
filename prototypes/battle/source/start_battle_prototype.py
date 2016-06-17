"""

"""

import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as QtWidgets

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Battle Prototype')

app = QtWidgets.QApplication([])

window = MainWindow()
window.show()

app.exec_()