from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timedelta
from app.util.uuid import id
from app.db import db
from app.db.models import User

profiles = Blueprint('profiles', __name__, url_prefix="/profile")


@profiles.route('/')
@login_required
def profile():
    now = datetime.utcnow()
    delta = current_user.validation_date + timedelta(minutes=5)
    can_re_validate = True if not current_user.validated and now > delta else False
    return render_template('profile/profile.html', name=current_user.name,
                           email=current_user.email, can_do=can_re_validate)

@profiles.route('/send_email')
@login_required
def send_email():
    now = datetime.utcnow()
    user = User.query.filter_by(id=current_user.id).first()
    delta = user.validation_date + timedelta(minutes=5)
    can_re_validate = True if not user.validated and now > delta else False
    if can_re_validate:
        user.validation_date = now
        user.validate_id = id()
        db.session.commit()
        print('test mail function')
        #mail function
    return redirect(url_for('profiles.profile'))


@profiles.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile_post():
    if request.method == 'POST':
        old_email = request.form.get('old_email')
        name = request.form.get('name')
        email = request.form.get('email')
        user = User.query.filter_by(email=old_email).first()
        user.name = name
        user.email = email
        db.session.commit()

        return redirect(url_for('profiles.profile'))

    return render_template('profile/profile_edit.html', name=current_user.name,
                           email=current_user.email)


@profiles.route('/edit_password', methods=['GET', 'POST'])
@login_required
def edit_password():
    if request.method == 'POST':
        email = request.form.get('email')
        old_password = request.form.get('curr_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')
        user = User.query.filter_by(email=email).first()
        if new_password == confirm_new_password:
            if check_password_hash(user.password, old_password):
                user.password = generate_password_hash(new_password,
                                                       method='sha256')
                db.session.add(user)
                db.session.commit()

                return redirect(url_for('profiles.profile'))

        flash('Please check your password details.')  # does nothing fix later

    return render_template('profile/password_edit.html',
                           name=current_user.name, email=current_user.email)
