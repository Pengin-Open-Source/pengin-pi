from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
from .models import Ticket, TicketForum, Customer

tickets = Blueprint('tickets', __name__)

@tickets.route("/tickets")
def tickets_view():
    tickets = TicketForum.query.order_by(TicketForum.date.desc()).all()
    return render_template('ticket/ticket_main.html', tickets=tickets)

# Create ticket view
@tickets.route("/tickets/create_ticket", methods=['GET'])
def create_ticket_view():
    return render_template('ticket/ticket_create.html')

# POST create ticket
@tickets.route("/tickets/create_ticket", methods=['POST'])
def create_ticket():
    # Check if user is a customer
    customer = Customer.query.filter_by(user_id=current_user.id).first()
    if not customer:
        flash("Sorry, you're currently not a customer and only customers can submit a ticket.")
        return redirect(url_for('tickets.tickets_view')) # if not customer return to tickets
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
def edit_ticket_view(ticket):
    # temp ticket var
    ticket = {'title':"HELLO", 'content':'WORLD'}
    
    return render_template('ticket/ticket_edit.html', ticket=ticket)
