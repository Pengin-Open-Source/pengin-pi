from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import User, ForumPost, ForumComment, db

forums_blueprint = Blueprint('forums_blueprint', __name__, url_prefix="/forums")

@forums_blueprint.route("/")
def forums():
  threads = ["Thread 1", "Thread 2", "Thread 3", "Thread 4", "Thread 5"]

  return render_template('forums/threads.html', title ='forum', threads = threads)

@forums_blueprint.route("/<thread>")
def thread(thread):
  print(thread)
  posts = ForumPost.query.filter_by(thread=thread).all()  

  return render_template('forums/thread.html', title =thread, posts = posts)

@forums_blueprint.route("/<thread>/<post>")
def post(post):
  display_post = ForumPost.query.filter_by(post=post)

  return render_template('forums/post.html', title = display_post.title, post = display_post)