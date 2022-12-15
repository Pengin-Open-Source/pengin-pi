from flask_admin import Admin
from app.db.models import db
from app.db.models import User, UserRoles, Role, BlogPost, Company,\
                          CompanyMembers, Contracts, ForumPost,\
                          ForumComment, Thread, Order, ShippingAddress,\
                          Customer, Product, TicketComment, TicketForum,\
                          Resolution, Event, ThreadRoles

from app.admin.views import SecureModelView, FixView

admin = Admin()

admin.add_view(SecureModelView(User, db.session))
admin.add_view(SecureModelView(Role, db.session))
admin.add_view(SecureModelView(Company, db.session))
admin.add_view(SecureModelView(BlogPost, db.session))
admin.add_view(SecureModelView(Contracts, db.session))
admin.add_view(SecureModelView(ForumPost, db.session))
admin.add_view(SecureModelView(ForumComment, db.session))
admin.add_view(SecureModelView(Thread, db.session))
admin.add_view(SecureModelView(Order, db.session))
admin.add_view(SecureModelView(ShippingAddress, db.session))
admin.add_view(SecureModelView(Customer, db.session))
admin.add_view(SecureModelView(Product, db.session))
admin.add_view(SecureModelView(TicketForum, db.session))
admin.add_view(SecureModelView(TicketComment, db.session))
admin.add_view(SecureModelView(Resolution, db.session))
admin.add_view(SecureModelView(Event, db.session))

admin.add_view(FixView(CompanyMembers, db.session))
admin.add_view(FixView(UserRoles, db.session))
admin.add_view(FixView(ThreadRoles, db.session))
