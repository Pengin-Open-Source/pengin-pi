from flask import (Blueprint, current_app, flash, redirect, render_template,
                   request, session, url_for)
from flask_login import login_required, login_user, logout_user
from flask_principal import AnonymousIdentity, Identity, identity_changed
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from app.db import db
from app.db.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():

    return render_template('authentication/login.html')


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

    return render_template('authentication/signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    # if this returns a user, then the email already exists in database
    if user:
        # if a user is found, we want to redirect back to
        # signup page so user can try again
        flash('Email address already exists')

        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'),
                    validation_date=datetime.utcnow())
    db.session.add(new_user)
    db.session.commit()

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
