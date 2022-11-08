from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import User, ForumPost, ForumComment, db

forums_blueprint = Blueprint('forums_blueprint', __name__, url_prefix="/forums")

@forums_blueprint.route("/")
def forums():
  query = ForumPost.query.with_entities(ForumPost.thread).distinct().all() # returns list of tuples with 1 element.
  threads = [row[0] for row in query]

  return render_template('forums/threads.html', title ='forum', threads = threads)

@forums_blueprint.route("/<thread>")
def thread(thread):
  posts = ForumPost.query.filter_by(thread=thread).all()  

  return render_template('forums/thread.html', thread=thread, title = thread, posts = posts)

@forums_blueprint.route("/<thread>/<post_title>")
def post(post_title, thread):
  post = ForumPost.query.filter_by(title=post_title).first()

  return render_template('forums/post.html', title = post_title, post = post)