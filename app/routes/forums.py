from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import User, ForumPost, ForumComment, db

#dummy variable list of dictionaries remove once DB queries setup
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

forums_blueprint = Blueprint('forums_blueprint', __name__, url_prefix="/forums")

@forums_blueprint.route("/")
def forums():
    
    return render_template('forums.html', title ='forums', posts = posts)