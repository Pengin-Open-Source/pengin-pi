from app.routes.home import home_blueprint
from app.routes.auth import auth as auth_blueprint
from app.routes.forums import forums_blueprint
from app.routes.blog_posts import blogPosts as blogPosts_blueprint
from app.routes.profiles import profiles as profile_blueprint
from app.routes.calendar import calendar_blueprint
from app.routes.companies import company_info as company_blueprint
from app.routes.forums import forums_blueprint
from app.routes.profiles import profiles as profile_blueprint
from app.routes.tickets import ticket_blueprint
from app.routes.calendar import calendar_blueprint
from app.routes.products import product_blueprint
from app.routes.about import about_blueprint
from app.routes.orders import order_info as order_blueprint
from app.routes.jobs import jobs_blueprint


# Blueprints variable is a list of blueprints in this current directory
blueprints = [val for key, val in locals().items()
              if isinstance(val, type(home_blueprint))]
