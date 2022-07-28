from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import db
from .models import Forum_Comment, Forum_Post, User

forums = Blueprint('forums', __name__)

# Forum routes
@forums.route("/forums") #redirect to default forum
def forums_redirect():
    return redirect(url_for('forums.forums_page', thread = 1))

@forums.route("/forums/<thread>") #<thread> designates the id of which thread user is currently in
def forums_page(thread):
    # Query db for posts by descending order by date to show most recent posts first
    posts = Forum_Post.query.order_by(Forum_Post.date.desc())
    return render_template('/forums/forums.html', title ='forums', posts = posts, thread=thread)

#Forum create post form GET request
@forums.route('/forums/<thread>/create_post', methods=['GET'])
@login_required
def forums_create_post_form(thread):
    return render_template('/forums/forums_create_post.html', title ='forums', thread=thread)

#Forum create post POST request
@forums.route('/forums/create_post', methods=['POST'])
@login_required
def forums_create_post():
    # Get request data
    thread = request.form.get('thread')
    title = request.form.get('title')
    content = request.form.get('content')

    # create new post
    new_post = Forum_Post(thread=thread, title=title, content=content, author = current_user.name)

    # add the new post to the database
    db.session.add(new_post)
    db.session.commit()

    # reload profile page
    return redirect(url_for('forums.forums_page', thread = thread))
