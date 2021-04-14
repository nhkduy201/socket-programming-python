import os
import db
import pickle
import socket
import dotenv
import argparse
import threading


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


def get_info_server():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int,
                        help='port connect to host', default=11201)
    parser.add_argument('-b', '--buffer', type=int,
                        help='size of buffer recieve and send', default=8)
    args = parser.parse_args()
    return get_host_ip(), args.port, args.buffer


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
    first_rec = socket.recv(buff)
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
    if str(type(res)) == "<class 'list'>":
        for r in res:
            print(format_line(r))
    else:
        print(format_line(res))


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
    print(f' client {ip}:{port} disconnected')


def handle_client_req(con, req, check_datas, cur):
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
                    res = db.signup(cur, para)
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


def client_thread(con, ip, port, buffer):
    is_signin = False
    is_admin = False
    is_exit = False
    cur = get_db_cur()
    while True:
        req = receive(con, buffer)
        if is_exit or not len(req):
            exit_client(con, ip, port)
            break
        is_signin, is_admin, is_exit = handle_client_req(
            con, req, (is_signin, is_admin, is_exit), cur)


def server_main_process(sock, buffer):
    while True:
        try:
            con, addr = sock.accept()
        except KeyboardInterrupt:
            print('\nexited')
            break
        ip, port = addr[0], str(addr[1])
        print(f'client {ip}:{port} connected')
        threading.Thread(target=client_thread, args=[
                         con, ip, port, buffer], daemon=True).start()


def client_main_process(sock, buffer):
    while True:
        try:
            req_mes = input("Proceed what: ")
            if len(req_mes):
                sock.sendall(attach_send(req_mes))
                res = receive(sock, buffer)
                if res == '!exit':
                    print_res('exited')
                    sock.close()
                    break
                print_res(res)
        except KeyboardInterrupt:
            print_res('\nexited')
            sock.close()
            break
