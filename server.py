import socket
from threading import Thread
from ults import rev_str, recv_stream, attach_send
import dotenv
import os
dotenv.load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))


def client_thread(conn, ip, port):
    while True:
        req = recv_stream(conn, BUFFER_SIZE)
        if not len(req):
            conn.close()
            print(f'Disconnected from {ip}{port}')
            break
        res = rev_str(req)
        conn.sendall(attach_send(res))


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((HOST, PORT))
soc.listen(10)
print('Socket now listening')


while True:
    try:
        conn, addr = soc.accept()
    except KeyboardInterrupt:
        break
    ip, port = str(addr[0]), str(addr[1])
    print('Accepting connection from ' + ip + ':' + port)
    Thread(target=client_thread, args=[conn, ip, port]).start()
