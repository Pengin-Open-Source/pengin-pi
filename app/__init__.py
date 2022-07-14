from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_principal import Principal, UserNeed, RoleNeed, identity_loaded, AnonymousIdentity

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

# init Principals so we can use it later
principals = Principal()
# init login manager so we can use it later
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # adding to suppress warning, will delete later
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    login_manager.init_app(app) #login manager
    principals.init_app(app) #principals
    
    #login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    #login_manager.init_app(app)

    from .models import User

    #####
    # logan kiser: troubleshooting db issues, will delete before submitting
    #              pull request.
    # with app.app_context():
    #     db.create_all()
    #####

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

      #Identity loaded when user logs in or logs out    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        if not isinstance(identity, AnonymousIdentity):
            identity.user = current_user
            # Add the UserNeed to the identity
            if hasattr(current_user, 'id'):
                identity.provides.add(UserNeed(current_user.id))
            # identity with the roles that the user provides
            if hasattr(current_user, 'roles'):
                for role in current_user.roles:
                    identity.provides.add(RoleNeed(role.name))

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for blogpost routes in app
    from .blogPosts import blogPosts as blogPosts_blueprint
    app.register_blueprint(blogPosts_blueprint)

    # blueprint for non-auth parts of app
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app