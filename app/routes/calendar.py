from flask import Blueprint, render_template, redirect, url_for, request
from datetime import date
from flask_login import login_required, current_user
from app.db.models import Event
from app.db import db

calendar_blueprint = Blueprint('calendar_blueprint', __name__, url_prefix="/calendar")

@calendar_blueprint.route("/")
@login_required
def calendar():
  events = Event.query.filter_by(user_id=current_user.id).all()

  return render_template('calendar/calendar.html', events=events, current_user = current_user)

@calendar_blueprint.route("/create", methods=['GET', 'POST'])
@login_required
def calendar_create():
  if request.method == 'POST':
    title = request.form.get('title')
    description = request.form.get('description')
    start = request.form.get('start')
    end = request.form.get('end')
    location = request.form.get('location')

    new_event = Event(title=title, description=description, start_datetime=start, end_datetime=end, location=location, 
                      date_created = date.today(), user_id=current_user.id)
    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for("calendar_blueprint.calendar"))


  return render_template('calendar/create_event.html', current_user = current_user)

@calendar_blueprint.route("/<event_id>")
@login_required
def calendar_event(event_id):
  event = Event.query.filter_by(id=event_id).first()

  return render_template('calendar/event.html', event=event, current_user = current_user)
