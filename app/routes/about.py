from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.util.security import admin_permission
from app.db import db
from app.db.models import About

about_blueprint = Blueprint('about_blueprint', __name__,
                            url_prefix="/about")


@about_blueprint.route("/")
def view():
    about = About.query.filter_by().first()

    return render_template('about/about_main.html', about=about,
                           current_user=current_user)


@about_blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_about():
    exists = About.query.first() is not None

    if exists:
        about = About.query.first()
        if request.method == 'POST':
            about.name = request.form.get('name')
            about.article = request.form.get('article')
            about.facebook = request.form.get('facebook')
            about.instagram = request.form.get('instagram')
            about.whatsapp = request.form.get('whatsapp')
            about.linkedin = request.form.get('linkedin')
            about.youtube = request.form.get('youtube')
            about.twitter = request.form.get('twitter')
            about.phone = request.form.get('phone')
            about.address1 = request.form.get('address1')
            about.address2 = request.form.get('address2')
            about.city = request.form.get('city')
            about.state = request.form.get('state')
            about.country = request.form.get('country')

            db.session.commit()

            return redirect(url_for("about_blueprint.view"))

        return render_template('about/edit.html', about=about)
    else:
        if request.method == 'POST':

            db.session.add()
            db.session.commit()

            return redirect(url_for("about_blueprint.view"))

        return render_template('about/create.html')
