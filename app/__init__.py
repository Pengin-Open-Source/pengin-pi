from flask import Flask, request, send_from_directory
from flask_login import LoginManager, current_user
from flask_principal import Principal, UserNeed, RoleNeed, identity_loaded, AnonymousIdentity
from app.admin import admin_blueprint, admin
import app.routes as route
import app.db.models as model


principals = Principal()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # adding to suppress warning, will delete later
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    model.db.init_app(app)
    login_manager.init_app(app) 
    principals.init_app(app) 
    admin.init_app(app)
    login_manager.login_view = 'auth.login' 

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
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

    return app
