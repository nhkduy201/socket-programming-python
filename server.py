import socket
from threading import Thread
from ults import receive, get_host, get_db_cur, exit_client, process_send
import dotenv
import os


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


dotenv.load_dotenv()
HOST = get_host()
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((HOST, PORT))
soc.listen(10)
print('socket now listening')


while True:
    try:
        con, addr = soc.accept()
    except KeyboardInterrupt:
        print('\nexited')
        break
    ip, port = addr[0], str(addr[1])
    print(f'{ip}:{port} connected')
    Thread(target=client_thread, args=[con, ip, port], daemon=True).start()
