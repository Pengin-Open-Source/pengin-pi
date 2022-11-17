from flask_admin import Admin
from app.db.models import db
from app.db.models import User, UserRoles, Role, BlogPost, Company, CompanyMembers
from app.admin.views import SecureModelView, FixView
from app.admin.views import admin_blueprint, admin_permission


admin = Admin()
admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Role, db.session))
admin.add_view(FixView(UserRoles, db.session))
admin.add_view(SecureModelView(Company, db.session))
admin.add_view(SecureModelView(BlogPost, db.session))
admin.add_view(FixView(CompanyMembers, db.session))