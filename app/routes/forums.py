from datetime import date

from flask import Blueprint, abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.util.uuid import id
from app.db import db
from app.db.models import ForumComment, ForumPost, Thread, ThreadRoles, User, Role
from app.db.util import paginate
from app.util.security import (admin_permission, delete_comment_permission,
                               delete_post_permission, edit_comment_permission,
                               edit_post_permission, user_permission)

forums_blueprint = Blueprint('forums_blueprint', __name__,
                             url_prefix="/forums")


@forums_blueprint.route("/", methods=["GET", "POST"])
@login_required
def forums():
    """/forums/
    Default route for forum.
    Requires: user login
    Returns:
        _type_: forums/threads.html
    """
    threads = []
    thread_ids = []
    is_admin = admin_permission.can()
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1
    
    # TODO: could've got all unique threads whose role is in current_user's roles with a complex query alone
    if is_admin:
        threads = Thread.query.all()
    else:    
        for role in current_user.roles:
            role_thread_ids = (
                            ThreadRoles.query
                            .with_entities(ThreadRoles.thread_id)
                            .filter_by(role_id=role.id).all()
                            )
            thread_ids.extend(role_thread_ids)

        # Removes duplicates. TODO: return in ordered list
        unique_thread_ids = tuple(set(thread_ids))
        for thread_id_tuple in unique_thread_ids:
            thread = Thread.query.filter_by(id=thread_id_tuple[0]).first()
            threads.append(thread)
    
    threads = paginate(Thread, page=page, key="name", pages=10)

    return render_template('forums/threads.html', title='Forum',
                            threads=threads, is_admin=is_admin)


@forums_blueprint.route('/create', methods=['GET', 'POST'])
@admin_permission.require()
@login_required
def create_thread():
    """/forums/create
    Route for creating a thread.
    Requires: user login, admin
    Success Returns:
        _type_: forums_blueprint.forums
    Failure Returns:
        _type_: forums/create_thread.html
    """
    if request.method == 'POST':
        thread = request.form.get('thread')
        role_id = request.form.get('role')
        #role_id = Role.query.filter_by(name=role).first().id
        thread_id = id()
        new_thread = Thread(id=thread_id, name=thread)
        db.session.add(new_thread)
        new_threadrole = ThreadRoles(thread_id=thread_id, role_id=role_id)
        db.session.add(new_threadrole)
        db.session.commit()        

        return redirect(url_for("forums_blueprint.forums"))
    roles = Role.query.all()
    return render_template('forums/create_thread.html', roles=roles)


@forums_blueprint.route("/<thread_id>")
@login_required
def thread(thread_id):
    """/forums/<thread_id>
    Route for forum thread.
    Requires: user login
    Returns:
        _type_: forums/thread.html
    """
    posts = ForumPost.query.filter_by(thread_id=thread_id).all()
    thread = Thread.query.filter_by(id=thread_id).first()

    return render_template('forums/thread.html',
                           is_admin=admin_permission.can(),
                           can_delete=delete_post_permission,
                           can_edit=edit_post_permission,
                           thread_id=thread_id, title=thread.name,
                           posts=posts, current_user=current_user)


@forums_blueprint.route('/<thread_id>/create', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def create_post(thread_id):
    """/forums/<thread_id>/create
    Route for create forum post.
    Requires: user login, user permission
    Success Returns:
        _type_: forums_blueprint.thread
    Failure Returns:
        _type_: forums/create_post.html
    """
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        today = date.today()
        author = current_user.id
        new_post = ForumPost(title=title, thread_id=thread_id,
                             content=content, tags=tags, date=today,
                             author=author)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("forums_blueprint.thread",
                                thread_id=thread_id))

    return render_template('forums/create_post.html', thread_id=thread_id)


@forums_blueprint.route("/<thread_id>/<post_id>", methods=['GET', 'POST'])
@login_required
@user_permission.require()
def post(post_id, thread_id):
    """/forums/<thread_id>/<post_id>
    Route for authenticated post creation OR forum post.
    Requires: user login, user permission
    POST method Returns:
        _type_: forums_blueprint.post
    GET Returns:
        _type_: forums/post.html
    """
    if request.method == 'POST':
        post = ForumPost.query.filter_by(id=post_id).first()
        content = request.form.get('content')
        today = date.today()
        author = current_user.id
        new_comment = ForumComment(content=content, post_id=post_id,
                                   date=today, author=author)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("forums_blueprint.post", post_id=post_id,
                                thread_id=thread_id))

    post = ForumPost.query.filter_by(id=post_id).first()
    author = User.query.filter_by(id=post.author).first()
    comments = ForumComment.query.filter_by(post_id=post.id).all()
    comment_authors = {j: User.query.filter_by(id=j).first().name
                       for j in tuple(set([comment.author
                                           for comment in comments]))}

    return render_template('forums/post.html', comment_authors=comment_authors,
                           is_admin=admin_permission.can(), post_id=post_id,
                           can_delete_comment=delete_comment_permission,
                           can_edit_comment=edit_comment_permission,
                           can_delete_post=edit_post_permission,
                           can_edit_post=edit_post_permission,
                           author=author.name, post=post, comments=comments,
                           thread_id=thread_id, current_user=current_user)


