from datetime import date, datetime
import re

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.db import db
from app.db.models import TicketComment, TicketForum, User, Orders, OrdersList
from app.db.models.orders import OrderChangeRequest, OrderHistory
from app.db.models.product import Product
from app.db.util import paginate

# import the permissions related to tickets
from app.util.security import (admin_permission,
                               delete_ticket_comment_permission,
                               delete_ticket_permission,
                               edit_ticket_comment_permission,
                               edit_ticket_permission, user_permission)

ticket_blueprint = Blueprint('ticket_blueprint', __name__,
                             url_prefix="/tickets")


@ticket_blueprint.route("/", methods=["GET", "POST"])
@login_required
def tickets():
    status = request.args.get('status')
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    if status == 'all':
        tickets = paginate(TicketForum, page=page, pages=20)
        # filter by company once company/customer model fixed
    else:
        tickets = paginate(TicketForum, page=page, pages=20, filters={"resolution_status": status})

    return render_template('tickets/ticket_list.html',
                           title="Tickets", tickets=tickets,
                           current_user=current_user, primary_title='Tickets')


@ticket_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def create_ticket():
    if request.method == 'POST':
        summary = request.form.get('summary')
        content = request.form.get('content')
        tags = request.form.get('tags')
        today = date.today()
        user_id = current_user.id
        resolution_status = 'open'
        new_ticket = TicketForum(summary=summary,
                                 content=content, tags=tags,
                                 user_id=user_id, date=today,
                                 resolution_status=resolution_status)
        db.session.add(new_ticket)
        db.session.commit()

        return redirect(url_for("ticket_blueprint.tickets"))

    return render_template('tickets/create_ticket.html')


@ticket_blueprint.route("/<ticket_id>", methods=['GET', 'POST'])
@login_required
@user_permission.require()
def ticket(ticket_id):
    if request.method == 'POST':
        content = request.form.get('content')
        today = date.today()
        author_id = current_user.id
        new_comment = TicketComment(ticket_id=ticket_id, content=content,
                                    date=today, author_id=author_id)
        db.session.add(new_comment)
        db.session.commit()

        return redirect(url_for("ticket_blueprint.ticket",
                                ticket_id=ticket_id))

    ticket = TicketForum.query.filter_by(id=ticket_id).first()
    author = User.query.filter_by(id=ticket.user_id).first().name
    comments = TicketComment.query.filter_by(ticket_id=ticket_id).all()
    comment_authors = {j: User.query.filter_by(id=j).first().name
                       for j in tuple(set([comment.author_id
                                           for comment in comments]))}
    
    order_id_match = re.search(r'Order ID: ([\w-]+)', ticket.summary)
    order_id = order_id_match.group(1) if order_id_match else None
    order = Orders.query.filter_by(id=order_id).first()
    
    return render_template('tickets/ticket.html',
                           is_admin=admin_permission.can(), author=author,
                           can_delete_ticket=delete_ticket_permission,
                           can_delete_comment=delete_ticket_comment_permission,
                           can_edit_ticket=edit_ticket_permission,
                           can_edit_comment=edit_ticket_comment_permission,
                           comment_authors=comment_authors, ticket=ticket,
                           comments=comments,
                           order=order,
                           primary_title='Ticket')


@ticket_blueprint.route('/delete/ticket/<id>', methods=['POST'])
@login_required
def delete_ticket(id):
    permission = delete_ticket_permission(id)
    if permission.can() or admin_permission.can():
        ticket = TicketForum.query.filter_by(id=id).first()
        db.session.delete(ticket)
        db.session.commit()

        return redirect(url_for('ticket_blueprint.tickets'))

    abort(403)


@ticket_blueprint.route('/delete/ticket-comment/<id>', methods=['POST'])
@login_required
def delete_ticket_comment(id):
    permission = delete_ticket_comment_permission(id)
    if permission.can() or admin_permission.can():
        comment = TicketComment.query.filter_by(id=id).first()
        db.session.delete(comment)
        db.session.commit()

        return redirect(url_for('ticket_blueprint.ticket',
                                ticket_id=comment.ticket_id))

    abort(403)


