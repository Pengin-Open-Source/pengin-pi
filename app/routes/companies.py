from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db, paginate
from app.db.models import Company, CompanyMembers, User

company_info = Blueprint('company_info', __name__, url_prefix="/company")
admin_permission = Permission(RoleNeed('admin'))


@company_info.route("/")
def display_companies_home():
    companies = Company.query.all()

    return render_template('company_info/company_info_main.html',
                           companies=companies, is_admin=admin_permission.can())


@company_info.route('/<company_id>')
@login_required
def display_company_info(company_id):
    company = Company.query.get_or_404(company_id)

    return render_template('company_info/company_info.html', company=company)


@company_info.route('/editor', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def company_editor():
    companies = Company.query.all()

    return render_template('company_info/company_editor.html', companies=companies, is_admin=admin_permission.can())


@company_info.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def create_company():
    if request.method == 'POST':
        name = request.form.get('name')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        country = request.form.get('country')
        phone = request.form.get('phone')
        email = request.form.get('email')
        new_company = Company(name=name, address1=address1, address2=address2,
                              city=city, state=state, zipcode=zipcode,
                              country=country, phone=phone, email=email)
        db.session.add(new_company)
        db.session.commit()
        new_members_company = CompanyMembers(id=new_company.id,
                                             user_id=current_user.id)
        db.session.add(new_members_company)
        db.session.commit()

        return redirect(url_for("company_info.display_company_info",
                                company_id=new_company.id))

    return render_template('company_info/company_info_create.html')


@company_info.route('/<company_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_company_info_post(company_id):
    company = Company.query.filter_by(id=company_id).first()

    if request.method == 'POST':
        company.name = request.form.get('name')
        company.address1 = request.form.get('address1')
        company.address2 = request.form.get('address2')
        company.city = request.form.get('city')
        company.state = request.form.get('state')
        company.zipcode = request.form.get('zipcode')
        company.country = request.form.get('country')
        company.phone = request.form.get('phone')
        company.email = request.form.get('email')
        db.session.commit()

        return redirect(url_for('company_info.display_company_info',
                                company_id=company.id))

    return render_template('company_info/company_edit.html', company=company)


@company_info.route('/<company_id>/members/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
def edit_company_members(company_id):
    company = Company.query.filter_by(id=company_id).first()
    page = request.args.get('page')

    if not page:
        page = 1
    else:
        page = int(page)

    next_page = page + 1
    prev_page = page - 1
    users = paginate(User, page, pages=9)

    if request.method == 'POST':
        checkbox_values = request.form.getlist('member-checkbox')

        # clear all members so only those with checkboxes can be added.
        for user in users:
            company.members.remove(user)

        for value in checkbox_values:
            user = User.query.filter_by(id=value).first()
            company.members.append(user)

        db.session.commit()

        return redirect(url_for('company_info.display_company_info',
                                company_id=company.id))

    return render_template('company_info/edit_members.html', users=users, company=company, page=page, next_page=next_page, prev_page=prev_page)
