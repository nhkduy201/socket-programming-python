import sqlite3
import bcrypt
import dotenv
import os
dotenv.load_dotenv()
KEY = os.getenv('KEY')


def getCur():
    con = sqlite3.connect('main.db')
    con.isolation_level = None
    return con.cursor()


def db_init(cur):
    cur.execute(
        'create table user(username text not null primary key, password text)')


def signin(cur, datas):
    username, password = datas
    user = get_user(cur, username)
    if user is not None and bcrypt.checkpw(password.encode(), user[1]):
        return 'Signed in', user[2], True
    return 'Wrong signin info', False, False


def signup(cur, datas):
    if len(datas) == 2:
        username, password = datas
        key = None
    else:
        username, password, key = datas
    try:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        hashed_key = bcrypt.hashpw(KEY.encode(), bcrypt.gensalt())
        if key is not None:
            if bcrypt.checkpw(key.encode(), hashed_key):
                values = (username, hashed_password, True)
            else:
                return 'Wrong signin info'
        else:
            values = (username, hashed_password, False)
        cur.execute('insert into user values (?, ?, ?)',
                    values)
        return "Signed up"
    except sqlite3.IntegrityError as err:
        return 'Account existed'


def get_user(cur, username):
    cur.execute(f'select * from user where username = "{username}"')
    return cur.fetchone()


# db_init()
# getCur().execute('delete from user')
# getCur().execute('alter table user add is_admin boolean')
# signup('MiDu', 'Liu liu eeeee')
# rs = cur.fetchone()
# print(rs)
# print(datas)
