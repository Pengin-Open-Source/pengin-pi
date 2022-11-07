from datetime import date
import sqlite3

con = sqlite3.connect("db.sqlite")
cur = con.cursor()

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque pharetra placerat nisl. Mauris vitae pretium est. Donec pharetra diam quam, quis lobortis nisi viverra nec. Ut sollicitudin nulla vitae nisl accumsan volutpat vel eget risus. In sed pharetra justo, sed malesuada quam. Curabitur blandit dictum leo, quis feugiat ipsum laoreet a. Nam molestie tristique viverra. Phasellus odio lacus, ultrices sed viverra eget, rutrum at orci. Aliquam non orci at ante posuere efficitur eget in diam. Aenean quis nulla vel turpis molestie fermentum nec sed ligula. Sed consectetur, sapien et aliquet porttitor, risus risus varius erat, eget elementum nibh velit ac odio. Etiam vel turpis elit. "
posts = [
  {
    'title': "Test Post 1",
    'content': lorem,
    'thread': "Thread 1",
    'author': "author1",
    'tags':"lifestyle,politics,art",
    'date': date.today()
  },
  {
    'title': "Test Post 2",
    'content': lorem,
    'thread': "Thread 1",
    'author': "author1",
    'tags':"gaming,politics",
    'date': date.today()
  },
  {
    'title': "Test Post 3",
    'content': lorem ,
    'thread': "Thread 1",
    'author': "author2",
    'tags':"lifestyle,gaming,art",
    'date': date.today()
  },
  {
    'title': "Test Post 4",
    'content': lorem,
    'thread': "Thread 2",
    'author': "author2",
    'tags':"gaming",
    'date': date.today()
  },
  {
    'title': "Test Post 5",
    'content': lorem,
    'thread': "Thread 2",
    'author': "author3",
    'tags':"lifestyle,art",
    'date': date.today()
  }
]

for post in posts:
  cur.execute(f"INSERT INTO forum_post (title, content, thread, author, tags, date) VALUES ({post['title']},{post['content']}, {post['thread']},{post['author']}, {post['tags']},{post['date']})")
  cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", posts)
  con.commit()