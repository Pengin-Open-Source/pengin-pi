from flask import Blueprint, render_template, redirect, flash, url_for, request, abort
from flask_login import login_required, current_user
from . import db
from datetime import datetime
from .models import BlogPost


blogPosts = Blueprint('blogPosts', __name__)

@blogPosts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
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
    # handle GET method
    return render_template('create_post.html')

@blogPosts.route("/post/<int:post_id>")
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@blogPosts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@blogPosts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))