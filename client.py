import socket
import dotenv
import os
from ults import receive, attach_send, print_res
dotenv.load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
while True:
    try:
        req_mes = input("Proceed what: ")
        if len(req_mes):
            sock.send(attach_send(req_mes))
            res = receive(sock, BUFFER_SIZE)
            print_res(res)
            if(res == 'Exited'):
                break
    except KeyboardInterrupt:
        break
