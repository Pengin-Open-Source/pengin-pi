from flask import Blueprint, render_template, redirect, flash, url_for, request, abort
from flask_login import login_required, current_user
from . import db
from .models import Forum_Post
from datetime import datetime
from flask_principal import Permission, RoleNeed

forums = Blueprint('forums', __name__)
admin_permission = Permission(RoleNeed('admin'))


def get_forum_posts():
    return Forum_Post.query.all()


# Nothing is DB so pulled into here
posts = [
    {
        'author': 'Sergey Astvatsaturov',
        'title': 'Single life!',
        'content': 'I rock',
        'date_posted': 'February 10th, 2022'
    },

    {
        'author': 'Stuart Anderson',
        'title': 'Life in Japan',
        'content': "Can't wait to get back to the states",
        'date_posted': 'February 11th, 2022'
    },
    {
        'author': 'Dante Samuels',
        'title': 'Kid 2',
        'content': 'So excited!',
        'date_posted': 'February 13th, 2022'
    }
]


allowedPosts = [
    {
        'author': 'Andys Friend',
        'title': 'New Tech',
        'content': 'Cool!',
        'date_posted': 'July 20th, 2022'
    }

]

# From andy's code


@forums.route("/forums")
def display_forum_home():
    if current_user.is_authenticated:
        return render_template('forums.html', title='forums', posts=posts + allowedPosts)
    else:
        return render_template('forums.html', title='forums', posts=posts)


# Lokesh - not quite sure how to go about creating a way for
# authorized user to see certain posts based on id
# vs non-authorized ones. This would be just be for viewing
# not for creating or commenting, kind of like stack overflow
@forums.route("/forums/<string:forum_post_title>")
# Lokesh - I am thinking string would be the way to go so users
# could search by name rather than a number unknown to them
def forum_post(forum_title):
    post = Forum_Post.query.get_or_404(forum_title)
    return render_template('forums.html', title='forums', post=post)


@forums.route('/forums/createpost', methods=['GET', 'POST'])
@login_required
def create_forum_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        thread = request.form.get('thread')
        author = request.form.get('author')
        tags = request.form.get('tags')
        date = request.form.get('date')

        new_post = Forum_Post(title=title, content=content,
                              thread=thread, author=author, tags=tags, date=date)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("forums", forum_id=new_post.id))
        # TODO need a proper URL
    # handle GET method
    return render_template('forums', post=get_forum_posts())
    # TODO need a porper url somehwere to show/handle new post
