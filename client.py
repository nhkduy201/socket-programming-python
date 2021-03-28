import socket
import dotenv
import os
from ults import recv_stream, attach_send
dotenv.load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
while True:
    clients_input = input("Proceed what: ")
    sock.send(attach_send(clients_input))
    res = recv_stream(sock, BUFFER_SIZE)
    print(res)
