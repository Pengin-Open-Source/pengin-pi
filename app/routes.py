#import flask module
from flask import Blueprint, render_template

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


## TODO: move the ticket routes to the proper file (e.g. forums.py?)

@main.route("/tickets")
def tickets():
    return render_template('ticket/ticket_main.html')