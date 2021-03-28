import os


def rev_str(str):
    return ''.join(reversed(str))


def recv_stream(socket, buff):
    first_rec = socket.recv(buff).decode()
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
