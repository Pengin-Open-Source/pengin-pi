import os
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import login_required, login_user, logout_user
from flask_principal import AnonymousIdentity, Identity, identity_changed
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.db import db
from app.db.models import User
from app.util.mail import send_mail
from app.util.security.recaptcha import verify_response
from app.util.security.limit import limiter
import re

#from app.util.log import log


auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('authentication/login.html', site_key=os.getenv("SITE_KEY"))

@limiter.limit("10 per minute")
@auth.route('/login', methods=['POST'])
@verify_response
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')

        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    identity_changed.send(current_app._get_current_object(),
                          identity=Identity(user.id))

    return redirect(url_for('profiles.profile'))


@auth.route('/signup')
def signup():
    return render_template('authentication/signup.html', site_key=os.getenv("SITE_KEY"))


@limiter.limit("3 per minute")
@auth.route('/signup', methods=['POST'])
@verify_response
def signup_post():
    def is_valid_email(mail):
        email_regex = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}')
        """Checks if the given email address is valid."""
        email_valid = email_regex.match(mail) is not None
        email_exists = True if User.query.filter_by(email=email).first() else False
        
        return (email_valid and not email_exists)
        
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    # if this returns a user, then the email already exists in database
    if not is_valid_email(email):
        # if a user is found, we want to redirect back to
        # signup page so user can try again
        flash('Email address already exists or invalid email.')

        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'),
                    validation_date=datetime.utcnow())
    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    try:
        send_mail(user.email, user.validation_id)
    except Exception as e:
        print("Error: ", e)

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return redirect(url_for('home_blueprint.home'))
