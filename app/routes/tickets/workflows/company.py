# app/routes/tickets/workflows/company.py

from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import date, datetime
from app.db import db
from app.db.models import TicketForum

company_ticket = Blueprint('company_ticket', __name__, url_prefix='/tickets/company')

def handle_company_creation_ticket(form_data):
    company_name = form_data.get('company_name')
    address1 = form_data.get('address1')
    address2 = form_data.get('address2', '')
    city = form_data.get('city')
    state = form_data.get('state')
    zipcode = form_data.get('zipcode')
    country = form_data.get('country')
    phone = form_data.get('phone', '')
    email = form_data.get('email')
    summary = form_data.get('summary', f'Company Creation Request: {company_name}')
    additional_info = form_data.get('additional_info', '')
    tags = form_data.get('tags', '')
    today = date.today()

    content = (f"Summary: {summary}\n"
               f"Company Name: {company_name}\n"
               f"Address: {address1} {address2}, {city}, {state}, {zipcode}, {country}\n"
               f"Phone: {phone}\n"
               f"Email: {email}\n"
               f"Additional Information: {additional_info}")

    new_ticket = TicketForum(summary=summary,
                             content=content, tags=tags,
                             user_id=current_user.id, date=today,
                             resolution_status='open')
    db.session.add(new_ticket)
    db.session.commit()