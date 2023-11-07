from flask import Flask, request, send_from_directory
from flask_login import LoginManager, current_user
from flask_principal import (AnonymousIdentity, Principal, RoleNeed, UserNeed,
                             identity_loaded)
from flask_migrate import Migrate
import app.db.models as model
import app.routes as route
#from app.admin import admin, admin_blueprint
from app.db import config
from app.util.security import (delete_comment_need, delete_post_need,
                               delete_ticket_comment_need, delete_ticket_need,
                               edit_comment_need, edit_post_need,
                               edit_ticket_comment_need, edit_ticket_need)
from app.util.time.time import copyright, time_zone
from app.util.uuid import id
from app.util.security.limit import limiter
from app.util.markup import markup

principals = Principal()
login_manager = LoginManager()
migrate = Migrate()

class DummyHome():
    company_name = ''
    article = ''
    image = ''


def create_app():
    app = Flask(__name__, static_folder='static')

    # SQLAlchemy Config
    app.config['SECRET_KEY'] = id()
    app.config.update(config)
    markup.init_app(app)
    limiter.init_app(app)
    model.db.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    #admin.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate.init_app(app, model.db)

    # Inject global variables to templates
    @app.context_processor
    def inject_globals():
        company = model.Home.query.first() or DummyHome()
        name = company.company_name
        return dict(company_name=name)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table,
        # use it in the query for the user
        return model.User.query.get(user_id)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        """Permissions loader function
        This method loads all of the user permissions
        to the user identity
        """
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

    # Register all routes as blueprints
    for blueprint in route.blueprints:
        app.register_blueprint(blueprint)

    #app.register_blueprint(admin_blueprint)

    app.context_processor(time_zone)
    app.context_processor(copyright)
    return app
