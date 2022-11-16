from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_principal import Permission, RoleNeed
from . import admin
from .models.user import User, UserRoles, Role
from .models.company import Company, CompanyMembers
from .models.blog import BlogPost
from . import db

#Admin blueprint
admin_bpt = Blueprint('admin_bpt', __name__)

admin_permission = Permission(RoleNeed('admin'))


class SecureModelView(ModelView):
    @admin_permission.require()
    def is_accessible(self):
        return current_user.is_authenticated


class FixView(SecureModelView):
    column_display_pk = True # optional, but I like to see the IDs in the list
    column_hide_backrefs = False
    column_list = ('id', 'user_id', 'role_id')


#add DB model views into flask admin
admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Role, db.session))
admin.add_view(FixView(UserRoles, db.session))
admin.add_view(SecureModelView(Company, db.session))
admin.add_view(SecureModelView(BlogPost, db.session))
admin.add_view(FixView(CompanyMembers, db.session))
   
