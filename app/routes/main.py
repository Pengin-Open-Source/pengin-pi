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

#one function handles two separate routes
@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/about")
def about():
    return render_template('about.html', title ='about')

@main.route("/products")
def products():
    return render_template('products.html', title ='products')

@main.route("/forums")
def forums():
    return render_template('forums.html', title ='forums', posts = posts)
