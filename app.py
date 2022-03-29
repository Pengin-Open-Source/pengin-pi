#import flask module
from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

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

#create app variable setting it to equal to an instance of the Flask class
#__name__ is special variable in python that is the name of the module
#__name__ can be equal to __main__ 
app = Flask(__name__)

#secret key
#make this an environment variable at some point temp for now
app.config['SECRET_KEY'] = 'temp'

#Routes are what you type into your browser to go to different webpages
#use route decorators 
#the "/" is the homepage
@app.route("/")
#also alows you to go to home page
#one function handles two seperate routes
@app.route("/home")
def home():
    #use render_template to return the home.html file 
    # posts = posts gives you access to the data in that variable in your template
    return render_template('home.html')


#create about page
@app.route("/about")
def about():
    return render_template('about.html', title ='about')

#create products page
@app.route("/products")
def products():
    return render_template('products.html', title ='products')

#create registration page
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success') 
        return redirect(url_for('home'))
    return render_template('register.html', title ='register', form=form)

#create login page
@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title ='login', form=form)

@app.route("/forums")
def forums():
    return render_template('forums.html', title ='forums', posts = posts)