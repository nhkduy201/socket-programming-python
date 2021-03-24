from ults import attach_send, print_r  # my modules
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
    first_rec = s.recv(BUFFER_SIZE).decode()
    seperated_pos = first_rec.find(' ')
    rec_len = int(first_rec[:seperated_pos])
    rec_msg = first_rec[(seperated_pos + 1):]
    while len(rec_msg) < rec_len:
        rec_msg += s.recv(BUFFER_SIZE).decode()
    print_r(rec_msg)
