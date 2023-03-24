from app.db import db
from app.util.uuid import id


class ForumPost(db.Model):
    __tablename__ = "forum_post"
    id = db.Column(db.String(36), default=id, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    tags = db.Column(db.String(150))
    date = db.Column(db.String(100))


class ForumComment(db.Model):
    __tablename__ = "forum_comment"
    id = db.Column(db.String(36), default=id, primary_key=True)
    content = db.Column(db.Text)
    date = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))


class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.String(36), default=id, primary_key=True)
    name = db.Column(db.String(100))


class ThreadRoles(db.Model):
    __tablename__ = "thread_roles"
    id = db.Column(db.String(36), default=id, primary_key=True)
