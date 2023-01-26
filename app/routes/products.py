from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required
from app.util.security import admin_permission
from app.db import db
from app.db.models import Product
from app.util.s3 import conn
from werkzeug.utils import secure_filename
from app.db.util import paginate

product_blueprint = Blueprint('product_blueprint',
                              __name__, url_prefix="/products")


@product_blueprint.route('/', methods=["GET", "POST"])
def products():
    is_admin = admin_permission.can()
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    products = paginate(Product, page=page, key="name", pages=9)
    for product in products:
        product.card_image_url = conn.get_URL(product.card_image_url)

    return render_template('products/products.html', is_admin=is_admin, products=products, page=page)

@product_blueprint.route('/<product_id>')
def product(product_id):
    is_admin = admin_permission.can()
    product = Product.query.filter_by(id=product_id).first()
    product.stock_image_url = conn.get_URL(product.stock_image_url)

    return render_template('products/product.html', is_admin=is_admin, product=product, page=1)

@product_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        description = request.form.get('description')
        tags = request.form.get('tags')

        large_file = request.files["file-large"]
        small_file = request.files["file-small"]

        # Image create handling
        large_url = large_file.filename if "file-large" in request.files and large_file.filename != "" else '/static/images/test.png'
        small_url = small_file.filename if "file-small" in request.files and small_file.filename != "" else '/static/images/test.png'

        
        if large_file:
            large_file.filename = secure_filename(large_file.filename)
            large_url = conn.create(large_file)  

        if small_file:
            small_file.filename = secure_filename(small_file.filename)
            small_url = conn.create(small_file)
                
        product = Product(name=name, price=price, description=description, tags=tags,
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
        product.tags = request.form.get('tags')

        # Image create handling
        large_file = request.files["file-large"]
        small_file = request.files["file-small"]
        
        if large_file:
            large_file.filename = secure_filename(large_file.filename)
            large = conn.create(large_file)
        else:
            large = product.stock_image_url
        
        if small_file:
            small_file.filename = secure_filename(small_file.filename)
            small = conn.create(small_file)
        else:
            small = product.card_image_url

        product.stock_image_url = large if large and large != "" else '/static/images/test.png'
        product.card_image_url = small if small and small != "" else '/static/images/test.png'

        db.session.commit()

        return redirect(url_for('product_blueprint.product', product_id=id))

    product.stock_image_url = conn.get_URL(product.stock_image_url)
    product.card_image_url = conn.get_URL(product.card_image_url)

    return render_template('products/product_edit.html', product=product)


@product_blueprint.route('/delete/<id>', methods=['POST'])
@login_required
@admin_permission.require()
def delete_product(id):
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('product_blueprint.products'))


@product_blueprint.route('/create/<id>', methods=['GET', 'POST'])
def create_file(id):
    if request.method == 'POST':
        if "file" not in request.files:

            return "No file key in request.files"

        file = request.files["file"]

        if file.filename == "":

            return "Please select a file"

        if file:
            file.filename = secure_filename(file.filename)
            conn.create(file)

            product = Product.query.filter_by(id=id).first()
            product.card_image_url = file.filename
            product.stock_image_url = file.filename

            db.session.commit()

            return redirect(url_for('product_blueprint.product',
                                    product_id=id))

        else:

            return redirect(url_for('product_blueprint.product',
                                    product_id=id))

    return render_template('products/product_image_create.html')
