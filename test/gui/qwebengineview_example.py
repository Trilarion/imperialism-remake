from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore

# create app
app = QtWidgets.QApplication([])

# QWebEngineView
widget = QtWebEngineWidgets.QWebEngineView()
widget.load(QtCore.QUrl("http://qt-project.org/"))
widget.show()

# run
app.exec_()