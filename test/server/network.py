from PyQt5 import QtCore, QtNetwork

from base import constants as c
from server.server import ServerManager
from lib.network import Server
from base.network import Client

server = ServerManager()
server.server.start(c.NETWORK_PORT)
client = Client()
client.set_socket()

def setup():
    client.connect_to_host(c.NETWORK_PORT)
    # print('wait {}'.format(server.server.waitForNewConnection(1000)))

def send():
    message = {
        'channel': c.CH_SCENARIO_PREVIEW,
        'content': None
    }
    client.send(message)

    message = {
        'channel' : c.CH_CORE_SCENARIO_TITLES,
        'content' : 'Hi guys'
    }
    client.send(message)


app = QtCore.QCoreApplication([])

QtCore.QTimer.singleShot(100, setup)
QtCore.QTimer.singleShot(1000, send)
QtCore.QTimer.singleShot(3000, app.quit)
app.exec_()
