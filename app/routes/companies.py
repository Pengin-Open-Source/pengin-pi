from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_principal import Permission, RoleNeed
from app.db import db, paginate, paginate_join
from app.db.models import Company, CompanyMembers, User
from app.util.security.limit import limiter
from app.util.security import user_permission, view_company_permission, permission_required

company_info = Blueprint('company_info', __name__, url_prefix="/company")
admin_permission = Permission(RoleNeed('admin'))


@company_info.route("/", methods=['GET', 'POST'])
@login_required
@user_permission.require()
def display_companies_home():
    def handle_admin_view():
        if request.method == "POST":
            page = int(request.form.get('page_number', 1))
        else:
            page = 1
        companies = Company.query.paginate(
            page=page, per_page=10, error_out=False)
        return render_template('company_info/company_info_main.html',
                               companies=companies, primary_title='Companies')

    def handle_user_view():
        member_company = CompanyMembers.query.filter_by(
            user_id=current_user.id).first()
        if member_company:
            return redirect(url_for('company_info.display_company_info', company_id=member_company.company_id))
        return render_template('company_info/no_company.html')

    is_admin = admin_permission.can()

    if is_admin:
        return handle_admin_view()
    else:
        return handle_user_view()


@company_info.route('/<company_id>', methods=['POST', 'GET'])
@login_required
@user_permission.require()
def display_company_info(company_id: str) -> render_template:
    """display company info method
    This method handles the company/company_id route and returns a company information view.

    Required Inputs:
        company_id: company UUID4 string

    Outputs:
        render_template -> company_info.html
    Output Arguments:
        company_info.html, company query, paginated company members
    """

    # Get company from database
    company = Company.query.get_or_404(company_id)
    # If POST, get page number from form button
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    # custom paginate method to join two tables and paginate results.  Gets users where members of company_id
    members = paginate_join(User, CompanyMembers, User.id == CompanyMembers.user_id, page=page,
                            pages=10, filters={'company_id': company_id})

    return render_template('company_info/company_info.html', primary_title='Company Info',
                           company=company, members=members)


@company_info.route('/create', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
@user_permission.require()
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

    return render_template('company_info/company_info_create.html', primary_title='Create New Company')


@company_info.route('/<company_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
@user_permission.require()
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

    return render_template('company_info/company_edit.html', company=company, primary_title='Edit Company')


@company_info.route('/<company_id>/members', methods=['GET', 'POST'])
@login_required
@user_permission.require()
@permission_required(view_company_permission(company_id))
def display_company_members(company_id):
    company = Company.query.get_or_404(company_id)

    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    users = paginate(User, page=page, pages=10)
    members_ids = CompanyMembers.query.with_entities(
        CompanyMembers.user_id).filter_by(company_id=company.id).all()
    members_ids_list = [i for i in members_ids for i in i]

    return render_template('company_info/display_members.html', users=users, company=company, page=page, members_ids_list=members_ids_list)


@company_info.route('/<company_id>/members/edit', methods=['GET', 'POST'])
@login_required
@admin_permission.require()
@user_permission.require()
def edit_company_members(company_id):
    company = Company.query.filter_by(id=company_id).first()
    if request.method == "POST":
        page = int(request.form.get('page_number', 1))
    else:
        page = 1

    users = paginate(User, page=page, pages=10)
    members_ids = CompanyMembers.query.with_entities(
        CompanyMembers.user_id).filter_by(company_id=company.id).all()
    members_ids_list = [i for i in members_ids for i in i]

    return render_template('company_info/edit_members.html', users=users, company=company, page=page, members_ids_list=members_ids_list)


@limiter.limit("10 per minute")
@company_info.route('/<company_id>/members/edit/save', methods=['POST'])
@login_required
@admin_permission.require()
@user_permission.require()
def edit_company_members_post(company_id):
    if request.method == 'POST':
        company = Company.query.filter_by(id=company_id).first()
        checkbox_values = request.form.getlist('member-checkbox')
        page_num = request.form.get('page-number')
        users_for_delete = paginate(User, int(page_num), pages=9)
        members_ids = CompanyMembers.query.with_entities(
            CompanyMembers.user_id).filter_by(company_id=company.id).all()
        members_ids_list = [i for i in members_ids for i in i]

        # clear members so only those with checkboxes are left in DB.
        for user in users_for_delete:
            if user.id in members_ids_list:
                CompanyMembers.query.filter_by(user_id=user.id).delete()

        for value in checkbox_values:
            user = User.query.filter_by(id=value).first()
            new_member = CompanyMembers(company_id=company.id, user_id=user.id)
            db.session.add(new_member)

        db.session.commit()

        return redirect(url_for('company_info.edit_company_members',
                                company_id=company.id))
