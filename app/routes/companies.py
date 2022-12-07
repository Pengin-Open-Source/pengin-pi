from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app.db import db
from app.db.models import Company, CompanyMembers


company_info = Blueprint('company_info', __name__, url_prefix="/companies")

def get_companies():
    return Company.query.all()

@company_info.route("/")
def display_companies_home():
    return render_template('company_info/company_info_main.html', companies=get_companies())

@company_info.route('/<company_id>')
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
        new_company = Company(name=name, address1=address1, address2=address2, city=city, state=state, zipcode=zipcode, country=country, phone=phone, email=email)
        db.session.add(new_company)
        db.session.commit()
        new_members_company = CompanyMembers(id = new_company.id , user_id = current_user.id)
        db.session.add(new_members_company)
        db.session.commit()
        return redirect(url_for("company_info.display_company_info", company_id=new_company.id))
    return render_template('company_info/company_info_create.html')

@company_info.route('/edit_company_info/<company_id>', methods=['GET','POST'])
@login_required
def edit_company_info_post(company_id):
    if request.method == 'POST':
        company = Company.query.filter_by(id=company_id).first()
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
        return redirect(url_for('company_info.display_company_info', company_id=company.id))
    company = Company.query.filter_by(id=company_id).first()
    return render_template('company_info/company_edit.html', company=company)