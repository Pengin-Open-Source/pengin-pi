from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models import Customer, Orders, Company, User

customer_info = Blueprint('customer_info', __name__, url_prefix="/customers")
admin_permission = Permission(RoleNeed('admin'))


@customer_info.route('/create', methods=['GET', 'POST'])
#@login_required
#@admin_permission.require()
def create_customer():
    if request.method == 'POST':
        order_id = request.form.get('order_id')

        if request.form.get('company_id') != "":
            customer_id = request.form.get('company_id')
            new_customer = Customer(company_id=customer_id)
            db.session.add(new_customer)
            db.session.commit()

        elif request.form.get('user_id') != "":
            customer_id = request.form.get('user_id')
            new_customer = Customer(user_id=customer_id)
            db.session.add(new_customer)
            db.session.commit()

        elif request.form.get('new_company') != "":
            name = request.form.get('new_company')
            new_company = Company(name=name)
            db.session.add(new_company)
            db.session.commit()

            customer_id = new_company.id
            new_customer = Customer(company_id=customer_id)
            db.session.add(new_customer)
            db.session.commit()

        elif request.form.get('new_user') != "":
            name = request.form.get('new_user')
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()

            customer_id = new_user.id
            new_customer = Customer(user_id=customer_id)
            db.session.add(new_customer)
            db.session.commit()

        order = Orders(id=order_id)
        order.customer_id = new_customer.id
        db.session.commit()

        return redirect(url_for("home_blueprint.home"))

    orders = Orders.query.all()
    company_customers = Company.query.all()
    user_customers = User.query.all()

    return render_template('customer/customer_create.html', orders=orders,
                           company_customers=company_customers,
                           user_customers=user_customers)



@customer_info.route('<order_id>/edit', methods=['GET', 'POST'])
#@login_required
#@admin_permission.require()
def edit_customer(order_id):
    order_customer_id = Orders.query.filter_by(id=order_id).first().customer_id
    customer = Customer.query.filter_by(id=order_customer_id).first()

    if request.method == 'POST':
        if request.form.get('company_id') != "":
            customer_id = request.form.get('company_id')
            customer.company_id = customer_id
            db.session.commit()

        elif request.form.get('user_id') != "":
            customer_id = request.form.get('user_id')
            customer.user_id = customer_id
            db.session.commit()

        elif request.form.get('new_company') != "":
            name = request.form.get('new_company')
            new_company = Company(name=name)
            db.session.add(new_company)
            db.session.commit()

            customer_id = new_company.id
            new_customer = Customer(company_id=customer_id)
            db.session.add(new_customer)
            db.session.commit()

        elif request.form.get('new_user') != "":
            name = request.form.get('new_user')
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()

            customer_id = new_user.id
            new_customer = Customer(user_id=customer_id)
            db.session.add(new_customer)
            db.session.commit()

        order = Orders(id=order_id)
        order.customer_id = customer.id or new_customer.id
        db.session.commit()

        return redirect(url_for("home_blueprint.home"))

    company_customers = Company.query.all()
    user_customers = User.query.all()

    return render_template('customer/customer_edit.html', order_id=order_id,
                           user_customers=user_customers, customer=customer,
                           company_customers=company_customers)