@ticket_blueprint.route('/edit/ticket/<id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(id):
    ticket = TicketForum.query.filter_by(id=id).first()

    if request.method == 'POST':
        permission = edit_ticket_permission(id)
        if permission.can() or admin_permission.can():
            ticket.summary = request.form.get('summary')
            ticket.content = request.form.get('content')
            ticket.tags = request.form.get('tags')
            db.session.commit()

            return redirect(url_for('ticket_blueprint.ticket',
                                    ticket_id=id))

        abort(403)

    return render_template('tickets/edit_ticket.html', ticket=ticket)


@ticket_blueprint.route('/edit/ticket-comment/<ticket_id>/<comment_id>',
                        methods=['GET', 'POST'])
@login_required
def edit_ticket_comment(ticket_id, comment_id):
    comment = TicketComment.query.filter_by(id=comment_id).first()

    if request.method == 'POST':
        permission = edit_ticket_comment_permission(comment_id)
        if permission.can() or admin_permission.can():
            comment.content = request.form.get('content')
            db.session.commit()

            return redirect(url_for("ticket_blueprint.ticket",
                                    ticket_id=ticket_id))

        abort(403)

    return render_template('tickets/edit_comment.html', comment=comment,
                           ticket_id=ticket_id)


@ticket_blueprint.route('/edit-status/<ticket_id>',
                        methods=['GET', 'POST'])
@login_required
def edit_ticket_status(ticket_id):
    ticket = TicketForum.query.filter_by(id=ticket_id).first()

    if request.method == 'POST':
        permission = edit_ticket_permission(ticket)
        if permission.can() or admin_permission.can():
            ticket.resolution_status = request.form.get('status')

            if request.form.get('status') == 'resolved':
                ticket.resolution_date = date.today()
            else:
                ticket.resolution_date = ''

            db.session.commit()

            return redirect(url_for("ticket_blueprint.ticket",
                                    ticket_id=ticket_id))

        abort(403)

    return render_template('tickets/edit_status.html', ticket_id=ticket_id)

@ticket_blueprint.route('/<ticket_id>/orders/<order_id>/review')
@login_required
@admin_permission.require()
def review_order(ticket_id, order_id):
    request_type = request.args.get('type')
    order = Orders.query.get_or_404(order_id)
    products = {item.product_id: Product.query.get(item.product_id) for item in order.orders_list}
    ticket = TicketForum.query.filter_by(id=ticket_id).first()

    order_change_request = OrderChangeRequest.query.filter_by(order_id=order_id).first()
    order_change_request_products = {}

    if order_change_request:
        order_change_request_products = {item.product_id: Product.query.get(item.product_id) for item in order_change_request.orders_list}

    return render_template('tickets/workflows/admin_order_review.html', order=order, products=products, order_change_request=order_change_request, order_change_request_products=order_change_request_products, request_type=request_type, ticket=ticket)

@ticket_blueprint.route('/<ticket_id>/orders/<order_id>/approve', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def approve_order_changes(ticket_id, order_id):
    action = request.args.get('action')
    order = Orders.query.get_or_404(order_id)
    order_change_request = OrderChangeRequest.query.filter_by(order_id=order_id).first()
    ticket = TicketForum.query.filter_by(id=ticket_id).first()

    if request.method == 'POST':
        if action == 'approve':
            # apply the changes from the OrderChangeRequest to the Order
            order.order_date = order_change_request.order_date
            order.customer_id = order_change_request.customer_id
            order.orders_list = order_change_request.orders_list

            # delete the OrderChangeRequest from the database. The original order information has already been saved to OrderHistory when the order was created; another copy will be saved now using the after_update_listener on the model
            db.session.delete(order_change_request)

            ticket.resolution_status = 'resolved'
            ticket.resolution_date = date.today()

            db.session.commit()

            return redirect(url_for("ticket_blueprint.ticket", ticket_id=ticket_id))
        
        elif action == 'reject':
            # save copy of the OrderChangeRequest to OrderHistory table; even though the changes are rejected, we may need to refer to them later 
            order_history = OrderHistory(
                order_id=order_change_request.id,
                timestamp=datetime.now(),
                user_id=current_user.id,
                # type='rejected order change request'
            )
            db.session.add(order_history)

            # delete the OrderChangeRequest from the database
            db.session.delete(order_change_request)

            ticket.resolution_status = 'resolved'
            ticket.resolution_date = date.today()

            db.session.commit()

            return redirect(url_for("ticket_blueprint.ticket", ticket_id=ticket_id))

    return render_template('tickets/workflows/customer_order_edit.html', primary_title='Edit Order', order=order, order_change_request=order_change_request)



@ticket_blueprint.route('/<ticket_id>/orders/<order_id>/approve-order-cancel', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def approve_order_cancel(ticket_id, order_id):
    order = Orders.query.get_or_404(order_id)
    ticket = TicketForum.query.filter_by(id=ticket_id).first()

    if request.method == 'POST':        

        new_order_history = OrderHistory(
            order_id=order.id,
            timestamp=datetime.now(),
            user_id=current_user.id,
            # type='cancelled order'
        )

        db.session.add(new_order_history)
        ticket.resolution_status = 'resolved'
        ticket.resolution_date = date.today()
        order.is_cancelled = True
        db.session.commit()

        return redirect(url_for("ticket_blueprint.ticket", ticket_id=ticket_id))

    return render_template('tickets/workflows/customer_order_edit.html', primary_title='Edit Order', order=order)