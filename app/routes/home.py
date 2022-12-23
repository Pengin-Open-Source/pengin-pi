from flask import Blueprint, redirect, render_template, request, url_for
from app.db.models.home import Home
from app.db import db
import logging

home_blueprint = Blueprint('home_blueprint', __name__)


@home_blueprint.route("/")
@home_blueprint.route("/home")
def home():

    home = Home.query.first()
    home_image = Home.query.first().image
    logging.info('S3 Image accessed: ' + home_image)

    return render_template('home/home.html', home=home, home_image=home_image)


@home_blueprint.route("/home/edit")
def home_edit():
    # As there should only be one entry for home model it can be checked
    # whether this exists or not to allow creation or editing.
    exists = Home.query.first() is not None

    # TODO Add image upload handling which assigns S3 URl to image variable
    image = 'Sort out file handling for image when products issue done'

    if exists:
        home = Home.query.first()
        if request.method == 'POST':
            home.company_name = request.form.get('name')
            home.article = request.form.get('article')
            home.image = image

            db.session.commit()

            return redirect(url_for("home_blueprint.view"))

        return render_template('home/edit.html', home=home)
    else:
        if request.method == 'POST':
            company_name = request.form.get('name')
            article = request.form.get('article')
            image = image

            new_about = Home(company_name=company_name, article=article,
                             image=image)

            db.session.add(new_about)
            db.session.commit()

            return redirect(url_for("home_blueprint.view"))

        return render_template('home/create.html')
