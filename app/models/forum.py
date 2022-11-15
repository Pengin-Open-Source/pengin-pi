from .db import db
from sqlalchemy import func

class ForumPost(db.Model):
    __tablename__ = "forum_post"
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), unique=True)
    content = db.Column(db.String())
    thread = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String(), unique=True)
    date = db.Column(db.Integer(), unique=True)
    comment = db.relationship('ForumComment')


class ForumComment(db.Model):
    __tablename__ = "forum_comment"
    id = db.Column(db.Integer(), primary_key=True)
    post_id = db.Column(db.Integer(), db.ForeignKey(
        'forum_post.id', ondelete='CASCADE'))
    content = db.Column(db.String())
    author = db.Column(db.String())
    date = db.Column(db.Integer(), unique=True)
    zipcode = db.Column(db.Integer())

#adding forum_post from #112
class Forum_Post(db.Model):
    __tablename__ = 'forum_post'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String())
    content = db.Column(db.String())
    thread = db.Column(db.String())
    author = db.Column(db.String())
    tags = db.Column(db.String())
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
   # comments = db.relationship('Forum_Comment', secondary='ticket_forum')
       

class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    roles = db.relationship('Role', secondary='thread_roles')

class ThreadRoles(db.Model):
    __tablename__ = "thread_roles"
    id = db.Column(db.Integer(), primary_key=True)
    thread_id = db.Column(db.Integer(), db.ForeignKey('thread.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))