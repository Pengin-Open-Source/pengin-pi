from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
import logging
from app.util.security import admin_permission
from app.db import db
from app.db.models import About

about_blueprint = Blueprint('about_blueprint', __name__,
                            url_prefix="/about")


@about_blueprint.route("/")
def view():
    about = About.query.filter_by().first()
    about_image = About.query.filter_by().first().image
    logging.info('Image S3 URL accessed:' + about_image)

    return render_template('about/about_main.html', about=about,
                           current_user=current_user, about_image=about_image)


@about_blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_about():
    # As there should only be one entry for about model it can be checked
    # whether this exists or not to allow creation or editing.
    exists = About.query.first() is not None

    # TODO Add image upload handling which assigns S3 URl to image variable
    image = 'Sort out file handling for image when products issue done'

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
            about.image = image

            db.session.commit()

            return redirect(url_for("about_blueprint.view"))

        return render_template('about/edit.html', about=about)
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            article = request.form.get('article')
            facebook = request.form.get('facebook')
            instagram = request.form.get('instagram')
            whatsapp = request.form.get('whatsapp')
            linkedin = request.form.get('linkedin')
            youtube = request.form.get('youtube')
            twitter = request.form.get('twitter')
            phone = request.form.get('phone')
            address1 = request.form.get('address1')
            address2 = request.form.get('address2')
            city = request.form.get('city')
            state = request.form.get('state')
            country = request.form.get('country')
            image = image

            new_about = About(name=name, article=article, facebook=facebook,
                              instagram=instagram, whatsapp=whatsapp,
                              linkedin=linkedin, youtube=youtube, phone=phone,
                              twitter=twitter, address1=address1,
                              address2=address2, city=city, state=state,
                              country=country, image=image)

            db.session.add(new_about)
            db.session.commit()

            return redirect(url_for("about_blueprint.view"))

        return render_template('about/create.html')
