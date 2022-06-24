from flask import Blueprint, render_template, redirect, flash, url_for, request, abort
from flask_login import login_required, current_user
from . import db
from datetime import datetime
from .models import BlogPost


blogPosts = Blueprint('blogPosts', __name__)

# little helper to generate blog post links (inspired by tobuwebflask)
def get_links():
    return BlogPost.query.all()

# Logan Kiser:
# render all blog posts, potentially just their links
# not sure how the front-end folks would like to organize this, tobuwebflask
# goes with a list of links in a left-hand pane
@blogPosts.route("/blog")
def display_blog_home():
    all_posts = BlogPost.query.limit(15)
    return render_template('blog_main.html', posts=all_posts, links=get_links())


@blogPosts.route("/blog/<int:post_id>")
def display_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog/view.html', post=post, links=get_links())


@blogPosts.route('/blog/create', methods=['GET', 'POST'])
@login_required
def create_post():
    # handle POST method
    if request.method == 'POST':
        # process request data into convenient object vessel 
        title = request.form.get('title')
        user = current_user.id
        content = request.form.get('content')
        tags = request.form.get('tags')
        new_post = BlogPost(title=title, user=user, content=content, tags=tags)
        # insert post into database via BlogPost object
        db.session.add(new_post)
        db.session.commit()
        # render main blog page
        return redirect(url_for("blogPosts.display_blog_home"))
    # handle GET method
    return render_template('blog/create.html', newPost=1, links=get_links())


@blogPosts.route("/blog/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        # first retrieve object from DB
        updated_post = BlogPost.query.get(post_id)
        # update appropriate fields
        # this assumes all fields are passed via request
        updated_post.title = request.form.get('title')
        updated_post.title = request.form.get('content')
        updated_post.title = request.form.get('tags')
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('blogPosts.display_post', post_id=post.id))
    # populate form with existing data and allow user to alter blog post
    return render_template('blog/update.html', post=post, links=get_links())


@blogPosts.route("/blog/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blogPosts.all_posts'))
