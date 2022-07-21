#import flask module
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import db
from .models import User

main = Blueprint('main', __name__)

#dummy variable list of dictionaries 
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


#Routes are what you type into your browser to go to different webpages
#use route decorators 
#the "/" is the homepage
@main.route("/")
#also alows you to go to home page
#one function handles two seperate routes
@main.route("/home")
def home():
    #use render_template to return the home.html file 
    # posts = posts gives you access to the data in that variable in your template
    return render_template('home.html')


#create about page
@main.route("/about")
def about():
    return render_template('about.html', title ='about')

#create products page
@main.route("/products")
def products():
    return render_template('products.html', title ='products')

@main.route("/forums/<id>") #id designates which forum, could use a string or int
def forums(id):
    return render_template('forums.html', title ='forums', posts = posts, id=id)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html', name=current_user.name, email=current_user.email)


# TODO finish profile editing feature / test that it works
#edit profile info post
@main.route('/profile/edit_profile', methods=['POST'])
@login_required
def edit_profile_post():
    old_email = request.form.get('old_email')
    name = request.form.get('name')
    email = request.form.get('email')
    # find user
    user = User.query.filter_by(email=old_email).first()

    # update name
    user.name = name
    user.email = email
    db.session.commit()
    
    # reload profile page
    return redirect(url_for('main.profile'))

@main.route('/edit_password')
def edit_password():
    return render_template('edit_password.html')

@main.route('/edit_password', methods=['POST'])
def edit_password_post():
    return redirect(url_for('main.profile'))
    
