from app.db import db
from app.db.models.blog import BlogPost
from app.db.models.customer import User, UserRoles, Role, Company, CompanyMembers
from app.db.models.forum import ForumComment, ForumPost, Thread, ThreadRoles
from app.db.models.product import Product
from app.db.models.orders import Contracts, Orders, ShippingAddress, Customer, OrdersList
from app.db.models.ticket import TicketComment, TicketForum, Resolution
from app.db.models.calendar import Event
from app.db.models.home import Home
from app.db.models.about import About
from app.db.models.jobs import Application, Job
from sqlalchemy.orm import with_polymorphic
from sqlalchemy import schema


#Company
Company.customer = db.relationship('Customer')

#User
User.roles = db.relationship('Role', secondary='user_roles')
User.posts = db.relationship('ForumPost')
User.comments = db.relationship('ForumComment')
User.companies = db.relationship('Company', secondary='company_members')
User.customer = db.relationship('Customer')
User.tickets = db.relationship('TicketForum')
User.ticket_comments = db.relationship('TicketComment')
User.posts = db.relationship('Application')

#Job
Job.application_id = db.relationship('Application')

#Application
Application.user_id = db.Column(db.String(36), db.ForeignKey('user.id',
                                                   ondelete='CASCADE'))
Application.job_id = db.Column(db.String(36), db.ForeignKey('job.id',
                                                ondelete='CASCADE'))

#User Roles
UserRoles.user_id = db.Column(db.String(36), db.ForeignKey('user.id',
                                                   ondelete='CASCADE'))
UserRoles.role_id = db.Column(db.String(36), db.ForeignKey('roles.id',
                                                ondelete='CASCADE'))
#Company Members
CompanyMembers.company_id = db.Column(db.String(36), db.ForeignKey('company.id',
                        ondelete='CASCADE'))
CompanyMembers.user_id = db.Column(db.String(36), db.ForeignKey('user.id',
                    ondelete='CASCADE'))
CompanyMembers.role_id = db.Column(db.String(36), db.ForeignKey('roles.id',
                    ondelete='CASCADE'))
#Role
Role.event_info = db.relationship('Event', back_populates="role_info", lazy=True)
#Customer
Customer.__table_args__ = (
        schema.CheckConstraint('NOT(user_id IS NULL AND company_id IS NULL)'),
    )
Customer.user_id = db.Column(db.String(36),
                    db.ForeignKey('user.id', ondelete='CASCADE'),
                    nullable=False)
Customer.company_id = db.Column(db.String(36),
                        db.ForeignKey('company.id', ondelete='CASCADE'),
                        nullable=False)
Customer.orders = db.relationship('Orders')
Customer.contracts = db.relationship('Contracts')
Customer.shipping_address = db.relationship('ShippingAddress')

#ShippingAddress
ShippingAddress.customer_id = db.Column(db.String(36),
                        db.ForeignKey('customer.id', ondelete='CASCADE'),
                        nullable=False)
#Orders
Orders.orders_list = db.relationship('OrdersList')
Orders.customer_id = db.Column(db.String(36), db.ForeignKey('customer.id',
                                                ondelete='CASCADE'))
#Contracts
Contracts.customer_id = db.Column(db.String(36), db.ForeignKey('customer.id',
                                                ondelete='CASCADE'))
#Thread
Thread.roles = db.relationship('Role', secondary='thread_roles')
#ThreadRoles
ThreadRoles.thread_id = db.Column(db.String(36), db.ForeignKey('thread.id',
                                                ondelete='CASCADE'))
ThreadRoles.role_id = db.Column(db.String(36), db.ForeignKey('roles.id',
                                                ondelete='CASCADE'))
#ForumPost
ForumPost.comments = db.relationship('ForumComment')
ForumPost.thread_id = db.Column(db.String(36), db.ForeignKey('thread.id',
                                                ondelete='CASCADE'))
ForumPost.author = db.Column(db.String(36), db.ForeignKey('user.id',
                                                ondelete='CASCADE'))
#ForumComment
ForumComment.author = db.Column(db.String(36), db.ForeignKey('user.id',
                                                ondelete='CASCADE'))
ForumComment.post_id = db.Column(db.String(36), db.ForeignKey('forum_post.id',
                                                ondelete='CASCADE'))
#Event
Event.user_id = db.Column(db.String(36), db.ForeignKey('user.id',
                                                ondelete='CASCADE'))
Event.organizer = db.Column(db.String(36), db.ForeignKey('user.id',
                                                ondelete='CASCADE'))
Event.role = db.Column(db.String(36), db.ForeignKey('roles.id',
                                                ondelete='CASCADE'))
Event.role_info = db.relationship("Role", back_populates="event_info", lazy=True)
#TicketForum
TicketForum.user_id = db.Column(db.String(36), db.ForeignKey('user.id',
                                                ondelete='CASCADE'))
TicketForum.customer_id = db.Column(db.String(36), db.ForeignKey('customer.id',
                                                ondelete='CASCADE'))
#TicketComment
TicketComment.ticket_id = db.Column(db.String(36), db.ForeignKey('ticket_forum.id',
                                                ondelete='CASCADE'))
TicketComment.author_id = db.Column(db.String(36), db.ForeignKey('user.id',
                                                ondelete='CASCADE'))
#OrdersList
OrdersList.orders_id = db.Column(db.String(36), db.ForeignKey('orders.id'))
OrdersList.product_id = db.Column(db.String(36), db.ForeignKey('product.id'))
