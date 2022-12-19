from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.security import admin_permission, user_permission
from app.db import db
from app.db.models import User

product_blueprint = Blueprint('product_blueprint',
                              __name__, url_prefix="/products")


@product_blueprint.route('/')
def products():

    return render_template('products/products.html')


@product_blueprint.route('/<product_id>')
def product(product_id):

    return render_template('products/product.html', product_id=product_id)


@product_blueprint.route('/create_product', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_product():
    if request.method == 'POST':
        stuff = stuff

    return render_template('products/product_create.html')


@product_blueprint.route('/edit_product', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_product():
    if request.method == 'POST':
        stuff = stuff

    return render_template('products/product_edit.html')
