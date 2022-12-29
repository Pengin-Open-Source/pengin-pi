import sqlite3
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from app import create_app
from app.db import db
from app.util.uuid import id

create_app()

con = sqlite3.connect("instance/db.sqlite")
cur = con.cursor()

password = generate_password_hash('asd', method='sha256')

user_id_1 = id()
user_id_2 = id()
user_id_3 = id()

"""
3 users => user 1's roles (admin, user) AND user 2's roles = (user, thread5) AND user 3's roles = (user, thread6)
4 roles (admin, user, thread5, thread6)
4 events (admin,user,user,admin) from user 1
"""

users = [
    (
        user_id_1,
        "u1@gmail.com",
        "author1",
        password
    ),
    (
        user_id_2,
        "u2@gmail.com",
        "author2",
        password
    ),
    (
        user_id_3,
        "u3@gmail.com",
        "author3",
        password
    ),
]

role_id_1 = id()
role_id_2 = id()
role_id_3 = id()
role_id_4 = id()

roles = [
    (
        role_id_1,
        "admin",
    ),
    (
        role_id_2,
        "user",
    ),
    (
        role_id_3,
        "thread5",
    ),
    (
        role_id_4,
        "thread6",
    )
]

# author1 is admin, 2 and 3 are users with access
# to threads 5 and 6 respectively
user_roles = [
    (
        id(),
        user_id_1,
        role_id_1
    ),
    (
        id(),
        user_id_1,
        role_id_2
    ),
    (
        id(),
        user_id_2,
        role_id_2
    ),
    (
        id(),
        user_id_3,
        role_id_2
    ),
    (
        id(),
        user_id_2,
        role_id_3
    ),
    (
        id(),
        user_id_3,
        role_id_4
    )
]

d1 = '2022/09/19 13:55'
d2 = '2022/09/19 15:55'
d3 = '2022/09/20 15:55'
d4 = '2022/09/20 19:55'
d5 = '2022/09/21 20:55'
d6 = '2022/09/21 23:55'

events = [
    (
        id(),
        user_id_1,
        user_id_1,
        role_id_1,
        datetime.strptime(d1, '%Y/%m/%d %H:%M'),
        datetime.strptime(d2, '%Y/%m/%d %H:%M'),
        "Test Event 1",
        "Test description 1",
        "Faketown"
    ),
    (
        id(),
        user_id_1,
        user_id_1,
        role_id_2,
        datetime.strptime(d3, '%Y/%m/%d %H:%M'),
        datetime.strptime(d4, '%Y/%m/%d %H:%M'),
        "Test Event 2",
        "Test description 2",
        "Faketown"
    ),
    (
        id(),
        user_id_1,
        user_id_1,
        role_id_2,
        datetime.strptime(d5, '%Y/%m/%d %H:%M'),
        datetime.strptime(d6, '%Y/%m/%d %H:%M'),
        "Test Event 3",
        "Test description 3",
        "Faketown"
    ),
    (
        id(),
        user_id_1,
        user_id_1,
        role_id_1,
        datetime.strptime(d1, '%Y/%m/%d %H:%M'),
        datetime.strptime(d6, '%Y/%m/%d %H:%M'),
        "Test Event 4",
        "Test description 4",
        "Faketown"
    )
]

cur.executemany("""INSERT INTO user (id, email, name, password)
                VALUES(?, ?, ?, ?)""", users)
cur.executemany("INSERT INTO roles (id, name) VALUES(?, ?)", roles)
cur.executemany("""INSERT INTO user_roles ( id, user_id, role_id)
                VALUES(?, ?,?)""", user_roles)
cur.executemany("""INSERT INTO events (id, user_id, organizer, role,
                start_datetime, end_datetime, title, description, location)
                VALUES(?,?,?,?,?,?,?,?,?)""", events)

con.commit()
con.close()
print("done seeding")
