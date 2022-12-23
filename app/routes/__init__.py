from app.routes.home import home_blueprint
from app.routes.auth import auth as auth_blueprint
from app.routes.forums import forums_blueprint
from app.routes.blogPosts import blogPosts as blogPosts_blueprint
from app.routes.profiles import profiles as profile_blueprint
from app.routes.companies import company_info as company_blueprint
from app.routes.tickets import ticket_blueprint
from app.routes.calendar import calendar_blueprint


# Routes variable is a list of blupeprints in this current directory
blueprints = [val for key, val in globals().items()
              if isinstance(val, type(home_blueprint))]
