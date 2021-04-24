import sqlite3


def getCur():
    con = sqlite3.connect('main.db')
    con.isolation_level = None
    return con.cursor()


def init_db(cur):
    cur.execute(
        'create table user(username text not null primary key, password text, is_admin boolean)')
    cur.execute('create table match(id integer not null primary key autoincrement, first_team text not null, score text not null, second_team text not null)')
    cur.execute('create table event(event_id integer not null, time text not null, detail text not null, is_first_team boolean, match_id integer not null, primary key(event_id, match_id))')


def drop_db(cur):
    cur.execute('drop table user')
    cur.execute('drop table match')
    cur.execute('drop table event')

def signin(cur, datas):
    username, password = datas
    user = get_user(cur, username)
    if user is not None and password == user[1]:
        return 'Signed in', user[2], True
    return 'Wrong signin info', False, False


def signup(cur, datas, admin_key):
    if len(datas) == 2:
        username, password = datas
        key = None
    else:
        username, password, key = datas
    try:
        if key is not None:
            if key == admin_key:
                values = (username, password, True)
            else:
                return 'Wrong signin info'
        else:
            values = (username, password, False)
        cur.execute('insert into user values (?, ?, ?)',
                    values)
        return "Signed up"
    except sqlite3.IntegrityError as err:
        return 'Account existed'


def get_user(cur, username):
    cur.execute(f'select * from user where username = "{username}"')
    return cur.fetchone()


def insert_match(cur, match_datas, event_datas):
    cur.execute('insert into match(first_team, score, second_team) values (?, ?, ?)',
                match_datas)
    last_match_id = cur.lastrowid
    for i in range(len(event_datas)):
        cur.execute('insert into event values (?, ?, ?, ?, ?)',
                    (i + 1,) + event_datas[i] + (last_match_id,))


def get_all_match(cur):
    cur.execute("select * from match")
    return cur.fetchall()


def get_all_event(cur, match_id):
    try:
        int_match_id = int(match_id)
    except ValueError:
        return 'Invalid command'
    cur.execute(f"select m.first_team, m.score, m.second_team from match m where m.id = {int_match_id}")
    match = cur.fetchone()
    event_list = [match]
    cur.execute(
        f"select ev.time, ev.is_first_team, ev.detail from event ev where ev.match_id = {int_match_id}")
    event_list = event_list + cur.fetchall()
    if len(event_list) == 0:
        return 'Match not found'
    fulltime_event = ('FT', None, match[1])
    event_list.append(fulltime_event)
    return event_list


# cur = getCur()
# drop_db(cur)
# init_db(cur)
# signup(cur, ('normal_client', 'clientpass'), 'wrongkey')
# signup(cur, ('admin_client', 'adminpass'), 'private')

# insert_match(cur, ('Arsenal', '0-1', 'Everton'), [('38', 'yc:Thomas', True), ('HT', '0-0', None), ('55', 'yc:Allan', False), ('62', 'yc:Mason Holgate', False), ('68', 'yc:Fabian Delph', False), ('76', '0-1:Bernd Leno', False)])
# insert_match(cur, ('AFC Bournemouth', '0-1', 'Brentford'), [('25', 'yc:Pontus Jansson', True), ('HT', '0-0', None), ('50', 'rc:Pontus Jansson', True), ('68', 'rc:Jefferson-yc:Mason Holgate', None), ('78', '0-1:Bryan Mbeumo', False), ('80', 'rc:Ivan Toney', True)])
