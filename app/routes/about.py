from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.util.security import admin_permission
from app.db import db
from app.db.models import About

about_blueprint = Blueprint('about_blueprint', __name__,
                            url_prefix="/about")


@about_blueprint.route("/")
def view():
    # about = About.query.filter_by().first()

    return render_template('about/view.html')


@about_blueprint.route('/about/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create():
    if request.method == 'POST':

        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("about_blueprint.view"))

    return render_template('about/create.html')
