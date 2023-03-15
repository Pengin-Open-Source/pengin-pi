import sqlite3
from datetime import date
import datetime

from werkzeug.security import generate_password_hash

from app import create_app
from app.util.uuid import id

create_app()

con = sqlite3.connect("instance/db.sqlite")
cur = con.cursor()

password = generate_password_hash('password', method='sha256')
lorem = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Quisque
         pharetra placerat nisl. Mauris vitae pretium est. Donec pharetra diam
         quam, quis lobortis nisi viverra nec. Ut sollicitudin nulla vitae
         nisl accumsan volutpat vel eget risus. In sed pharetra justo, sed
         malesuada quam. Curabitur blandit dictum leo, quis feugiat ipsum
         laoreet a. Nam molestie tristique viverra. Phasellus odio lacus,
         ultrices sed viverra eget, rutrum at orci. Aliquam non orci at ante
         posuere efficitur eget in diam. Aenean quis nulla vel turpis molestie
         fermentum nec sed ligula. Sed consectetur, sapien et aliquet
         porttitor, risus risus varius erat, eget elementum nibh velit ac
         odio. Etiam vel turpis elit. """
thread_id_1 = id()
thread_id_2 = id()
thread_id_3 = id()
thread_id_4 = id()
thread_id_5 = id()
thread_id_6 = id()
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
user_id_1 = id()
user_id_2 = id()
user_id_3 = id()
post_id_1 = id()
posts = [
  (
    post_id_1,
    "Test Post 1",
    lorem,
    thread_id_1,
    user_id_1,
    "lifestyle,politics,art",
    date.today()
  ),
  (
    id(),
    "Test Post 2",
    lorem,
    thread_id_1,
    user_id_1,
    "gaming,politics",
    date.today()
  ),
  (
    id(),
    "Test Post 3",
    lorem,
    thread_id_1,
    user_id_2,
    "lifestyle,gaming,art",
    date.today()
  ),
  (
    id(),
    "Test Post 4",
    lorem,
    thread_id_2,
    user_id_2,
    "gaming",
    date.today()
  ),
  (
    id(),
    "Test Post 5",
    lorem,
    thread_id_2,
    user_id_3,
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 6",
    lorem,
    thread_id_3,
    user_id_3,
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 7",
    lorem,
    thread_id_4,
    user_id_3,
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 8",
    lorem,
    thread_id_5,
    user_id_3,
    "lifestyle,art",
    date.today()
  ),
  (
    id(),
    "Test Post 9",
    lorem,
    thread_id_6,
    user_id_3,
    "lifestyle,art",
    date.today()
  )
]

comments = [
  (
    id(),
    post_id_1,
    "test comment1",
    user_id_1,
    date.today()
  ),
  (
    id(),
    post_id_1,
    "test comment2",
    user_id_3,
    date.today()
  )
]


users = [
  (
    user_id_1,
    "author1@gmail.com",
    "author1",
    password,
    True,
    datetime.datetime.utcnow(),
    id()
  ),
  (
    user_id_2,
    "author2@gmail.com",
    "author2",
    password,
    True,
    datetime.datetime.utcnow(),
    id()
  ),
  (
    user_id_3,
    "author3@gmail.com",
    "author3",
    password,
    False,
    datetime.datetime.utcnow(),
    id()
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

# threads 1-4 are public 5 and 6 are in their own groups,
# admin has access to all
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

ticket_id_1 = id()
ticket_id_2 = id()
ticket_id_3 = id()
ticket_id_4 = id()
ticket_id_5 = id()
tickets = [
  (
    ticket_id_1,
    user_id_1,
    "Ticket 1",
    "open",
    "",
    "something broke please help me",
    date.today()
  ),
  (
    ticket_id_2,
    user_id_1,
    "Ticket 2",
    "open",
    "",
    "something broke please help me",
    date.today()
  ),
  (
    ticket_id_3,
    user_id_1,
    "Ticket 3",
    "closed",
    "",
    "something broke please help me",
    date.today()
  ),
  (
    ticket_id_4,
    user_id_1,
    "Ticket 4",
    "resolved",
    date.today(),
    "something broke please help me",
    date.today()
  ),
  (
    ticket_id_5,
    user_id_1,
    "Ticket 5",
    "resolved",
    date.today(),
    "something broke please help me",
    date.today()
  )
]

ticket_comments = [
  (
    id(),
    ticket_id_1,
    user_id_1,
    date.today(),
    "Test Comment"
  ),
  (
    id(),
    ticket_id_1,
    user_id_1,
    date.today(),
    "Test Comment"
  ),
  (
    id(),
    ticket_id_1,
    user_id_1,
    date.today(),
    "Test Comment"
  ),
  (
    id(),
    ticket_id_1,
    user_id_1,
    date.today(),
    "Test Comment"
  )
]

events = [
  (
    id(),
    user_id_1,
    user_id_1,
    role_id_1,
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    "Test Event 1",
    "Test description 1",
    "Faketown"
  ),
  (
    id(),
    user_id_1,
    user_id_1,
    role_id_1,
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    "Test Event 2",
    "Test description 2",
    "Faketown"
  ),
  (
    id(),
    user_id_1,
    user_id_1,
    role_id_1,
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    "Test Event 3",
    "Test description 3",
    "Faketown"
  ),
  (
    id(),
    user_id_1,
    user_id_1,
    role_id_1,
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    "Test Event 4",
    "Test description 4",
    "Faketown"
  ),
  (
    id(),
    user_id_1,
    user_id_1,
    role_id_1,
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow(),
    "Test Event 5",
    "Test description 5",
    "Faketown"
  )
]

product_id_1 = id()
product_id_2 = id()

products = [
  (
    product_id_1,
    'Test Product 1',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    product_id_2,
    'Test Product 2',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    id(),
    'Test Product 3',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    id(),
    'Test Product 4',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    id(),
    'Test Product 5',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    id(),
    'Test Product 6',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    id(),
    'Test Product 7',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    id(),
    'Test Product 8',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  ),
  (
    id(),
    'Test Product 9',
    lorem,
    '$1',
    lorem,
    '/static/images/test.png',
    '/static/images/test.png'
  )
]

home = [
  (
    id(),
    'ExampleCorp',
    lorem,
    '/static/images/test.png'
  ),
]


about = [
  (
    id(),
    'ExampleCorp',
    '#',
    '#',
    '#',
    '#',
    '#',
    '#',
    '#',
    '000-0000-000',
    '123 Fakestreet',
    'Fakeborough',
    'Fake City',
    'Fakefornia',
    'Republic of Fakeland',
    lorem,
    '/static/images/test.png'
  )
]

customer_id_1 = id()
customer_id_2 = id()
customer_id_3 = id()

customers = [
  (
    customer_id_1,
    user_id_1,
    "cid",
    datetime.datetime.utcnow(),
  ),
  (
    customer_id_2,
    user_id_2,
    "cid2",
    datetime.datetime.utcnow(),
  ),
  (
    customer_id_3,
    user_id_3,
    "cid3",
    datetime.datetime.utcnow(),
  ),
]

addresses = [
  (
    id(),
    '123 Fakestreet (add1)',
    '456 Fakestreet (add2)',
    'Fake City',
    'Fake State',
    'Fake Country',
    '000-000-0000',
    'fakeemail@gmail.com',
    customer_id_1,
  )
]

contracts = [
  (
    id(),
    customer_id_1,
    "contract_type_1",
    "contract_content",
    datetime.datetime.utcnow(),
    datetime.datetime.utcnow()
  )
]

order_id = id()
orders = [
  (
    order_id,
    datetime.datetime.utcnow(),
    customer_id_1
  )
]

order_items = [
  (
    id(),
    product_id_1,
    order_id,
    10
  ),
  (
    id(),
    product_id_2,
    order_id,
    45
  )
]


cur.executemany("""INSERT INTO product (id, name, description,
                price, article, card_image_url, stock_image_url)
                VALUES(?,?,?,?,?,?,?)""", products)


cur.executemany("""INSERT INTO home (id, company_name, article, image)
                VALUES(?,?,?,?)""", home)

cur.executemany("""INSERT INTO about (id, name, twitter,facebook, instagram,
                whatsapp, linkedin, line, youtube, phone, address1, address2,
                city, state, country, article, image )
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", about)

