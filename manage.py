from app import create_app
from app import db
from app.db.models import * #import all models namespace, it's on purpose


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
    return model.query.filter_by(kwargs).first()
        
def update(model, search:dict, change:dict):
    lookup = getone(model, **search)
    #TODO: apply changes to lookup 
    #db.session.commit()
    
def build():
    #TODO: build out the seeder file.
    pass


if __name__ == "__main__":
    #do stuff here
    pass