import socket
from threading import Thread
from ults import get_info_server, server_main_process

host, port, buffer = get_info_server()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
print(f'server {host}:{port} listening')
server_main_process(sock, buffer)
