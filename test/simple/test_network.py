from PyQt5 import QtNetwork, QtCore

def new_server_connection():
    print('new server connection')

def new_client_connection():
    print('new client connection')

def setup():
    server.listen(QtNetwork.QHostAddress.LocalHost, 34543)
    client_socket.connectToHost(QtNetwork.QHostAddress.LocalHost, 34543)


app = QtCore.QCoreApplication([])

server = QtNetwork.QTcpServer()
server.newConnection.connect(new_server_connection)
client_socket = QtNetwork.QTcpSocket()
client_socket.connected.connect(new_client_connection)

QtCore.QTimer.singleShot(0, setup)
QtCore.QTimer.singleShot(3000, app.quit)
app.exec_()