from flask import Blueprint, render_template, redirect, url_for, request, abort
from datetime import date
from flask_login import login_required, current_user
from flask_principal import Permission, RoleNeed
from app.db.models import TicketComment, TicketForum, Resolution
from app.util.security import admin_permission, user_permission, delete_ticket_comment_permission, delete_ticket_permission
from app.db import db


ticket_blueprint = Blueprint('ticket_blueprint', __name__, url_prefix="/tickets")

@ticket_blueprint.route("/")
@login_required
def tickets():
  tickets = TicketForum.query.filter_by().all() # filter by company once company/customer model fixed
  return render_template('tickets/ticket_list.html',is_admin=admin_permission.can(), can_delete=delete_ticket_permission,  title="Tickets", tickets=tickets, current_user=current_user)

@ticket_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
@user_permission.require()
def create_ticket():
  if request.method == 'POST':
    summary = request.form.get('summary')
    content = request.form.get('content')
    tags = request.form.get('tags')
    user_id = current_user.id
    new_ticket = TicketForum(summary=summary, content=content,tags=tags, user_id=user_id)
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
    new_comment = TicketComment(ticket_id=ticket_id, content=content, date=today, author_id=author_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for("ticket_blueprint.ticket", ticket_id=ticket_id))
  ticket =  TicketForum.query.filter_by(id=ticket_id).first()
  comments= TicketComment.query.filter_by(ticket_id=ticket_id).all()
  return render_template('tickets/ticket.html',is_admin=admin_permission.can(), can_delete=delete_ticket_comment_permission, ticket=ticket, comments=comments )

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
    return redirect(url_for('ticket_blueprint.ticket', ticket_id = comment.ticket_id))

  abort(403)