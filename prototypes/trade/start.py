from PySide import QtGui, QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Trade Prototype')

app = QtGui.QApplication([])

window = MainWindow()
window.show()

app.exec_()