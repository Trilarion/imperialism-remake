from PySide import QtCore, QtNetwork
import constants as c
import server.network as snet
import client.network as cnet

def setup():
    snet.local_server.start(c.LOCALHOST, c.NETWORK_PORT)
    client.login(c.LOCALHOST, c.NETWORK_PORT)

def send():
    d = {'car':4,89:'dzhuifhe'}
    client.send(d)
    for id in snet.local_server.connections:
        snet.local_server.send(id, d)

app = QtCore.QCoreApplication([])

client = cnet.Client()

QtCore.QTimer.singleShot(0, setup)
QtCore.QTimer.singleShot(100, send)
QtCore.QTimer.singleShot(3000, app.quit)
app.exec_()
