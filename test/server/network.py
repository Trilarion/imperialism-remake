from PySide import QtCore, QtNetwork
import constants as c
from server.network import server
from client.network import client

def setup():
    server.start(c.NETWORK_PORT)
    client.login(QtNetwork.QHostAddress.LocalHost, c.NETWORK_PORT)

def send():
    message = {
        'type': 'chat.register',
    }
    client.send(message)

    message = {
        'type' : 'chat.message',
        'text' : 'Hi guys'
    }
    client.send(message)


app = QtCore.QCoreApplication([])

QtCore.QTimer.singleShot(0, setup)
QtCore.QTimer.singleShot(100, send)
QtCore.QTimer.singleShot(3000, app.quit)
app.exec_()
