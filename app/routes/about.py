from flask import Blueprint, render_template, redirect, url_for, request
from datetime import date, datetime
from flask_login import login_required, current_user
from app.db.models import Event
from app.db import db

about_blueprint = Blueprint('about_blueprint', __name__,
                               url_prefix="/about")


@about_blueprint.route("/")
def view():
    about = About.query.filter_by(user_id=current_user.id).all()
    event_dates = set()

    for event in events:
        event_dates.add(event.start_date)

    dates = [datetime.strptime(date, "%Y-%m-%d") for date in list(event_dates)]
    dates.sort()
    sorted_dates = [datetime.strftime(date, "%Y-%m-%d") for date in dates]

    return render_template('calendar/calendar.html', events=events,
                           dates=sorted_dates, current_user=current_user)

@blogPosts.route('/about/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        new_post = BlogPost(title=title, content=content, tags=tags)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for("blogPosts.display_post", post_id=new_post.id))

    return render_template('blog/create.html', newPost=1, links=get_links())
 
@about_blueprint.route("/")
def view():
    events = Event.query.filter_by(user_id=current_user.id).all()
    event_dates = set()

    for event in events:
        event_dates.add(event.start_date)

    dates = [datetime.strptime(date, "%Y-%m-%d") for date in list(event_dates)]
    dates.sort()
    sorted_dates = [datetime.strftime(date, "%Y-%m-%d") for date in dates]

    return render_template('calendar/calendar.html', events=events,
                           dates=sorted_dates, current_user=current_user)