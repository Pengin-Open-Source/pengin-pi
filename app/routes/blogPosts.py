from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models import BlogPost


blogPosts = Blueprint('blogPosts', __name__)
admin_permission = Permission(RoleNeed('admin'))

def get_links():
    return BlogPost.query.all()

@blogPosts.route("/blog")
def display_blog_home():
    posts = BlogPost.query.limit(15)
    return render_template('blog/blog.html', posts=posts, links=get_links(), roles=current_user.roles)

@blogPosts.route("/blog/<post_id>")
def display_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog/view.html', post=post, links=get_links(), roles=current_user.roles)

@blogPosts.route('/blog/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        new_post = BlogPost(title=title, content=content, tags=tags)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("blogPosts.display_post", post_id=new_post.id))
    return render_template('blog/create.html', newPost=1, links=get_links())