from flask import Flask, request, send_from_directory
from flask_login import LoginManager, current_user
from flask_principal import Principal, UserNeed, RoleNeed, \
    identity_loaded, AnonymousIdentity
from app.admin import admin_blueprint, admin
import app.routes as route
import app.db.models as model
from app.db import db
from app.util.security import edit_post_need, delete_post_need,\
                              edit_comment_need, delete_comment_need,\
                              delete_ticket_comment_need, delete_ticket_need,\
                              edit_ticket_comment_need, edit_ticket_need


principals = Principal()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder='static')

    # SQLAlchemy Config
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # adding to suppress warning, will delete later
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # S3 Config

    app.config['S3_BUCKET'] = "S3_BUCKET_NAME"
    app.config['S3_KEY'] = "AWS_ACCESS_KEY"
    app.config['S3_SECRET'] = "AWS_ACCESS_SECRET"
    app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format("")

    model.db.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    admin.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table,
        # use it in the query for the user
        return model.User.query.get(user_id)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        if not isinstance(identity, AnonymousIdentity):
            identity.user = current_user
            if hasattr(current_user, 'id'):
                identity.provides.add(UserNeed(current_user.id))
            if hasattr(current_user, 'roles'):
                for role in current_user.roles:
                    identity.provides.add(RoleNeed(role.name))
            if hasattr(current_user, 'posts'):
                for post in current_user.posts:
                    identity.provides.add(edit_post_need(post.id))
                    identity.provides.add(delete_post_need(post.id))
            if hasattr(current_user, 'comments'):
                for comment in current_user.comments:
                    identity.provides.add(edit_comment_need(comment.id))
                    identity.provides.add(delete_comment_need(comment.id))
            if hasattr(current_user, 'tickets'):
                for ticket in current_user.tickets:
                    identity.provides.add(delete_ticket_need(ticket.id))
                    identity.provides.add(edit_ticket_need(ticket.id))
            if hasattr(current_user, 'ticket_comments'):
                for comment in current_user.ticket_comments:
                    identity.provides.add(
                        delete_ticket_comment_need(comment.id)
                    )
                    identity.provides.add(
                        edit_ticket_comment_need(comment.id)
                    )

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    app.register_blueprint(route.auth_blueprint)
    app.register_blueprint(route.blogPosts_blueprint)
    app.register_blueprint(route.main_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(route.profile_blueprint)
    app.register_blueprint(route.company_blueprint)
    app.register_blueprint(route.forums_blueprint)
    app.register_blueprint(route.ticket_blueprint)
    app.register_blueprint(route.calendar_blueprint)
    app.register_blueprint(route.product_blueprint)

    return app
