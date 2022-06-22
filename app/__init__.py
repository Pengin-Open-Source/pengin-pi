from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # adding to suppress warning, will delete later
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    ######
    # logan kiser: troubleshooting db issues, will delete before submitting
    #              pull request.
    with app.app_context():
        db.create_all()
    ######

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))


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