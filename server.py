import socket
from threading import Thread
from ults import *
import dotenv
import os
dotenv.load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))


def client_thread(con, ip, port):
    is_signin = False
    is_admin = False
    is_exit = False
    cur = get_db_cur()
    while True:
        req = receive(con, BUFFER_SIZE)
        if is_exit or not len(req):
            exit_client(con, ip, port)
            break
        is_signin, is_admin, is_exit = process_send(
            con, req, (is_signin, is_admin, is_exit), cur)


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((HOST, PORT))
soc.listen(10)
print('Socket now listening')


while True:
    try:
        con, addr = soc.accept()
    except KeyboardInterrupt:
        break
    ip, port = addr[0], str(addr[1])
    print(f'{ip}:{port} connected')
    Thread(target=client_thread, args=[con, ip, port]).start()
