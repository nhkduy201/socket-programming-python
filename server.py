# my modules
from ults import attach_send, print_r, recv_stream
import dotenv
import os
import socket

# socket
# for env var
dotenv.load_dotenv()


HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while True:
    print('waiting for message...')
    conn, addr = s.accept()
    while True:
        rec_msg = recv_stream(conn, BUFFER_SIZE)
        print_r(rec_msg)
        send_msg = input('send: ')
        print(send_msg)
        conn.send(attach_send(send_msg))
