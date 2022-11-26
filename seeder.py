from datetime import date
import sqlite3
from app import create_app
from app.util.uuid import id
from app.db import db
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
  db.create_all()


con = sqlite3.connect("app/db.sqlite")
cur = con.cursor()

password = generate_password_hash('password', method='sha256')
lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque pharetra placerat nisl. Mauris vitae pretium est. Donec pharetra diam quam, quis lobortis nisi viverra nec. Ut sollicitudin nulla vitae nisl accumsan volutpat vel eget risus. In sed pharetra justo, sed malesuada quam. Curabitur blandit dictum leo, quis feugiat ipsum laoreet a. Nam molestie tristique viverra. Phasellus odio lacus, ultrices sed viverra eget, rutrum at orci. Aliquam non orci at ante posuere efficitur eget in diam. Aenean quis nulla vel turpis molestie fermentum nec sed ligula. Sed consectetur, sapien et aliquet porttitor, risus risus varius erat, eget elementum nibh velit ac odio. Etiam vel turpis elit. "

thread_id_1=id()
thread_id_2=id()
thread_id_3=id()
thread_id_4=id()
thread_id_5=id()
thread_id_6=id()
threads = [
  (
    thread_id_1,
    "thread1",
  ),
  (
    thread_id_2,
    "thread2",
  ),
  (
    thread_id_3,
    "thread3",
  ),
  (
    thread_id_4,
    "thread4",
  ),
  (
    thread_id_5,
    "thread5",
  ),
  (
    thread_id_6,
    "thread6",
  ),
]

post_id_1 = id()
posts = [
  (
    post_id_1,
    "Test Post 1",
    lorem,
    thread_id_1,
    "author1",
    "lifestyle,politics,art",
    date.today()
  ),
  (
    id(),
    "Test Post 2",
    lorem,
    thread_id_1,
    "author1",
    "gaming,politics",
    date.today()
  ),
  (
    id(),
    "Test Post 3",
    lorem ,
    thread_id_1,
    "author2",
    "lifestyle,gaming,art",
    date.today()
  ),
  (
    id(),
    "Test Post 4",
    lorem,
    thread_id_2,
    "author2",
    "gaming",
    date.today()
  ),
  (
    id(),
    "Test Post 5",
    lorem,
    thread_id_2,
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 6",
    lorem,
    thread_id_3,
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 7",
    lorem,
    thread_id_4,
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 8",
    lorem,
    thread_id_5,
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 9",
    lorem,
    thread_id_6,
    "author3",
    "lifestyle,art",
    date.today()
  )
]

comments = [
  (
    id(),
    post_id_1,
    "test comment1",
    "author1",
    date.today()
  ),
  (
    id(),
    post_id_1,
    "test comment2",
    "author3",
    date.today()
  )
]

user_id_1 = id()
user_id_2 = id()
user_id_3 = id()
users = [
  (
    user_id_1,
    "author1@gmail.com",
    "author1",
    password
  ),
  (
    user_id_2,
    "author2@gmail.com",
    "author2",
    password
  ),
  (
    user_id_3,
    "author3@gmail.com",
    "author3",
    password
  ),
]

role_id_1= id()
role_id_2= id()
role_id_3= id()
role_id_4= id()
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

#author1 is admin, 2 and 3 are users with access to threads 5 and 6 respectively
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

#threads 1-4 are public 5 and 6 are in their own groups, admin has access to all
thread_roles = [ 
  (
    id(),
    role_id_1,
    thread_id_1
  ),
  (
    id(),
    role_id_1,
    thread_id_2
  ),
  (
    id(),
    role_id_1,
    thread_id_3
  ),
  (
    id(),
    role_id_1,
    thread_id_4
  ),
  (
    id(),
    role_id_1,
    thread_id_5
  ),
  (
    id(),
    role_id_1,
    thread_id_6
  ),
  (
    id(),
    role_id_2,
    thread_id_1
  ),
  (
    id(),
    role_id_2,
    thread_id_2
  ),
  (
    id(),
    role_id_2,
    thread_id_3
  ),
  (
    id(),
    role_id_2,
    thread_id_4
  ),
  (
    id(),
    role_id_3,
    thread_id_5
  ),
  (
    id(),
    role_id_4,
    thread_id_6
  ),
]

cur.executemany("INSERT INTO forum_post (id, title, content, thread_id, author, tags, date ) VALUES(?, ?, ?, ?, ?, ?, ?)", posts)
cur.executemany("INSERT INTO forum_comment (id, post_id, content, author, date ) VALUES(?, ?, ?, ?, ?)", comments)
cur.executemany("INSERT INTO user (id, email, name, password) VALUES(?, ?, ?, ?)", users)
cur.executemany("INSERT INTO roles (id, name) VALUES(?, ?)", roles)
cur.executemany("INSERT INTO thread (id, name) VALUES(?, ?)", threads)
cur.executemany("INSERT INTO user_roles ( id, user_id, role_id) VALUES(?, ?,?)", user_roles)
cur.executemany("INSERT INTO thread_roles (id, role_id, thread_id) VALUES(?, ?,?)", thread_roles)
con.commit()
con.close()