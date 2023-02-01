from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models import Order, OrderList

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
        order_date = request.form.get('order_date') # or datetime.utcnow() if null
        customer_id = request.form.get('customer_id')
        product_id_list = request.form.getlist('order-product-id')
        order_id_list = request.form.getlist('order-order-id')
        quantity_list = request.form.getlist('order-quantity')

        for i in range(len(quantity_list)):
            # As multiple lists to iterate through I have used a traditional
            # loop with a counter that can then be used to access that item
            # in each list in the same iteration.
            product_id = product_id_list[i]
            order_id = order_id_list[i]
            quantity = quantity_list[i]

            # TODO add each order to DB
            new_order = Order()
            db.session.add(new_order)
            db.session.commit()

            new_members_order = OrderMembers(id=new_order.id,
                                                user_id=current_user.id)
            db.session.add(new_members_order)
            db.session.commit()

        return redirect(url_for("order_info.display_order_info",
                                order_id=new_order.id))

    return render_template('order_info/order_info_create.html')
