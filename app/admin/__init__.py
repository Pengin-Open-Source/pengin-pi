from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_principal import Permission, RoleNeed
from flask_admin import Admin
from ..models import User, UserRoles, Role, blog, company
from ..models.db import db

admin = Admin()
admin_blueprint = Blueprint('admin_blueprint', __name__)
admin_permission = Permission(RoleNeed('admin'))


class SecureModelView(ModelView):
    @admin_permission.require()
    def is_accessible(self):
        return current_user.is_authenticated


class FixView(SecureModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'role_id')


admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Role, db.session))
admin.add_view(FixView(UserRoles, db.session))
admin.add_view(SecureModelView(company.Company, db.session))
admin.add_view(SecureModelView(blog.BlogPost, db.session))
admin.add_view(FixView(company.CompanyMembers, db.session))