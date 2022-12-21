from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.util.security import admin_permission
from app.db import db
from app.db.models import Product
from app.util.s3 import upload_file_to_s3
from werkzeug.utils import secure_filename
import os

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

        # Image upload handling
        if "file-large" not in request.files:
            large_url = '/static/images/test.png'

        large_file = request.files["file-large"]

        if large_file.filename == "":
            large_url = '/static/images/test.png'

        if large_file:
            large_file.filename = secure_filename(large_file.filename)
            large_output = upload_file_to_s3(large_file,
                                             os.getenv("S3_BUCKET"))
            large_url = large_output

        if "file-small" not in request.files:
            small_url = '/static/images/test.png'

        small_file = request.files["file-small"]

        if small_file.filename == "":
            small_url = '/static/images/test.png'

        if small_file:
            small_file.filename = secure_filename(small_file.filename)
            small_output = upload_file_to_s3(large_file,
                                             os.getenv("S3_BUCKET"))
            small_url = small_output

        product = Product(name=name, price=price, description=description,
                          card_image_url=small_url, stock_image_url=large_url)

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


@product_blueprint.route('/upload/<id>', methods=['GET', 'POST'])
def upload_file(id):
    if request.method == 'POST':
        if "file" not in request.files:

            return "No file key in request.files"

        file = request.files["file"]

        if file.filename == "":

            return "Please select a file"

        if file:
            file.filename = secure_filename(file.filename)
            output = upload_file_to_s3(file, os.getenv("S3_BUCKET"))

            product = Product.query.filter_by(id=id).first()
            product.card_image_url = output
            product.stock_image_url = output

            db.session.commit()

            return redirect(url_for('product_blueprint.product',
                                    product_id=id))

        else:

            return redirect(url_for('product_blueprint.product',
                                    product_id=id))

    return render_template('products/product_image_upload.html')
