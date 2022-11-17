from flask import Blueprint, render_template, redirect, url_for, request
from datetime import date
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from app.db.models import Thread, ForumPost, ForumComment
from app.admin import admin_permission
from app.db import db

forums_blueprint = Blueprint('forums_blueprint', __name__, url_prefix="/forums")

@forums_blueprint.route("/")
def forums():
  threads = Thread.query.filter_by().all()

  return render_template('forums/threads.html', title ='Forum', threads = threads)

@forums_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_thread():
  if request.method == 'POST':
    thread = request.form.get('thread')
    new_thread = Thread(name=thread)
    db.session.add(new_thread)
    db.session.commit()

    return redirect(url_for("forums_blueprint.forums"))

  return render_template('forums/create_thread.html')

@forums_blueprint.route("/<thread>")
def thread(thread):
  posts = ForumPost.query.filter_by(thread=thread).all()  

  return render_template('forums/thread.html', thread = thread, title = thread, posts = posts)

@forums_blueprint.route('/<thread>/create', methods=['GET', 'POST'])
@login_required
def create_post(thread):
  if request.method == 'POST':
    title = request.form.get('title')
    content = request.form.get('content')
    tags = request.form.get('tags')
    today = date.today()
    author = current_user.name
    new_post = ForumPost(title=title, thread=thread, content=content, tags= tags, date= today, author=author)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for("forums_blueprint.thread", thread=thread))

  return render_template('forums/create_post.html', thread=thread)

@forums_blueprint.route("/<thread>/<post_title>", methods=['GET', 'POST'])
def post(post_title, thread):
  if request.method == 'POST':
    post = ForumPost.query.filter_by(title=post_title).first()
    post_id = post.id
    content = request.form.get('content')
    today = date.today()
    author = current_user.name
    new_comment = ForumComment( content=content, post_id= post_id, date= today, author=author)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for("forums_blueprint.post", post_title=post_title, thread=thread))

  post = ForumPost.query.filter_by(title=post_title).first()
  comments = ForumComment.query.filter_by(post_id=post.id).all()

  return render_template('forums/post.html', title = post_title, post = post, comments = comments, thread=thread)

@forums_blueprint.route('/delete/thread/<id>', methods=['POST'])
def delete_thread(id):
  thread = Thread.query.filter_by(id=id).first()
  db.session.delete(thread)
  db.session.commit()

  return redirect(url_for('forums_blueprint.forums'))

@forums_blueprint.route('/delete/post/<id>', methods=['POST'])
def delete_post(id):
  post = ForumPost.query.filter_by(id=id).first()
  thread = post.thread
  db.session.delete(post)
  db.session.commit()

  return redirect(url_for('forums_blueprint.thread', thread=thread))

@forums_blueprint.route('/delete/comment/<id>', methods=['POST'])
def delete_comment(id):
  comment = ForumComment.query.filter_by(id=id).first()
  db.session.delete(comment)
  db.session.commit()

  return redirect(url_for('delete_comment'))
