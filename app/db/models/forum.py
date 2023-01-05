from app.db import db
from app.util.uuid import id


class ForumPost(db.Model):
    __tablename__ = "forum_post"
    id = db.Column(db.String(36), default=id, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(10000))
    thread_id = db.Column(db.String(36), db.ForeignKey('thread.id',
                                                     ondelete='CASCADE'))
    author = db.Column(db.String(36), db.ForeignKey('user.id',
                                                  ondelete='CASCADE'))
    tags = db.Column(db.String(100))
    date = db.Column(db.String(100))
    comments = db.relationship('ForumComment')


class ForumComment(db.Model):
    __tablename__ = "forum_comment"
    id = db.Column(db.String(36), default=id, primary_key=True)
    post_id = db.Column(db.String(36), db.ForeignKey('forum_post.id',
                                                   ondelete='CASCADE'))
    content = db.Column(db.String(15000))
    author = db.Column(db.String(36), db.ForeignKey('user.id',
                                                  ondelete='CASCADE'))
    date = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))


class Thread(db.Model):
    __tablename__ = "thread"
    id = db.Column(db.String(36), default=id, primary_key=True)
    name = db.Column(db.String(100))
    roles = db.relationship('Role', secondary='thread_roles')


class ThreadRoles(db.Model):
    __tablename__ = "thread_roles"
    id = db.Column(db.String(36), default=id, primary_key=True)
    thread_id = db.Column(db.String(36), db.ForeignKey('thread.id',
                                                     ondelete='CASCADE'))
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id',
                                                   ondelete='CASCADE'))
