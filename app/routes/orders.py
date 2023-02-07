from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models import Order, OrderList
from app.db.util import paginate

order_info = Blueprint('order_info', __name__, url_prefix="/orders")
admin_permission = Permission(RoleNeed('admin'))


@order_info.route("/",  methods=["GET", "POST"])
def display_orders_home():
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1
    
    # orders = paginate(Order, page=page, key="id", pages=5)

    # dummy data for display purpose
    orders = [
        {"id": 1},
        {"id": 2},
        {"id": 3},
        {"id": 4},
    ]

    return render_template('order_info/order_info_main.html',
                           orders=orders, is_admin=admin_permission.can())


@order_info.route("/<order_id>")
@login_required
def display_order_info(order_id):
    # order = order.query.get_or_404(order_id)

    # dummy data for display purpose
    order = {
        "id": "123456",
        "order_date": "99/99/9999",
        "customer_id": "654321",
        "order_list": [
            {
                "id": "id111",
                "quantity": 8,
                "product_id": "367d39cc-ec94-4135-a8b5-d5d21ae73710",
            },
            {
                "id": "id222",
                "quantity": 88,
                "product_id": "22976ec5-22a5-45a2-a680-1fd7492d4c82",
            }
        ]
    }

    return render_template('order_info/order_info.html', order=order)


@order_info.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_order():
    if request.method == 'POST':
        order_date = request.form.get('order_date')
        order_list = request.form.get('order_list')
        customer_id = request.form.get('customer_id')
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
