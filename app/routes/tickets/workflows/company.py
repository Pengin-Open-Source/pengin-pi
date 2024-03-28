# app/routes/tickets/workflows/company.py

import uuid
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from datetime import date, datetime
from app.db import db
from app.db.models import TicketForum, Company, User, CompanyMembers

company_ticket = Blueprint('company_ticket', __name__, url_prefix='/tickets/company')

@company_ticket.route("/create", methods=["GET", "POST"])
@login_required
def handle_create_company_ticket():
    if request.method == "POST":
        form_data = request.form
        new_ticket = TicketForum(
            summary=form_data.get('summary'),
            content=f"Request to create company:\nCompany Name: {form_data.get('company_name')}\nAddress: {form_data.get('address1')} {form_data.get('address2')}, {form_data.get('city')}, {form_data.get('state')}, {form_data.get('zipcode')}, {form_data.get('country')}\nPhone: {form_data.get('phone')}\nEmail: {form_data.get('email')}\nAdditional Information: {form_data.get('additional_info')}",
            tags="edit_company",
            user_id=current_user.id,
            date=date.today(),
            resolution_status='open'
        )
        db.session.add(new_ticket)
        db.session.commit()

    return render_template('tickets/workflows/customer_create_company.html')

@company_ticket.route("/edit", methods=["GET", "POST"])
def handle_edit_company_ticket():
    if request.method == "POST":
        form_data = request.form
        new_ticket = TicketForum(
            summary=form_data.get('summary'),
            content=f"Request to edit company information:\nCompany Name: {form_data.get('company_name')}\nAddress: {form_data.get('address1')} {form_data.get('address2')}, {form_data.get('city')}, {form_data.get('state')}, {form_data.get('zipcode')}, {form_data.get('country')}\nPhone: {form_data.get('phone')}\nEmail: {form_data.get('email')}\nAdditional Information: {form_data.get('additional_info')}",
            tags="edit_company",
            user_id=current_user.id,
            date=date.today(),
            resolution_status='open'
        )
        db.session.add(new_ticket)
        db.session.commit()

    return render_template('tickets/workflows/customer_edit_company.html')


@company_ticket.route("/members_edit/<string:company_id>", methods=["GET", "POST"])
@login_required
def handle_edit_company_members_ticket(company_id):
    company = Company.query.get_or_404(company_id)
    users = User.query.all()
    existing_member_ids = [str(member.user_id) for member in CompanyMembers.query.filter_by(company_id=company.id).all()]

    if request.method == "POST":
        selected_member_ids = request.form.getlist('member_ids[]')
        deselected_member_ids = set(existing_member_ids) - set(selected_member_ids)
        newly_selected_member_ids = set(selected_member_ids) - set(existing_member_ids) # New line

        deselected_members_names = [User.query.get(id).name for id in deselected_member_ids]
        newly_selected_members_names = [User.query.get(id).name for id in newly_selected_member_ids] # New line

        summary = f"Edit Members Request for {company.name}"
        content = ""
        if deselected_members_names:
            content += "\nMembers to be excluded: " + ", ".join(deselected_members_names)
        if newly_selected_members_names: # New line
            content += "\nMembers to be included: " + ", ".join(newly_selected_members_names) # New line

        new_ticket = TicketForum(
            summary=summary,
            content=content,
            tags="edit_company_members",
            user_id=current_user.id,
            date=date.today(),
            resolution_status='open'
        )
        db.session.add(new_ticket)
        db.session.commit()

        return redirect(url_for('company_info.display_company_info', company_id=company_id))

    return render_template('tickets/workflows/customer_edit_company_members.html', 
                           company=company, 
                           users=users, 
                           existing_member_ids=existing_member_ids)
