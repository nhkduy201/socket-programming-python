from ults import attach_send  # my modules
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

req_data = ''
while req_data != '!break':
    req_data = input('send something: ')
    s.send(attach_send(req_data))
    first_rec = s.recv(BUFFER_SIZE).decode()
    seperated_pos = first_rec.find(' ')
    rec_len = int(first_rec[:seperated_pos])
    rec_data = first_rec[(seperated_pos + 1):]
    while len(rec_data) < rec_len:
        rec_data += s.recv(BUFFER_SIZE).decode()
    print(rec_data)
