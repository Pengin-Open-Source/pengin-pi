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
    return redirect(url_for(f"forums_blueprint.thread", thread=thread))
  return render_template('forums/create_post.html', thread=thread)

@forums_blueprint.route("/<thread>/<post_title>")
def post(post_title, thread):
  post = ForumPost.query.filter_by(title=post_title).first()
  comments = ForumComment.query.filter_by(post_id=post.id).all()
  return render_template('forums/post.html', title = post_title, post = post, comments = comments)