@forums_blueprint.route('/delete/thread/<id>', methods=['POST'])
@login_required
@admin_permission.require()
def delete_thread(id):
    """/forums/delete/thread/<id>
    Route for authenticated thread deletion
    Requires: user login, admin
    POST Returns:
        _type_: forums_blueprint.forums
    """
    thread = Thread.query.filter_by(id=id).first()
    db.session.delete(thread)
    db.session.commit()

    return redirect(url_for('forums_blueprint.forums'))


@forums_blueprint.route('/delete/post/<id>', methods=['POST'])
@login_required
@user_permission.require()
def delete_post(id):
    """/forums/delete/post/<id>
    Route for authenticated forum post deletion
    Requires: user login, user need OR admin
    Success Returns:
        _type_: forums_blueprint.thread
    Failure Returns:
        _type_: 403 permissions error
    """
    permission = delete_post_permission(id)
    if permission.can() or admin_permission.can():
        post = ForumPost.query.filter_by(id=id).first()
        thread_id = post.thread_id
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for('forums_blueprint.thread',
                                thread_id=thread_id))

    abort(403)


@forums_blueprint.route('/delete/comment/<id>', methods=['POST'])
@login_required
@user_permission.require()
def delete_comment(id):
    """/forums/delete/comment/<id>
    Route for authenticated post comment deletion
    Requires: user login, user need OR admin
    Success Returns:
        _type_: forums_blueprint.post
    Failure Returns:
        _type_: 403 permissions error
    """
    permission = delete_comment_permission(id)
    if permission.can() or admin_permission.can():
        comment = ForumComment.query.filter_by(id=id).first()
        post = ForumPost.query.filter_by(id=comment.post_id).first()
        db.session.delete(comment)
        db.session.commit()

        return redirect(url_for('forums_blueprint.post', post_id=post.id,
                                thread_id=post.thread_id))

    abort(403)


@forums_blueprint.route('/<thread_id>/<post_id>/edit', methods=['POST', 'GET'])
@login_required
@user_permission.require()
def edit_post(thread_id, post_id):
    """/forums//<thread_id>/<post_id>/edit
    Route for authenticated forum post editing
    Requires: user login, user need OR admin
    POST Returns:
        Success Returns:
            _type_: forums_blueprint.thread
        Failure Returns:
            _type_: 403 permissions error
    GET Returns:
        _type_: forums/edit_post.html
    """

    post = ForumPost.query.filter_by(id=post_id).first()

    if request.method == 'POST':
        permission = edit_post_permission(post_id)
        if permission.can() or admin_permission.can():
            post.title = request.form.get('title')
            post.content = request.form.get('content')
            post.tags = request.form.get('tags')
            db.session.commit()

            return redirect(url_for("forums_blueprint.thread",
                                    thread_id=thread_id))

        abort(403)

    return render_template('forums/edit_post.html', post=post,
                           thread_id=thread_id, post_id=post_id)


@forums_blueprint.route('<thread_id>/<post_id>/<comment_id>/edit',
                        methods=['POST', 'GET'])
@login_required
@user_permission.require()
def edit_comment(thread_id, post_id, comment_id):
    """/forums/<comment_id>/edit
    Route for authenticated forum comment editing
    Requires: user login, user need OR admin
    POST Returns:
        Success Returns:
            _type_: forums_blueprint.post
        Failure Returns:
            _type_: 403 permissions error
    GET Returns:
        _type_: forums/edit_comment.html
    """

    comment = ForumComment.query.filter_by(id=comment_id).first()

    if request.method == 'POST':
        permission = edit_comment_permission(comment_id)
        if permission.can() or admin_permission.can():
            comment.content = request.form.get('content')
            db.session.commit()

            return redirect(url_for("forums_blueprint.post",
                                    post_id=post_id, thread_id=thread_id))

        abort(403)

    return render_template('forums/edit_comment.html', comment=comment,
                           post_id=post_id, thread_id=thread_id,
                           comment_id=comment_id)
