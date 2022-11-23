from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from app.db.models import Ticket, TicketComment, TicketForum, Resolution
from app.admin import admin_permission
from app.db import db

user_permission = Permission(RoleNeed('user'))

ticket_blueprint = Blueprint('ticket_blueprint', __name__, url_prefix="/tickets")

@ticket_blueprint.route("/")
@login_required
def tickets():
  tickets = TicketForum.query.filter_by().all() # filter by company once company/customer model fixed
  
  return render_template('tickets/ticket_list.html',  title = "Tickets", tickets = tickets, current_user = current_user)

@ticket_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def create_ticket():
  if request.method == 'POST':
    summary = request.form.get('summary')
    content = request.form.get('content')
    tags = request.form.get('tags')
    new_ticket = TicketForum(summary=summary, content=content,tags=tags)
    db.session.add(new_ticket)
    db.session.commit()
    
    return redirect(url_for("ticket_blueprint.tickets"))

  return render_template('tickets/create_ticket.html')

@ticket_blueprint.route("/<ticket_id>", methods=['GET', 'POST'])
@login_required
@user_permission.require()
def ticket(ticket_id):
  if request.method == 'POST':

    return redirect(url_for("ticket_blueprint.ticket", ticket_id=ticket_id))


  return render_template('tickets/ticket.html', )

@ticket_blueprint.route('/delete/ticket/<id>', methods=['POST'])
@login_required
@admin_permission.require()
def delete_ticket(id):

  return redirect(url_for('ticket_blueprint.tickets'))


@ticket_blueprint.route('/delete/ticket-comment/<id>', methods=['POST'])
@login_required
@admin_permission.require()
def delete_comment(id):


  return redirect(url_for('ticket_blueprint.ticket', ticket_id = id))