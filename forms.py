#import modules
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo 

#we will write python classes that will be representative of our form, and then they will be converted into html format
#Create a registration form class 
#It will inherit from the FlaskForm Class

class RegistrationForm(FlaskForm):
    #First arguement is going to be the "username"
    username = StringField('Username', 
                            validators=[DataRequired(), 
                            Length(min=5,max = 15)])#Usernames must be between 5 and 15 characters (data required validators)
    
    email = StringField('Email',
                        validators=[DataRequired(), 
                        Email()])

    password = PasswordField('Password', 
                        validators=[DataRequired(), 
                        Length(min=5,max = 20)])#password must be between 5 and 15 characters (data required validators)

    password_confirm = PasswordField('Confirm Password', 
                        validators=[DataRequired(), 
                        Length(min=5,max = 20), EqualTo('password')]) #validator EqualTo means password_confirm must be equal to password
    
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    #login with your email
    email = StringField('Email', 
                        validators=[DataRequired(), 
                        Email()])
    #login password
    password = PasswordField('Password', 
                        validators=[DataRequired(), 
                        Length(min=5,max = 20)])#password must be between 5 and 15 characters (data required validators)

    #keeps the user logged in for a while using a secure cookie. 
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    