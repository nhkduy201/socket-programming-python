# my modules
from ults import rev_str, attach_send  # recv_stream
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
    conn, addr = s.accept()
    print(f'Connected by {addr}')
    first_rec = conn.recv(BUFFER_SIZE).decode()
    seperated_pos = first_rec.find(' ')
    rec_len = int(first_rec[:seperated_pos])
    rec_data = first_rec[(seperated_pos + 1):]
    while len(rec_data) < rec_len:
        rec_data += conn.recv(BUFFER_SIZE).decode()
    conn.send(attach_send(rev_str(rec_data)))
