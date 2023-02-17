from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models import Customer, Orders, Company, User

customer_info = Blueprint('customer_info', __name__, url_prefix="/customers")
admin_permission = Permission(RoleNeed('admin'))


@customer_info.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_customer():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        customer_id = request.form.get('customer_id')

        return redirect(url_for("order_info.display_order_info",
                                order_id=order_id))

    orders = Orders.query.all()
    company_customers = Company.query.all()
    user_customers = User.query.all()

    return render_template('customer/customer_create.html', orders=orders,
                           company_customers=company_customers,
                           user_customers=user_customers)

'''
@customer_info.route('/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_customer():
    if request.method == 'POST':

        return redirect(url_for("order_info.display_order_info",
                                order_id=new_order.id))

    return render_template('order_info/order_info_create.html')
'''