from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from sip import SIP_VERSION_STR
import PyQt5.QtWidgets as QtWidgets

if __name__ == '__main__':

    print("QT   version: {}".format(QT_VERSION_STR))
    print("PyQt version: {}".format(PYQT_VERSION_STR))
    print("SIP  version: {}".format(SIP_VERSION_STR))

    # create app
    app = QtWidgets.QApplication([])

    # simple QWidget
    widget = QtWidgets.QWidget()
    widget.setWindowTitle('Test')
    widget.show()

    # run
    app.exec_()