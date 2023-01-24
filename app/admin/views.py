from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_principal import Permission, RoleNeed

admin_blueprint = Blueprint('admin_blueprint', __name__)
admin_permission = Permission(RoleNeed('admin'))


class SecureModelView(ModelView):
    @admin_permission.require()
    def is_accessible(self):
        return current_user.is_authenticated


class UserRolesView(SecureModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'role_id')

class RoleView(SecureModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'name')

class ThreadRolesView(SecureModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'thread_id', 'role_id')


class CompanyMembersView(SecureModelView):
    column_display_pk = True  # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'company_id', 'role_id')
