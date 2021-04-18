import sqlite3


def getCur():
    con = sqlite3.connect('main.db')
    con.isolation_level = None
    return con.cursor()


def init_db(cur):
    cur.execute(
        'create table user(username text not null primary key, password text, is_admin boolean)')
    cur.execute('create table match(id integer not null primary key autoincrement, first_team text not null, score text not null, second_team text not null)')
    cur.execute('create table event(event_id integer not null, time text not null, detail text not null, is_first_team boolean, match_id integer, primary key(event_id, match_id))')


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
    cur.execute(
        f"select ev.time, ev.is_first_team, ev.detail from event ev where ev.match_id = {match_id}")
    event_list = cur.fetchall()
    cur.execute(f"select m.score from match m where m.id = {match_id}")
    fulltime_event = ('FT', cur.fetchone()[0], 'null')
    event_list.append(fulltime_event)
    return event_list


# cur = getCur()
# drop_db(cur)
# init_db(cur)

# signup(cur, ('user1', 'pass2'))
# signup(cur, ('user2', 'pass1'))

# insert_match(cur, ('mu', '1-1', 'mc'),
#              [('10', '{"yc":"so1"}', False), ('40', '{"scrd":"so10","scr":"1-0"}', True), ('HT', '{"scr":"1-0"}', 'null'), ('89', '{"scrd":"so4";"scr":"1-1"}', False)])
# insert_match(cur, ('as', '2-1', 'cs'),
#              [('10', '{"scrd":"so10","scr":"1-0"}', True), ('40', '{"scrd":"so20","scr":"2-0"}', True), ('HT', '{"scr":"1-0"}', 'null'), ('89', '{"scrd":"so4";"scr":"2-1"}', False)])

# cur.execute('select * from match')
# print(cur.fetchall())
# cur.execute('select * from event')
# print(cur.fetchall())
