#import flask module
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
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

@main.route("/forums")
def forums():
    return render_template('forums.html', title ='forums', posts = posts)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html', name=current_user.name, email=current_user.email)


#edit profile info post
@main.route('/profile/edit_profile', methods=['POST'])
@login_required
def edit_profile_post():
    old_email = request.form.get('old_email')
    name = request.form.get('name')
    email = request.form.get('email')
    # Find user
    user = User.query.filter_by(email=old_email).first()

    # Update name
    user.name = name
    user.email = email
    db.session.commit()
    
    # Reload profile page
    return render_template('profile/profile.html', name=current_user.name, email=current_user.email)

#edit password post
@main.route('/profile/edit_password', methods=['POST'])
@login_required
def edit_password_post():
    email = request.form.get('email')
    curr_password = request.form.get('curr_password')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')

    # Find user
    user = User.query.filter_by(email=email).first()

    # Check if curr password is correct
    if not check_password_hash(user.password, curr_password):
        # Flash error
        flash('curr_password_error')
    
    # Check if new password and confirmation new password are the same
    if new_password == confirm_new_password:
        # Hash and save new password
        user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
    else:
        # Flash error
        flash('new_password_confirm_error')
    return redirect(url_for('main.profile')) # reload the page
    
