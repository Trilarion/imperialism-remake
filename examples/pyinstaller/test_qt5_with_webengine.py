from PyQt5.QtCore import QT_VERSION_STR, PYQT_VERSION_STR
from sip import SIP_VERSION_STR
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtWebEngineWidgets as QtWebEngineWidgets

if __name__ == '__main__':

    print("QT   version: {}".format(QT_VERSION_STR))
    print("PyQt version: {}".format(PYQT_VERSION_STR))
    print("SIP  version: {}".format(SIP_VERSION_STR))

    # create app
    app = QtWidgets.QApplication([])

    # QWebEngineView
    web_view_widget = QtWebEngineWidgets.QWebEngineView()
    web_view_widget.titleChanged.connect(
        web_view_widget.setWindowTitle)  # displays the actual page title as windows title
    web_view_widget.load(QtCore.QUrl("http://qt-project.org/"))
    web_view_widget.show()

    # run
    app.exec_()