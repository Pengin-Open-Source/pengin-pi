from app import create_app
from app import db
from app.db.models import Thread, ThreadRoles, User, UserRoles, ForumPost, ForumComment, Home, About, Order, ShippingAddress, Customer, Company, CompanyMembers, Role, Contracts, Event, BlogPost


def create_all():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
def create(model, **kwargs):
    new = model(kwargs)
    app = create_app()
    
    with app.app_context():
        db.session.add(new)
        db.session.commit()

def getone(model, **kwargs):
    app = create_app()
    with app.app_context():
        return model.query.filter_by(kwargs).first()
        
def update(model, search:dict, change:dict):
    lookup = getone(model, **search)
    #TODO: apply changes to lookup 
    #db.session.commit()
    
def build():
    #TODO: build out the seeder file.
    pass


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        user = User.query.filter_by(email="stuart@tobupengin.com").first().id
        role = Role.query.filter_by(name="user").first().id
        new = UserRoles(user_id=user, role_id=role)
        db.session.add(new)
        db.session.commit()