cur.executemany("""INSERT INTO ticket_forum (id, user_id, summary,
                resolution_status, resolution_date, content, date)
                VALUES(?,?,?,?,?,?,?)""", tickets)
cur.executemany("""INSERT INTO ticket_comment (id, ticket_id, author_id, date,
                content) VALUES(?,?,?,?,?)""", ticket_comments)
cur.executemany("""INSERT INTO forum_post (id, title, content, thread_id,
                author, tags, date ) VALUES(?, ?, ?, ?, ?, ?, ?)""", posts)
cur.executemany("""INSERT INTO forum_comment (id, post_id, content, author,
                date ) VALUES(?, ?, ?, ?, ?)""", comments)
cur.executemany("""INSERT OR IGNORE INTO user (id, email, name, password, validated, validation_date, validation_id)
                VALUES(?, ?, ?, ?, ?, ?, ?)""", users)
cur.executemany("INSERT INTO roles (id, name) VALUES(?, ?)", roles)
cur.executemany("INSERT INTO thread (id, name) VALUES(?, ?)", threads)
cur.executemany("""INSERT INTO user_roles ( id, user_id, role_id)
                VALUES(?, ?,?)""", user_roles)
cur.executemany("""INSERT INTO thread_roles (id, role_id, thread_id)
                VALUES(?, ?,?)""", thread_roles)
cur.executemany("""INSERT INTO events (id, user_id, organizer, role, date_created, start_datetime, end_datetime, title, description, location)
                VALUES(?,?,?,?,?,?,?,?,?,?)""", events)

cur.executemany("""INSERT INTO shipping_address (id, address1, address2, city, state, country, phone, email, customer)
                VALUES(?,?,?,?,?,?,?,?,?)""", addresses)
cur.executemany("""INSERT INTO customer (id, user_id, company_id, date)
                VALUES(?,?,?,?)""", customers)
cur.executemany("""INSERT INTO contracts (id, customer_id, contract_type, content, service_date, expiration_date)
                VALUES(?,?,?,?,?,?)""", contracts)    
# cur.executemany("""INSERT INTO order (id, order_date, customer_id)
#                 VALUES(?,?,?)""", orders)
# cur.executemany("""INSERT INTO order_items (id, product_id, order_id, quantity)
#                 VALUES(?,?,?,?)""", order_items)
                
con.commit()
con.close()