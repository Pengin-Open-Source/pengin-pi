from flask import Blueprint, render_template


main = Blueprint('main', __name__)

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
