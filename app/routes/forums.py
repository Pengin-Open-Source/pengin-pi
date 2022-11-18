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

@forums_blueprint.route("/<thread_id>")
def thread(thread_id):
  posts = ForumPost.query.filter_by(thread_id=thread_id).all()  

  return render_template('forums/thread.html', thread_id = thread_id, title = thread_id, posts = posts)

@forums_blueprint.route('/<thread_id>/create', methods=['GET', 'POST'])
@login_required
def create_post(thread_id):
  if request.method == 'POST':
    title = request.form.get('title')
    content = request.form.get('content')
    tags = request.form.get('tags')
    today = date.today()
    author = current_user.name
    new_post = ForumPost(title=title, thread_id=thread_id, content=content, tags= tags, date= today, author=author)
    db.session.add(new_post)
    db.session.commit()

    return redirect(url_for("forums_blueprint.thread", thread_id=thread_id))

  return render_template('forums/create_post.html', thread_id=thread_id)

@forums_blueprint.route("/<thread_id>/<post_id>", methods=['GET', 'POST'])
def post(post_id, thread_id):
  if request.method == 'POST':
    post = ForumPost.query.filter_by(id=post_id).first()
    post_id = post.id
    content = request.form.get('content')
    today = date.today()
    author = current_user.name
    new_comment = ForumComment( content=content, post_id= post_id, date= today, author=author)
    db.session.add(new_comment)
    db.session.commit()

    return redirect(url_for("forums_blueprint.post", post_id=post_id, thread_id=thread_id))

  post = ForumPost.query.filter_by(id=post_id).first()
  comments = ForumComment.query.filter_by(post_id=post.id).all()

  return render_template('forums/post.html', title = post_id, post = post, comments = comments, thread_id=thread_id)

@forums_blueprint.route('/delete/thread/<id>', methods=['POST'])
def delete_thread(id):
  thread = Thread.query.filter_by(id=id).first()
  db.session.delete(thread)
  db.session.commit()

  return redirect(url_for('forums_blueprint.forums'))

@forums_blueprint.route('/delete/post/<id>', methods=['POST'])
def delete_post(id):
  post = ForumPost.query.filter_by(id=id).first()
  thread_id = post.thread_id
  db.session.delete(post)
  db.session.commit()

  return redirect(url_for('forums_blueprint.thread', thread_id=thread_id))

@forums_blueprint.route('/delete/comment/<id>', methods=['POST'])
def delete_comment(id):
  comment = ForumComment.query.filter_by(id=id).first()
  post = ForumPost.query.filter_by(id=comment.post_id).first()
  db.session.delete(comment)
  db.session.commit()

  return redirect(url_for('forums_blueprint.post', post_id=post.id, thread_id=post.thread_id))
