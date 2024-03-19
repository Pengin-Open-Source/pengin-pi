import os
import re
from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for, abort)
from flask_login import login_required, login_user, logout_user
from flask_principal import AnonymousIdentity, Identity, identity_changed
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.db import db
from app.db.models import User
from app.util.mail import send_mail
from app.util.security.recaptcha import verify_response
from app.util.security.limit import limiter
from app.util.uuid import id
from datetime import datetime, timedelta

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    # sample_messages = {'sender': ['hi', 'how are you'], 'receiver': ['hello', "i'm good"]}
    return render_template('authentication/login.html', primary_title='Login', item_title='Login')


@limiter.limit("10 per minute")
@auth.route('/login', methods=['POST'])
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
    return render_template('authentication/signup.html', site_key=os.getenv("SITE_KEY"), primary_title='Sign Up,')


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
                    password=generate_password_hash(
                        password, method='pbkdf2:sha256:600000'),
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


@auth.route('/generate-prt')
def generate_prt():
    return render_template('authentication/generate_prt_form.html', site_key=os.getenv("SITE_KEY"), primary_title='Forgot Password')


@limiter.limit("2 per minute")
@auth.route('/generate-prt', methods=["POST"])
@verify_response
def generate_prt_post():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Email does not exist.')
        return redirect(url_for("auth.generate_prt"))

    # allow password reset to validated users only
    if not user.validated:
        flash('This account is not validated.')
        return redirect(url_for("auth.generate_prt"))

    user.prt = id()
    user.prt_reset_date = datetime.utcnow()
    db.session.commit()

    send_mail(user.email, user.prt, "password_reset")
    return redirect(url_for('auth.login'))


@auth.route('/reset-password/<token>')
def reset_password(token):
    user = User.query.filter_by(prt=token).first()
    if user:
        return render_template('authentication/reset_password_form.html', email=user.email, token=token, site_key=os.getenv("SITE_KEY"), primary_title='Reset Password')

    abort(404)


@limiter.limit("2 per minute")
@auth.route('/reset-password/<token>', methods=["POST"])
@verify_response
def reset_password_post(token):
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    confirm_new_password = request.form.get('confirm_new_password')

    user = User.query.filter_by(email=email).first()
    if user:
        prt_expire_date = user.prt_reset_date + timedelta(minutes=60)

        if datetime.utcnow() > prt_expire_date:
            flash('Token expired.')
            return render_template('authentication/reset_password_form.html', email=user.email, token=token, site_key=os.getenv("SITE_KEY"))

        if new_password != confirm_new_password:
            flash('Passwords do not match.')
            return render_template('authentication/reset_password_form.html', email=user.email, token=token, site_key=os.getenv("SITE_KEY"))

        user.prt_consumption_date = datetime.utcnow()
        user.password = generate_password_hash(new_password,
                                               method='pbkdf2:sha256:600000')
        db.session.commit()
        return redirect(url_for('auth.login'))

    abort(404)
