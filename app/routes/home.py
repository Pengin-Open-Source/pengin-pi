from flask import Blueprint, redirect, render_template, request, url_for
from app.db.models.home import Home
from app.db import db
from flask_login import login_required
from app.util.security import admin_permission
from app.util.s3 import conn
import logging
from werkzeug.utils import secure_filename

home_blueprint = Blueprint('home_blueprint', __name__)


@home_blueprint.route("/")
@home_blueprint.route("/index")
@home_blueprint.route("/home")
def home():

    home = Home.query.first()
    try:
        image = conn.get_URL(home.image)
    except:
        image = "/static/images/test.png"

    if home:
        logging.info('S3 Image accessed: ' + home.image)

    return render_template('home/home.html', home=home, image=image)


@home_blueprint.route("/home/edit", methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def home_edit():
    # As there should only be one entry for home model it can be checked
    # whether this exists or not to allow creation or editing.
    exists = Home.query.first() is not None

    # TODO Add image upload handling which assigns S3 URl to image variable
    image = 'Sort out file handling for image when products issue done'

    if exists:
        home = Home.query.first()

        if home.image:
            logging.info('Image accessed: ' + home.image)

        if request.method == 'POST':
            home.company_name = request.form.get('name')
            home.article = request.form.get('article')
            image = request.files["file"]
            url = image.filename if "file" in request.files and image.filename != "" else '/static/images/test.png'
            home.image = url
            if image:
                image.filename = secure_filename(image.filename)
                home.image = conn.create(image)
            
            db.session.commit()


            return redirect(url_for("home_blueprint.home"))

        return render_template('home/edit.html', home=home)
    elif request.method == 'POST':
            company_name = request.form.get('name')
            article = request.form.get('article')
            image = request.files["file"]
            url = image.filename if "file" in request.files and image.filename != "" else '/static/images/test.png'
            if image:
                image.filename = secure_filename(image.filename)
                url = conn.create(image)

            new_about = Home(company_name=company_name, article=article,
                             image=url)

            db.session.add(new_about)
            db.session.commit()

            return redirect(url_for("home_blueprint.home"))

    else:
        return render_template('home/create.html')
