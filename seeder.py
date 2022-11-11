from datetime import date
import sqlite3
from app import db, create_app

db.create_all(app=create_app())

con = sqlite3.connect("app/db.sqlite")
cur = con.cursor()

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque pharetra placerat nisl. Mauris vitae pretium est. Donec pharetra diam quam, quis lobortis nisi viverra nec. Ut sollicitudin nulla vitae nisl accumsan volutpat vel eget risus. In sed pharetra justo, sed malesuada quam. Curabitur blandit dictum leo, quis feugiat ipsum laoreet a. Nam molestie tristique viverra. Phasellus odio lacus, ultrices sed viverra eget, rutrum at orci. Aliquam non orci at ante posuere efficitur eget in diam. Aenean quis nulla vel turpis molestie fermentum nec sed ligula. Sed consectetur, sapien et aliquet porttitor, risus risus varius erat, eget elementum nibh velit ac odio. Etiam vel turpis elit. "
posts = [
  (
    "Test Post 1",
    lorem,
    "Thread 1",
    "author1",
    "lifestyle,politics,art",
    date.today()
  ),
  (
    "Test Post 2",
    lorem,
    "Thread 1",
    "author1",
    "gaming,politics",
    date.today()
  ),
  (
    "Test Post 3",
    lorem ,
    "Thread 1",
    "author2",
    "lifestyle,gaming,art",
    date.today()
  ),
  (
    "Test Post 4",
    lorem,
    "Thread 2",
    "author2",
    "gaming",
    date.today()
  ),
  (
    "Test Post 5",
    lorem,
    "Thread 2",
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    "Test Post 6",
    lorem,
    "Thread 3",
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    "Test Post 7",
    lorem,
    "Thread 4",
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    "Test Post 8",
    lorem,
    "Thread 5",
    "author3",
    "lifestyle,art",
    date.today()
  ),
  (
    "Test Post 9",
    lorem,
    "Thread 6",
    "author3",
    "lifestyle,art",
    date.today()
  )
]

comments = [
  (
    1,
    "test comment1",
    "author1",
    date.today()
  ),
  (
    1,
    "test comment2",
    "author3",
    date.today()
  )
]

users = [
  (
    "author1@gmail.com",
    "author1"
  ),
  (
    "author2@gmail.com",
    "author2"
  ),
  (
    "author3@gmail.com",
    "author3"
  ),
]

threads = [
  (
    "thread1",
  ),
  (
    "thread2",
  ),
  (
    "thread3",
  ),
  (
    "thread4",
  ),
  (
    "thread5",
  ),
  (
    "thread6",
  ),
]

roles = [
  (
    "admin",
  ),
  (
    "user",
  ),
  (
    "thread5",
  ),
  (
    "thread6",
  )
]

user_roles = [
  (
    1,
    1
  ),
  (
    2,
    2
  ),
  (
    3,
    2
  ),
  (
    2,
    3
  ),
  (
    3,
    4
  )
]

cur.executemany("INSERT INTO forum_post (title, content, thread, author, tags, date ) VALUES(?, ?, ?, ?, ?, ?)", posts)
cur.executemany("INSERT INTO forum_comment (post_id, content, author, date ) VALUES(?, ?, ?, ?)", comments)
cur.executemany("INSERT INTO user (email, name) VALUES(?, ?)", users)
cur.executemany("INSERT INTO roles (name) VALUES(?)", roles)
cur.executemany("INSERT INTO thread (name) VALUES(?)", threads)
cur.executemany("INSERT INTO user_roles (user_id, role_id) VALUES(?, ?)", user_roles)
con.commit()
con.close()