from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import db
from .models import Forum_Comment, Forum_Post, User

forums = Blueprint('forums', __name__)

# Helper to get the posts of a thread
def get_thread_posts(posts, limit):
    threads = {}
    for post in posts:
        # Ignore thread if home thread
        # if post.thread == 'home':
        #     continue
        if post.thread not in threads:
            threads[post.thread] = [post]
        elif len(threads[post.thread]) > limit:
            continue
        else:
            threads[post.thread].append(post)
    return threads

@forums.route('/forums/', defaults={'thread': 'home'}) # default forums thread is home
@forums.route('/forums/<thread>') #<thread> designates the id of which thread user is currently in
def forums_page(thread):
    # Query db for posts by descending order by date to show most recent posts first
    posts = Forum_Post.query.order_by(Forum_Post.date.desc())
    # Get threads
    threads = get_thread_posts(posts, 10)
    return render_template('/forums/forums.html', title ='forums', posts = posts, threads=threads, thread=thread)

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
    tags = request.form.get('tags')

    # create new post
    new_post = Forum_Post(thread=thread, title=title, content=content, tags=tags, author = current_user.name)

    # add the new post to the database
    db.session.add(new_post)
    db.session.commit()

    # reload profile page
    return redirect(url_for('forums.forums_page', thread = thread))
