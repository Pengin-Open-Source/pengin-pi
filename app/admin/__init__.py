from flask_admin import Admin

from app.admin.views import (CompanyMembersView, SecureModelView,
                             ThreadRolesView, UserRolesView, RoleView,
                             admin_blueprint)
from app.db.models import (BlogPost, Company, CompanyMembers, Contracts,
                           Customer, Event, ForumComment, ForumPost, Orders,
                           Product, Resolution, Role, ShippingAddress, Thread,
                           ThreadRoles, TicketComment, TicketForum, User,
                           UserRoles, db)

admin = Admin()

admin.add_view(SecureModelView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(SecureModelView(Company, db.session))
admin.add_view(SecureModelView(BlogPost, db.session))
admin.add_view(SecureModelView(Contracts, db.session))
admin.add_view(SecureModelView(ForumPost, db.session))
admin.add_view(SecureModelView(ForumComment, db.session))
admin.add_view(SecureModelView(Thread, db.session))
admin.add_view(SecureModelView(Orders, db.session))
admin.add_view(SecureModelView(ShippingAddress, db.session))
admin.add_view(SecureModelView(Customer, db.session))
admin.add_view(SecureModelView(Product, db.session))
admin.add_view(SecureModelView(TicketForum, db.session))
admin.add_view(SecureModelView(TicketComment, db.session))
admin.add_view(SecureModelView(Resolution, db.session))
admin.add_view(SecureModelView(Event, db.session))

admin.add_view(CompanyMembersView(CompanyMembers, db.session))
admin.add_view(UserRolesView(UserRoles, db.session))
admin.add_view(ThreadRolesView(ThreadRoles, db.session))
