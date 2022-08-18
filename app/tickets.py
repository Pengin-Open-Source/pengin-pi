from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Ticket, TicketForum, Customer

tickets = Blueprint('tickets', __name__)

@tickets.route("/tickets")
@login_required
def tickets_view():
    tickets = TicketForum.query.order_by(TicketForum.date.desc()).all()
    return render_template('ticket/ticket_main.html', tickets=tickets)

# Create ticket view
@tickets.route("/tickets/create_ticket", methods=['GET'])
@login_required
def create_ticket_view():
    return render_template('ticket/ticket_create.html')

# POST create ticket
@tickets.route("/tickets/create_ticket", methods=['POST'])
@login_required
def create_ticket():
    # Check if user is a customer
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if not customer:
        flash("Sorry, you're currently not a customer and only customers can submit a ticket.")
        return redirect(url_for('main.home')) # if not customer return to home

    # Get form data
    summary = request.form.get('summary')
    content = request.form.get('content')
    tags = request.form.get('tags')


    new_ticket_forum = TicketForum(customer_id=customer.id, summary=summary, content=content, tags=tags)
    
    # add the new ticket forum to the database
    db.session.add(new_ticket_forum)
    db.session.commit()

    # refresh db to get new_ticket_forum id for new Ticket obj
    db.session.refresh(new_ticket_forum)

    new_ticket = Ticket(customer_id=customer.id, forum_post_id=new_ticket_forum.id)

    # add the new ticket to database
    db.session.add(new_ticket)
    db.session.commit()

    return redirect(url_for('tickets.tickets_view'))
    

# Edit ticket view
@tickets.route("/tickets/<int:ticket>/edit_ticket", methods=['GET'])
@login_required
def edit_ticket_view(ticket):
    # Get ticket from database
    ticket_obj = Ticket.query.filter_by(id=ticket).first()

    # Check ticket exists
    if not ticket_obj:
        flash("Sorry, this ticket doesn't exist")
        return redirect(url_for('tickets.tickets_view')) # if ticket doesn't exist return to tickets

    # Get ticket forum post
    ticket_forum = TicketForum.query.filter_by(id=ticket_obj.ticket_forum_post).first()

    if not ticket_forum:
        flash("Sorry, this ticket doesn't have a forum post.")
        return redirect(url_for('tickets.tickets_view')) # if ticket forum doesn't exist

    # Render edit ticket view with summary, content, and tags filled
    return render_template('ticket/ticket_edit.html', summary=ticket_forum.summary, content=ticket_forum.content, tags=ticket_forum.tags)

@tickets.route("/tickets/<int:ticket>/edit_ticket", methods=['POST'])
@login_required
def edit_ticket(ticket):
    # Check user is customer
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if not customer:
        flash("Sorry, you're currently not a customer and only customers can edit a ticket.")
        return redirect(url_for('main.home')) # if not customer return to home
    
    # Get ticket to be edited from database
    ticket_obj = Ticket.query.filter_by(id=ticket).first()

    # Check ticket exists
    if not ticket_obj:
        flash("Sorry, this ticket doesn't exist")
        return redirect(url_for('tickets.tickets_view')) # if ticket doesn't exist return to tickets
    
    # Check if user's customer id matches ticket's customer id
    if customer.id != ticket.customer_id:
        flash("Sorry, you're not the author of this ticket.")
        return redirect(url_for('tickets.tickets_view')) # if customer ids don't match return to tickets

    # Get form data
    summary = request.form.get('summary')
    content = request.form.get('content')
    tags = request.form.get('tags')

    # Get ticket forum post
    ticket_forum = TicketForum.query.filter_by(ticket_obj.forum_post_id).first()
    
    # Check ticket forum post exists
    if not ticket_forum:
        flash("Sorry, this ticket doesn't have a forum post.")
        return redirect(url_for('tickets.tickets_view')) # if ticket forum doesn't exist

    ticket_forum.summary = summary
    ticket_forum.content = content
    ticket_forum.tags = tags

    db.session.commit()

    return redirect(url_for('tickets.tickets_view'))
