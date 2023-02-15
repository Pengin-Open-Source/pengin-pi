from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.util.uuid import id as ID
from app.db.models import Orders, OrdersList, Product, Customer, User, Company

order_info = Blueprint('order_info', __name__, url_prefix="/orders")
admin_permission = Permission(RoleNeed('admin'))


def get_orders():
    return Orders.query.all()


@order_info.route("/")
def display_orders_home():
    return render_template('order_info/order_info_main.html',
                           orders=get_orders(), is_admin=admin_permission.can())


@order_info.route('/<order_id>')
@login_required
def display_order_info(order_id):
    order = orders.query.get_or_404(order_id)

    return render_template('order_info/order_info.html', order=order)


@order_info.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_order():
    if request.method == 'POST':
        order_date = request.form.get('order_date')
        customer_id = request.form.get('customer_id')
        product_id = request.form.getlist('product_id')
        quantity = request.form.getlist('quantity')
        orders = [{'product': product, 'qty': qty} for product, qty in dict(zip(product_id, quantity)).items()]
        order_id = ID()

        new_order = Orders(id=order_id, order_date=order_date, customer_id=customer_id)
        db.session.add(new_order)

        for order in orders:
            new_order_list = OrdersList(quantity=order['qty'], orders_id=order_id, product_id=order['product'])
            db.session.add(new_order_list)
        db.session.commit()

        return redirect(url_for("order_info.display_order_info",
                                order_id=order_id))

    products = Product.query.all()
    customers = Customer.query.all()
    customers_with_names = []

    for customer in customers:
        if customer.company_id:
            name = Company.query.filter_by(id=customer.company_id).first().name
            customers_with_names.append({'customer': customer, 'name': name})
        elif customer.user_id:
            name = User.query.filter_by(id=customer.user_id).first().name
            customers_with_names.append({customer: customer, name: name})

    return render_template('order_info/order_info_create.html', products=products, customers_with_names=customers_with_names)


@order_info.route('/<order_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_order(order_id):
    order = Orders.query.get_or_404(order_id)
    order_list = order.orders_list
    customer = Customer.query.filter_by(id=order.customer_id).first()

    if customer.company_id:
        customer_name = Company.query.filter_by(id=customer.company_id).first().name
    elif customer.user_id:
        customer_name = User.query.filter_by(id=customer.user_id).first().name

    if request.method == 'POST':
        order.order_date = request.form.get('order_date')
        order.customer_id = request.form.get('customer_id')

        product_ids = request.form.getlist('product_id')
        quantities = request.form.getlist('quantity')
        order_list_ids = request.form.getlist('order-list-id')
        order_list_update = dict(zip(order_list_ids, zip(quantities, product_ids)))

        for k, v in order_list_update.items():
            order_list = OrdersList.query.filter_by(id=k).first()
            order_list.quantity = v[0]
            order_list.product_id = v[1]

        db.session.commit()

        return redirect(url_for("order_info.display_order_info",
                                order_id=order_id))

    products = Product.query.all()
    customers = Customer.query.all()
    customers_with_names = []
    product_names_by_id = {}

    for product in products:
        product_names_by_id[product.id] = product.name

    for customer in customers:
        if customer.company_id:
            name = Company.query.filter_by(id=customer.company_id).first().name
            customers_with_names.append({'customer': customer, 'name': name})
        elif customer.user_id:
            name = User.query.filter_by(id=customer.user_id).first().name
            customers_with_names.append({customer: customer, name: name})

    return render_template('order_info/order_info_edit.html', products=products,
                           customers_with_names=customers_with_names, order=order,
                           order_list=order_list, customer_name=customer_name, product_names_by_id=product_names_by_id)