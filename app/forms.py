from tkinter import Widget
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo 
from wtforms.widgets import TextArea

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), 
                            Length(min=5,max = 15)])
    
    email = StringField('Email',
                        validators=[DataRequired(), 
                        Email()])

    password = PasswordField('Password', 
                        validators=[DataRequired(), 
                        Length(min=5,max = 20)])

    password_confirm = PasswordField('Confirm Password', 
                        validators=[DataRequired(), 
                        Length(min=5,max = 20), EqualTo('password')]) #validator EqualTo means password_confirm must be equal to password
    
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), 
                        Email()])
    password = PasswordField('Password', 
                        validators=[DataRequired(), 
                        Length(min=5,max = 20)])

    #keeps the user logged in for a while using a secure cookie. 
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators = [DataRequired()])
    content = StringField('Content', validators = [DataRequired()], widget = TextArea() )
    author = StringField('Author', validators = [DataRequired()])
    submit = StringField('Submit')
