from datetime import date
import sqlite3

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

cur.executemany("INSERT INTO forum_post (title, content, thread, author, tags, date ) VALUES(?, ?, ?, ?, ?, ?)", posts)
cur.executemany("INSERT INTO forum_comment (post_id, content, author, date ) VALUES(?, ?, ?, ?)", comments)
#executemany comments
#executemany users 
con.commit()
con.close()