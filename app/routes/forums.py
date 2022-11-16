from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
import app.models as models
from ..admin import admin_permission

forums_blueprint = Blueprint('forums_blueprint', __name__, url_prefix="/forums")

@forums_blueprint.route("/")
@admin_permission.require()
def forums():
  threads = models.Thread.query.filter_by().all()

  return render_template('forums/threads.html', title ='Forum', threads = threads)

@forums_blueprint.route("/<thread>")
def thread(thread):
  posts = models.ForumPost.query.filter_by(thread=thread).all()  

  return render_template('forums/thread.html', thread = thread, title = thread, posts = posts)

@forums_blueprint.route("/<thread>/<post_title>")
def post(post_title, thread):
  post = models.ForumPost.query.filter_by(title=post_title).first()
  comments = models.ForumComment.query.filter_by(post_id=post.id).all()

  return render_template('forums/post.html', title = post_title, post = post, comments = comments)