from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Ticket, TicketForum, Customer

tickets = Blueprint('tickets', __name__)

@tickets.route("/tickets")
def tickets():
    return render_template('ticket/ticket_main.html')

# Create ticket view
@tickets.route("/tickets/create_ticket", methods=['GET'])
def create_ticket_view():
    return render_template('ticket/ticket_create.html')

# POST create ticket
@tickets.route("/tickets/create_ticket", methods=['POST'])
def create_ticket():
    # Check if user is a customer
    customer = Customer.query.filter_by(user_id=current_user.id)
    if not customer:
        flash("Sorry, you're currently not a customer and only customers can submit a ticket.")
        return redirect(url_for('tickets.tickets')) # if not customer return to tickets
    # Get form data
    summary = request.form.get('summary')
    content = request.form.get('content')
    tags = request.form.get('tags')

    new_ticket = Ticket(summary=summary, content=content, tags=tags)

    # add the new ticket to the database
    db.session.add(new_ticket)
    db.session.commit()

    return redirect(url_for('main.tickets'))
    

# Edit ticket view
@tickets.route("/tickets/<int:ticket>/edit_ticket", methods=['GET'])
def edit_ticket_view(ticket):
    # temp ticket var
    ticket = {'title':"HELLO", 'content':'WORLD'}
    
    return render_template('ticket/ticket_edit.html', ticket=ticket)
