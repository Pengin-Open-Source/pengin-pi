from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user

from app.routes import forums
from . import db
from .models import User


#dummy variable list of dictionaries 

forums = Blueprint('forums', __name__)

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



@forums.route("/forums")
def forums():
    return render_template('forums.html', title ='forums', posts = posts)



@login_required
@forums.route("/forums/delete/")
def delete_forum():
    for post in posts:
        creator = posts[post]['author']
        if current_user == creator:
            db.session.delete(post)
            db.session.commit()

        return render_template('forums.html', title ='forums', posts = posts)
