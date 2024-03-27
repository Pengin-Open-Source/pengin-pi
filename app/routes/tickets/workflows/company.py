# app/routes/tickets/workflows/company.py

from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from datetime import date, datetime
from app.db import db
from app.db.models import TicketForum, Company, User

company_ticket = Blueprint('company_ticket', __name__, url_prefix='/tickets/company')

def handle_create_company_ticket(form_data):
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


def handle_edit_company_ticket(form_data):
    company_name = form_data.get('company_name')
    address1 = form_data.get('address1')
    address2 = form_data.get('address2', '')
    city = form_data.get('city')
    state = form_data.get('state')
    zipcode = form_data.get('zipcode')
    country = form_data.get('country')
    phone = form_data.get('phone', '')
    email = form_data.get('email')
    summary = form_data.get('summary', f'Edit Company Information Request: {company_name}')
    additional_info = form_data.get('additional_info', '')
    tags = "edit_company" 
    today = date.today()

    content = (f"Request to edit company information:\n"
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

def handle_edit_company_members_ticket(form_data):
    # Debugging: Print raw form data to ensure it's being received as expected
    #print("Form data received:", form_data)
    
    company_id = form_data.get('company_id')
    company = Company.query.get(company_id)
    
    all_member_ids_raw = form_data.get('all_member_ids', '')
    all_member_ids = all_member_ids_raw.split(',') if all_member_ids_raw else []
    selected_member_ids = form_data.getlist('member_ids[]')

    print("All Member IDs:", all_member_ids)
    #print("Selected Member IDs:", selected_member_ids)

    deselected_member_ids = set(all_member_ids) - set(selected_member_ids)

    #print("Deselected Member IDs:", deselected_member_ids)

    # Fetch names for both selected and deselected members
    selected_members_names = [User.query.get(user_id).name for user_id in selected_member_ids]
    deselected_members_names = [User.query.get(user_id).name for user_id in deselected_member_ids]

    summary = f"Edit Members Request for {company.name}"
    content = f"Selected Members to be updated to: {', '.join(selected_members_names)}."
    if deselected_members_names:
        content += f" Deselected Members: {', '.join(deselected_members_names)}."

    tags = "edit_company_members"
    today = date.today()

    new_ticket = TicketForum(
        summary=summary,
        content=content,
        user_id=current_user.id,
        date=today,
        resolution_status='open',
        tags=tags
    )
    db.session.add(new_ticket)
    db.session.commit()
