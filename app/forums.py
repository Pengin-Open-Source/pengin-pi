from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from requests import post

from app.routes import forums
from . import db
from .models import User, Forum_Post


#dummy variable list of dictionaries 

forums = Blueprint('forums', __name__)


@forums.route("/forums")
def forum_posts():
    forum_posts = Forum_Post.query.order_by(Forum_Post.date)
    return render_template('forums.html', title ='forums', posts = forum_posts)




@forums.route("/forums/delete/<int:id>")
def delete_forum(id):
    forum_post_to_delete = Forum_Post.query.get_or_404(id)
    if current_user == forum_post_to_delete.author:
        try:
            db.session.delete(forum_post_to_delete)
            db.session.commit()
            flash("Forum Post was deleted")

            posts = Forum_Post.query.order_by(Forum_Post.date)
            return render_template('forums.html', title ='forums', posts = forum_posts)

        except:
            flash("Sorry, there was a problem deleting the post ")

            posts = Forum_Post.query.order_by(Forum_Post.date)
            return render_template('forums.html', title ='forums', posts = forum_posts)