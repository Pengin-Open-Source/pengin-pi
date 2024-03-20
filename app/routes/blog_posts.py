from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models import BlogPost
from app.db.util import paginate

blogPosts = Blueprint('blogPosts', __name__)
admin_permission = Permission(RoleNeed('admin'))

def get_links():
    return []


@blogPosts.route("/blog", methods=["GET", "POST"])
def display_blog_home():
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    posts = paginate(BlogPost, page=page, key="title", pages=10)
    return render_template('blog/blog.html', posts=posts, primary_title='Blog',
                           left_title='Blog Posts')


@blogPosts.route("/blog/<post_id>")
def display_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1
    
    posts = paginate(BlogPost, page=page, key="title", pages=10)
    author_date = post.date  # TODO blogPost model has no author attribute.

   # (Looks like is_admin is already defined in inject globals in app/__init__.py, so it doesn't need to be added,
   # To the context processor again. we should just be able to remove references to is_admin elsewhere
    return render_template('blog/view.html', page=page, post=post, posts=posts,
                           blog_author_date=author_date)


@blogPosts.route('/blog/<post_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        post.tags = request.form.get('tags')
        
        db.session.commit()

        return redirect(url_for("blogPosts.display_post", post_id=post.id))
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    return render_template('blog/edit.html', post=post)


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
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    return render_template('blog/create.html', newPost=1)
