from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.db import db
from app.db.models import Event, Role, User
from app.db.util import paginate
from sqlalchemy import asc
from app.util.security import admin_permission, user_permission, access_event_permission,  permission_required


calendar_blueprint = Blueprint('calendar_blueprint', __name__,
                               url_prefix="/calendar")


@calendar_blueprint.route("/", methods=["GET", "POST"])
@login_required
@user_permission.require()
def calendar():
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    user = User.query.filter_by(id=current_user.id).first()
    events = paginate(Event, page=page, pages=10,
                      order=asc, key="start_datetime")

    user_roles = set()
    for role in user.roles:
        user_roles.add(role.id)

    # group events by start_date (for UI/display purpose)
    events_by_start_date = {}
    for event in events:
        # Only load events for a role the user belongs to
        if event.role not in user_roles:
            continue

        event.add_time()
        start_date = event.start_datetime.date()

        if start_date in events_by_start_date:
            events_by_start_date[start_date].append(event)
        else:
            events_by_start_date[start_date] = [event]

    return render_template('calendar/calendar.html', events_by_start_date=events_by_start_date, events=events, current_user=current_user, primary_title='Calendar')


@calendar_blueprint.route("/create", methods=['GET', 'POST'])
@login_required
@user_permission.require()
def calendar_create():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        start_datetime = datetime.strptime(
            request.form.get('start_datetime'), '%Y-%m-%dT%H:%M')
        end_datetime = datetime.strptime(
            request.form.get('end_datetime'), '%Y-%m-%dT%H:%M')
        location = request.form.get('location').strip()
        role = request.form.get('role')
        # get user_id from User to set the organizer of event
        member = request.form.get('user_id')

        # add "organizer" input later. Assume organizer = event creator for now
        # already update the organizer of event after selecting user from 'creat-event-form'
        new_event = Event(user_id=member, organizer=member, role=role, title=title,
                          description=description, location=location, start_datetime=start_datetime, end_datetime=end_datetime)
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for("calendar_blueprint.calendar"))

    # query all roles to see who can view the event
    # an admin user can pick any role for an event
    # Any other user can only pick one of their own roles for an event
    # Theorectically, this could be expanded to allow for certain higher-level,  non-admin users to
    # pick certain roles that they don't posses,  but that they oversee.
    if admin_permission.can():
        roles = Role.query.all()
    else:
        roles = current_user.roles()

    # query all users to select the organizer of a new upcoming event
    # maybe some users should be prevented from seeing certain other users in some cases?
    users = User.query.all()
    return render_template('calendar/create_event.html',
                           current_user=current_user, roles=roles, users=users)


@calendar_blueprint.route("/<event_id>")
@login_required
@user_permission.require()
@permission_required(access_event_permission, 'event_id')
def calendar_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    event.add_date()
    event.add_time()
    organizer = User.query.filter_by(id=event.organizer).first()

    return render_template('calendar/event.html', event=event,
                           current_user=current_user, organizer=organizer)
