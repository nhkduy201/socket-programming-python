from ults import attach_send, print_r, recv_stream  # my modules
import socket
# for env var
import os
import dotenv
dotenv.load_dotenv()

HOST = os.getenv('HOST')
PORT = int(os.getenv('PORT'))
BUFFER_SIZE = int(os.getenv('BUFFER_SIZE'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    send_msg = input('send: ')
    print(send_msg)
    s.send(attach_send(send_msg))
    rec_msg = recv_stream(s, BUFFER_SIZE)
    print_r(rec_msg)
