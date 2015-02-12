from PySide import QtCore

from base import constants as c
from server.network import server_manager
from client.client import network_client


def setup():
    server_manager.server.start(c.Network_Port)
    network_client.connect_to_host(c.Network_Port)

def send():
    message = {
        'type': 'chat.register',
        'message': c.MessageType.scenario_preview.value
    }
    network_client.send(message)

    message = {
        'type' : 'chat.message',
        'text' : 'Hi guys'
    }
    network_client.send(message)


app = QtCore.QCoreApplication([])

QtCore.QTimer.singleShot(0, setup)
QtCore.QTimer.singleShot(100, send)
QtCore.QTimer.singleShot(3000, app.quit)
app.exec_()
