import os
import db


def get_db_cur():
    return db.getCur()


def receive(socket, buff):
    first_rec = socket.recv(buff).decode()
    if len(first_rec) == 0:
        return ''
    seperated_pos = first_rec.find(' ')
    rec_len = int(first_rec[:seperated_pos])
    rec_msg = first_rec[(seperated_pos + 1):]
    while len(rec_msg) < rec_len:
        rec_msg += socket.recv(buff).decode()
    return rec_msg


def attach_send(send_data):
    return (str(len(send_data)) + ' ' + send_data).encode()


def clr_scr():
    clear_cmd = ''
    if os.name == 'nt':
        clear_cmd = 'cls'
    else:
        if os.name == 'posix':
            clear_cmd = 'clear'
    # return subprocess.run(clear_cmd, shell=True) == 0
    os.system(clear_cmd)


def print_r(str_val):
    print(f'{str_val:>{os.get_terminal_size().columns}}')


def is_valid_cmd(cmd, para):
    command_map = {
        '!su': (2, 3),
        '!si': (2,),
        '!ls': (0,),
        '!scr': (1,),
        '!help': (0,)
    }
    if len(para) in command_map.get(cmd, ()):
        return True
    return False


def process_send(con, req, is_signin, is_admin, cur):
    res = ''
    cmd = req.split()[0]
    para = tuple(req.split()[1:])
    if is_valid_cmd(cmd, para):
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
                res = f'Data for {cmd} command'
        if cmd == '!help':
            res = '!su [username] [password] [key]    : sign up (with key if you are admin)\n!si [username] [password]          : sign in\n!ls                                : show the list of all matches\n!scr [id]                          : show the score of the given id\n!help                              : show this help'
    else:
        res = 'Invalid command'
    con.sendall(attach_send(res))
    return is_signin, is_admin
