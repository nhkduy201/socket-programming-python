import socket
from ults import get_info_client, client_main_process

host, port, buffer = get_info_client()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
client_main_process(sock, buffer)
