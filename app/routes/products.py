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
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        url = 'images/test.png'
        product = Product(name=name, price=price, description=description,
                          card_image_url=url, stock_image_url=url)

        db.session.add(product)
        db.session.commit()

        return redirect(url_for('product_blueprint.products'))

    return render_template('products/product_create.html')


@product_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_product(id):
    product = Product.query.filter_by(id=id).first()

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.description = request.form.get('description')
        db.session.commit()

        return redirect(url_for('product_blueprint.product', product_id=id))

    return render_template('products/product_edit.html', product=product)


@product_blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@admin_permission.require()
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('product_blueprint.products'))
