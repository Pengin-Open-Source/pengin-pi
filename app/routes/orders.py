from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models import Order, OrderList, Product, Customer
from itertools import groupby


order_info = Blueprint('order_info', __name__, url_prefix="/orders")
admin_permission = Permission(RoleNeed('admin'))

def get_orders():
    return Order.query.all()


@order_info.route("/")
def display_orders_home():
    return render_template('order_info/order_info_main.html',
                           orders=get_orders(), is_admin=admin_permission.can())


@order_info.route('/<order_id>')
@login_required
def display_order_info(order_id):
    order = order.query.get_or_404(order_id)

    return render_template('order_info/order_info.html', order=order)


@order_info.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_order():
    if request.method == 'POST':
        order_date = request.form.get('order_date') # TODO or datetime.utcnow() if null
        customer_id = request.form.get('customer_id')
        product_id = request.form.getlist('product_id')
        quantity = request.form.getlist('quantity')
        orders = [{'product': product, 'qty': qty} for product, qty in dict(zip(product_id, quantity)).items()]
        print(orders)

        for order in orders:
            new_order = Order(order_date=order_date, customer_id=customer_id)
            new_order_list = OrderList(quantity=order['qty'], order_id=new_order.id, product_id=order['product'])

            db.session.add(new_order)
            db.session.add(new_order_list)
            db.session.commit()

        return redirect(url_for("order_info.display_order_info",
                                order_id=new_order.id))

    products = Product.query.all()
    customers = Customer.query.all()

    return render_template('order_info/order_info_create.html', products=products, customers=customers)
