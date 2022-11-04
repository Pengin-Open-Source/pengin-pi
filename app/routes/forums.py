from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import User, ForumPost, ForumComment, db

forums_blueprint = Blueprint('forums_blueprint', __name__, url_prefix="/forums")

@forums_blueprint.route("/")
def forums():

  posts = ForumPost.query.all()  

  return render_template('forums/forums.html', title ='forums', posts = posts)