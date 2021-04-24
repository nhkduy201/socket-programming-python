import os
import db
import pickle
import socket
import argparse
import threading
from getch import *

def clear_screen():
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')


def get_info_client():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', type=str,
                        help='ip of host', default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int,
                        help='port connect to host', default=11201)
    parser.add_argument('-b', '--buffer', type=int,
                        help='size of buffer recieve and send', default=8)
    args = parser.parse_args()
    return args.ip, args.port, args.buffer


def get_info_server(def_adm_key):
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        help='port connect to host', default=11201)
    parser.add_argument('-b', '--buffer', type=int,
                        help='size of buffer recieve and send', default=8)
    parser.add_argument('-k', '--key', type=str,
                        help='key for admin', default=def_adm_key)
    args = parser.parse_args()
    return get_host_ip(), args.port, args.buffer, args.key


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        host = s.getsockname()[0]
    except Exception:
        host = '127.0.0.1'
    finally:
        s.close()
    return host


def get_db_cur():
    return db.getCur()


def receive(socket, buff):
    try:
        first_rec = socket.recv(buff)
    except Exception:
        return '!continue'
    if len(first_rec) == 0:
        return ''
    split_first = first_rec.split(b' ', 1)
    rec_len = int(split_first[0])
    rec_msg = split_first[1]
    while len(rec_msg) < rec_len:
        rec_msg += socket.recv(buff)
    return pickle.loads(rec_msg)


def attach_send(send_data):
    dump_data = pickle.dumps(send_data)
    return bytes(f'{len(dump_data)} ', 'utf-8') + dump_data


def format_line(line):
    formated_line = ''
    gap_size = 5
    if str(type(line)) == "<class 'tuple'>":
        for i in range(len(line) - 1):
            formated_line += str(line[i]) + ' ' * gap_size
        formated_line += str(line[len(line) - 1])
    else:
        formated_line = line
    return formated_line


def print_res(res):
    COLOR = '\033[96m'
    ENDC = '\033[0m'

    clear_screen()
    if str(type(res)) == "<class 'list'>":
        for r in res:
            print(f'{COLOR}{format_line(r)}{ENDC}')
    else:
        print(f'{COLOR}{format_line(res)}{ENDC}')


def is_valid_cmd(cmd, para):
    command_map = {
        '!su': (2, 3),
        '!si': (2,),
        '!ls': (0,),
        '!scr': (1,),
        '!help': (0,),
        '!exit': (0,)
    }
    if len(para) in command_map.get(cmd, ()):
        return True
    return False


def exit_client(con, ip, port):
    con.close()
    print(f'client {ip}:{port} disconnected')


def handle_client_req(con, req, check_datas, cur, admin_key):
    is_signin, is_admin, is_exit = check_datas
    res = ''
    cmd = req.split()[0]
    para = tuple(req.split()[1:])
    if not is_valid_cmd(cmd, para):
        res = 'Invalid command'
    else:
        if cmd == '!exit':
            is_exit = True
            res = '!exit'
        else:
            if not is_signin:
                if cmd == '!su':
                    res = db.signup(cur, para, admin_key)
                elif cmd == '!si':
                    res, is_admin, is_signin = db.signin(cur, para)
                else:
                    res = 'Sign in first'
            else:
                if cmd == '!su' or cmd == '!si':
                    res = 'You\'ve already signed in'
                elif cmd != '!help':
                    if cmd == '!ls':
                        res = db.get_all_match(cur)
                    else:
                        match_id = para[0]
                        res = db.get_all_event(cur, match_id)
            if cmd == '!help':
                res = ['!su [username] [password] [key] : sign up (with key if you are admin)', '!si [username] [password] : sign in',
                       '!ls : show the list of all matches', '!scr [id] : show the score of the given id', '!help : show this help']
    con.sendall(attach_send(res))
    return is_signin, is_admin, is_exit

def client_thread(con, ip, port, buffer, admin_key, exit_event):
    TIMEOUT = 0.5
    con.settimeout(TIMEOUT)
    # cnt_check_server = 0
    is_signin = False
    is_admin = False
    is_exit = False
    cur = get_db_cur()
    while True: #not exit_event.isSet():
        is_exit = exit_event.wait(TIMEOUT)
        if is_exit:
            con.sendall(attach_send('!server_exit'))
        # else:
        #     cnt_check_server += 1
        #     print(f'{ip}:{port} checking server, server run normally, time {cnt_check_server}')
        req = receive(con, buffer)
        if is_exit or not len(req):
            exit_client(con, ip, port)
            break
        if req == '!continue':
            continue
        is_signin, is_admin, is_exit = handle_client_req(con, req, (is_signin, is_admin, is_exit), cur, admin_key)

def server_main_process(host, port, sock, buffer, admin_key, exit_event):
    clear_screen()
    print(f'server {host}:{port} listening')
    while True:
        try:
            con, addr = sock.accept()
        except KeyboardInterrupt:
            exit_event.set()
            print('\nserver exit')
            break
        ip, port = addr[0], str(addr[1])
        print(f'client {ip}:{port} connected')
        threading.Thread(target=client_thread, args=[
                         con, ip, port, buffer, admin_key, exit_event]).start()

def client_send_process(sock):
    inp = ''
    while True:
        c = read_key()
        if c == '\n':
            if len(inp) > 0:
                sock.sendall(attach_send(inp))
                inp = ''
            continue
        if ord(c) == 127:
            inp = inp[:-1]
        else:
            inp += c

def client_main_process(sock, buffer):
    clear_screen()
    print_res('Try sending "!help"')
    # send
    threading.Thread(target=client_send_process, args=(sock,), daemon=True).start()
    # receive
    while True:
        try:
            res = receive(sock, buffer)
            if res == '!exit' or res == '!server_exit':
                if res == '!exit':
                    print_res('client exit')
                if res == '!server_exit':
                    print_res('server exit')
                sock.close()
                break
            print_res(res)
        except KeyboardInterrupt:
            print_res('client exit')
            sock.close()
            break
