from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.security import admin_permission, user_permission
from app.db import db
from app.db.models import Product

product_blueprint = Blueprint('product_blueprint',
                              __name__, url_prefix="/products")


@product_blueprint.route('/')
def products():
    products = Product.query.filter_by().all()

    return render_template('products/products.html', products=products)


@product_blueprint.route('/<product_id>')
def product(product_id):
    product = Product.query.filter_by(id=product_id).first()

    return render_template('products/product.html', product=product)


@product_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_product():
    if request.method == 'POST':
        stuff = stuff

    return render_template('products/product_create.html')


@product_blueprint.route('/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_product():
    if request.method == 'POST':
        stuff = stuff

    return render_template('products/product_edit.html')
