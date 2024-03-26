from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db
from app.db.models.orders import OrderChangeRequest, OrderHistory
from app.db.models.ticket import TicketForum
from app.util.uuid import id as ID
from app.db.models import Orders, OrdersList, Product, Customer, User, Company
from app.util.security import (admin_permission, user_permission)

order_info = Blueprint('order_info', __name__, url_prefix="/orders")
admin_permission = Permission(RoleNeed('admin'))


def get_orders():
    return Orders.query.all()

@order_info.route("/")
@login_required
@user_permission.require()
def display_orders_home():
    is_cancelled = request.args.get('is_cancelled')

    if is_cancelled == 'true':
        orders = Orders.query.filter_by(user_id=current_user.id, is_cancelled=True).all()
    elif is_cancelled == 'false' or is_cancelled is None:
        orders = Orders.query.filter_by(user_id=current_user.id, is_cancelled=False).all()

    customers = {order.customer_id: Customer.query.get(order.customer_id) for order in orders}

    for customer in customers.values():
        customer.company = Company.query.get(customer.company_id)
        customer.user = User.query.get(customer.user_id)
    
    return render_template('tickets/workflows/customer_orders_list.html', 
                           primary_title='Orders',
                           orders=orders, 
                           is_admin=admin_permission.can(),
                           customers=customers
                           )


@order_info.route('/<order_id>')
@login_required
@user_permission.require()
def display_order_info(order_id):
    order = Orders.query.get_or_404(order_id)
    products = {item.product_id: Product.query.get(item.product_id) for item in order.orders_list}

    return render_template('tickets/workflows/customer_order_info.html', order=order, products=products)


@order_info.route('/create', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def create_order():
    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        product_id = request.form.getlist('product_id')
        quantity = request.form.getlist('quantity')
        orders = [{'product': product, 'qty': qty} for product, qty in dict(zip(product_id, quantity)).items()]
        order_id = ID()

        # create a new Order object
        new_order = Orders(
            id=order_id, 
            order_date=datetime.now(), 
            customer_id=customer_id,
            user_id=current_user.id
            )
        db.session.add(new_order)

        # create a new OrderHistory object to store the order information in the case that it is updated or cancelled in the future
        order_history = OrderHistory(
            order_id=order_id,
            timestamp=datetime.now(),
            user_id=current_user.id,
            type='new order'
        )
        db.session.add(order_history)

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

    return render_template('tickets/workflows/customer_order_create.html', primary_title='Create Order', products=products, customers_with_names=customers_with_names)


@order_info.route('/<order_id>/edit', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def edit_order(order_id):
    order = Orders.query.get_or_404(order_id)
    order_list = order.orders_list
    customer = Customer.query.filter_by(id=order.customer_id).first()

    if customer.company_id:
        customer_name = Company.query.filter_by(id=customer.company_id).first().name
    elif customer.user_id:
        customer_name = User.query.filter_by(id=customer.user_id).first().name

    if request.method == 'POST':
        new_order_date = request.form.get('order_date')
        new_customer_id = request.form.get('customer_id')
        new_product_ids = request.form.getlist('product_id')
        new_quantities = request.form.getlist('quantity')

        # create a new OrderChangeRequest object with the order information submitted with the form
        order_change_request = OrderChangeRequest(
            order_id=order_id,
            order_date=new_order_date,
            customer_id=new_customer_id,
            timestamp=datetime.now(),
            user_id=current_user.id,
            status='pending'
        )

        db.session.add(order_change_request)
        db.session.commit()

        # create a new OrdersList object for each product
        for product_id, quantity in zip(new_product_ids, new_quantities):
            new_order_list = OrdersList(
                quantity=quantity,
                product_id=product_id,
                order_change_request_id=order_change_request.id # associate the new OrdersList with the new OrderChangeRequest object
            )
            db.session.add(new_order_list)
        
        db.session.commit()

        # create a new support ticket for the order change request
        ticket_summary = f"Order Change Request - Order ID: {order_id}"
        ticket_content = f"Changes to Order ID {order_id} pending approval. Please review and approve or reject the changes."

        ticket = TicketForum(
            summary=ticket_summary,
            content=ticket_content,
            date=datetime.now(),
            user_id=current_user.id,
            resolution_status = 'open',
            tags="order-change-request"
        )

        db.session.add(ticket)
        db.session.commit()

        return render_template('tickets/workflows/customer_order_success.html', primary_title='Request Submitted', order=order, ticket=ticket)

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

    return render_template('tickets/workflows/customer_order_edit.html', products=products, primary_title='Edit Order',
                           customers_with_names=customers_with_names, order=order,
                           order_list=order_list, customer_name=customer_name, product_names_by_id=product_names_by_id)

@order_info.route('/<order_id>/cancel', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def cancel_order(order_id):
    order = Orders.query.get_or_404(order_id)
    order_list = order.orders_list
    customer = Customer.query.filter_by(id=order.customer_id).first()

    if customer.company_id:
        customer_name = Company.query.filter_by(id=customer.company_id).first().name
    elif customer.user_id:
        customer_name = User.query.filter_by(id=customer.user_id).first().name

    if request.method == 'POST':

        ticket_summary = f"Cancel Order Request - Order ID: {order_id}"
        ticket_content = f"Cancellation of Order ID {order_id} pending approval. Please review and approve or reject the cancellation."

        ticket = TicketForum(
            summary=ticket_summary,
            content=ticket_content,
            date=datetime.now(),
            user_id=current_user.id,
            tags="order-cancel-request",
            resolution_status = 'open'
        )

        db.session.add(ticket)
        db.session.commit()

        return render_template('tickets/workflows/customer_order_success.html', primary_title='Request Submitted', order=order, ticket=ticket)

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

    return render_template('tickets/workflows/customer_order_edit.html', products=products, primary_title='Edit Order',
                           customers_with_names=customers_with_names, order=order,
                           order_list=order_list, customer_name=customer_name, product_names_by_id=product_names_by_id)


@order_info.route('/<order_id>/reorder', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def reorder(order_id):
    original_order = Orders.query.get_or_404(order_id)
    customer = Customer.query.filter_by(id=original_order.customer_id).first()
    original_orders_list = original_order.orders_list

    if request.method == 'POST':
        # create a new Order object with the same data as the original order
        new_order = Orders(
            order_date=datetime.now(),
            customer_id=original_order.customer_id,
            user_id=current_user.id
            )
        db.session.add(new_order)
        db.session.commit()

        # create a new OrderHistory object
        order_history = OrderHistory(
            order_id=new_order.id,
            timestamp=datetime.now(),
            user_id=current_user.id,
            type='reorder'
        )
        db.session.add(order_history)

        for original_order_item in original_orders_list:
            new_order_list = OrdersList(
                quantity=original_order_item.quantity, 
                orders_id=new_order.id, 
                product_id=original_order_item.product_id
                )
            db.session.add(new_order_list)

        db.session.commit()

        return render_template('tickets/workflows/customer_order_success.html', primary_title='Request Submitted', order=new_order)

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

        return render_template('tickets/workflows/customer_order_create.html', primary_title='Create Order', products=products, customers_with_names=customers_with_names)
