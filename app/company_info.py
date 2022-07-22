from flask import Blueprint, render_template, redirect, flash, url_for, request, abort
from flask_login import login_required, current_user
from . import db
from .models import Company
from datetime import datetime
from flask_principal import Permission, RoleNeed


company_info = Blueprint('company_info', __name__, url_prefix='/companies')
admin_permission = Permission(RoleNeed('admin'))

def get_companies():
    return Company.query.all()


@company_info.route("/")
def display_companies_home():
    return render_template('company_info/company_info_main.html', companies=get_companies())


# company info
@company_info.route('/<int:company_id>')
@login_required
def display_company_info(company_id):
    company = Company.query.get_or_404(company_id)
    return render_template('company_info/company_info.html', company=company)


@company_info.route('/create', methods=['GET', 'POST'])
@login_required
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
        ## TODO members?

        new_company = Company(name=name, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode, country=country, phone=phone, email=email)
        #add to the company membership table
        new_members_company = Members_Company(id = new_company.id , user_id = current_user.id)
        db.session.add(new_members_company)
        db.session.add(new_company)
        db.session.commit()
        return redirect(url_for("company_info.display_company", company_id=new_company.id))
    # handle GET method
    return render_template('company_info/company_info_create.html', companies=get_companies())


@company_info.route('/edit_company_info/<int:company_id>', methods=['POST'])
@login_required
def edit_company_info_post():

    # Get new information

    name = request.form.get('name')
    address1 = request.form.get('address1')
    address2 = request.form.get('address2')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')
    country = request.form.get('country')
    phone = request.form.get('phone')
    email = request.form.get('email')
    members = request.form.get('members')

    # TODO reflect changes

    return redirect(url_for('company_info.display_company_info'))

