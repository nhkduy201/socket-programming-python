def rev_str(str):
    return ''.join(reversed(str))


def recv_stream(socket, buff):
    first_rec = socket.recv(buff).decode()
    seperated_pos = first_rec.find(' ')
    rec_len = int(first_rec[:seperated_pos])
    rec_data = first_rec[(seperated_pos + 1):]
    while len(rec_data) < rec_len:
        rec_data += socket.recv(buff).decode()
    return rec_data


def attach_send(send_data):
    return (str(len(send_data)) + ' ' + send_data).encode()
