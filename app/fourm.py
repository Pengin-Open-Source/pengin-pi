from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import Forum_Post

forum = Blueprint('forum', __name__, url_prefix="/forums")


@forum.route("/post/<int:post_id>")
def display_post_details(post_id):
    # Commented out for now, testing the rendering.
    # forum_post = Forum_Post.query.get_or_404(post_id)
    # comments = Forum_Comment.query.get(post_id)
    # subcomments = Forum_Comment.query.get(parent_id)
    post = {
            'id': 1,
            'author': 'Sergey Astvatsaturov',
            'title': 'Single life!',
            'content': 'I rock',
            'date_posted': 'February 10th, 2022'
    }
    comments = [
        {
            'id': 1,
            'author': 'James',
            'content': 'This is a comment',
            'date_posted': 'February 10th, 2022'
        },
        {
            'id': 2,
            'author': 'Other James',
            'content': 'This is the other comment',
            'date_posted': 'February 11th, 2022'
        },
        {
            'id': 3,
            'author': 'Other Other James',
            'content': 'This is the other other comment',
            'date_posted': 'February 12th, 2022'
        }
    ]
    subcomments = [
        {
            'id': 1,
            'author': "Not James",
            'content': "This is the subcomment",
            'date_posted': 'February 15th 2022',
            'parent_comment': 1
        },
        {
            'id': 2,
            'author': "Other Not James",
            'content': "This is the other subcomment",
            'date_posted': 'February 14th 2022',
            'parent_comment': 2
        },
        {
            'id': 3,
            'author': "Other Other Not James",
            'content': "This is the other other subcomment",
            'date_posted': 'February 17th 2022',
            'parent_comment': 3
        },
        {
            'id': 4,
            'author': "Other Other Not James",
            'content': "This is the other other subcomment",
            'date_posted': 'February 17th 2022',
            'parent_comment': 1
        }
    ]

    return render_template('/forum/forum_details.html', forum_post=post, comments=comments, subcomments=subcomments)
