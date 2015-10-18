import base.constants as c
from server.network import ServerProcess
from multiprocessing import Pipe

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    server_process = ServerProcess(c.Network_Port, child_conn)
    server_process.start()

    # stop server
    parent_conn.send('quit')
    server_process.join()

    print('will exit')