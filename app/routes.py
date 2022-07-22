#import flask module
from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from . import db
from .models import Forum_Comment, Forum_Post, User
from datetime import date

main = Blueprint('main', __name__)


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

# Forum routes
@main.route("/forums") #redirect to default forum
def forums_redirect():
    return redirect(url_for('main.forums', thread = 1))

@main.route("/forums/<thread>") #<thread> designates the id of which thread user is currently in
def forums(thread):
    # Query db for posts
    posts = []
    return render_template('forums.html', title ='forums', posts = posts, thread=thread)

#Forum create post POST request
@main.route('/forums/create_post', methods=['POST'])
@login_required
def forums_create_post():
    # Get request data
    thread = request.form.get('thread')
    title = request.form.get('title')
    content = request.form.get('body')
    
    # Get date
    date = date.today()

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_post = Forum_Post(thread=thread, title=title, content=content, date=date, author = current_user.name)

    # add the new post to the database
    db.session.add(new_post)
    db.session.commit()

    # reload profile page
    return redirect(url_for('main.forum', thread = thread))

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
    
